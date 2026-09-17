/**
 * Production server for the mediaserver SPA — plain Deno.serve, no framework.
 *
 * - Serves the Vite build output from client/dist
 * - Proxies /api/* and /getfile/* to the Flask backend (which owns the
 *   mediascan database and the media files)
 * - Falls back to index.html for unknown paths (SPA history-mode routing)
 *
 * Environment variables:
 *   PORT               listen port (default 8000)
 *   FLASK_BACKEND_URL  Flask backend base URL (default http://127.0.0.1:5000)
 *   FLASK_URL_PREFIX   must match flaskConfig.urlPrefix in mediaserver-config.yml
 *                      (default "", e.g. "/mediaserver" in production)
 */

const PORT = Number(Deno.env.get("PORT") ?? "8000");
const FLASK_BACKEND_URL = Deno.env.get("FLASK_BACKEND_URL") ?? "http://127.0.0.1:5000";
const FLASK_URL_PREFIX = (Deno.env.get("FLASK_URL_PREFIX") ?? "").replace(/\/$/, "");
const DIST_DIR = new URL("../client/dist/", import.meta.url);

const MIME_TYPES: Record<string, string> = {
  ".html": "text/html; charset=utf-8",
  ".js": "text/javascript; charset=utf-8",
  ".mjs": "text/javascript; charset=utf-8",
  ".css": "text/css; charset=utf-8",
  ".json": "application/json",
  ".svg": "image/svg+xml",
  ".png": "image/png",
  ".jpg": "image/jpeg",
  ".jpeg": "image/jpeg",
  ".webp": "image/webp",
  ".gif": "image/gif",
  ".ico": "image/x-icon",
  ".woff": "font/woff",
  ".woff2": "font/woff2",
  ".ttf": "font/ttf",
  ".map": "application/json",
  ".txt": "text/plain; charset=utf-8",
};

function contentType(path: string): string {
  const idx = path.lastIndexOf(".");
  if (idx < 0) return "application/octet-stream";
  return MIME_TYPES[path.slice(idx).toLowerCase()] ?? "application/octet-stream";
}

const HOP_BY_HOP_HEADERS = [
  "connection",
  "keep-alive",
  "proxy-authenticate",
  "proxy-authorization",
  "te",
  "trailer",
  "transfer-encoding",
  "upgrade",
];

async function proxyToFlask(req: Request): Promise<Response> {
  const url = new URL(req.url);
  const target = `${FLASK_BACKEND_URL}${FLASK_URL_PREFIX}${url.pathname}${url.search}`;

  const reqHeaders = new Headers(req.headers);
  reqHeaders.delete("host");
  for (const h of HOP_BY_HOP_HEADERS) reqHeaders.delete(h);

  const upstream = await fetch(target, {
    method: req.method,
    headers: reqHeaders,
    body: req.method === "GET" || req.method === "HEAD" ? null : req.body,
    redirect: "manual",
  });

  const respHeaders = new Headers(upstream.headers);
  for (const h of HOP_BY_HOP_HEADERS) respHeaders.delete(h);

  return new Response(upstream.body, {
    status: upstream.status,
    statusText: upstream.statusText,
    headers: respHeaders,
  });
}

async function serveStatic(pathname: string): Promise<Response | null> {
  // Prevent path traversal, then resolve relative to the dist directory.
  const rel = pathname.replace(/^\/+/, "").split("/").filter((p) => p !== "..").join("/");
  if (rel === "") return null;
  const fileUrl = new URL(rel, DIST_DIR);
  try {
    const stat = await Deno.stat(fileUrl);
    if (!stat.isFile) return null;
    const body = await Deno.readFile(fileUrl);
    return new Response(body, {
      headers: { "content-type": contentType(rel) },
    });
  } catch {
    return null;
  }
}

async function serveIndex(): Promise<Response> {
  try {
    const body = await Deno.readFile(new URL("index.html", DIST_DIR));
    return new Response(body, {
      headers: { "content-type": "text/html; charset=utf-8" },
    });
  } catch {
    return new Response(
      "client/dist not found — run `deno task build` first.",
      { status: 503, headers: { "content-type": "text/plain; charset=utf-8" } },
    );
  }
}

async function handler(req: Request): Promise<Response> {
  const url = new URL(req.url);

  if (url.pathname.startsWith("/api/") || url.pathname.startsWith("/getfile/")) {
    try {
      return await proxyToFlask(req);
    } catch (err) {
      // Client disconnected / request aborted mid-flight: harmless, don't log a 502.
      const e = err as { name?: string; code?: string };
      if (e?.name === "AbortError" || e?.code === "ECONNRESET") {
        return new Response(null, { status: 499 }); // client closed request
      }
      console.error(`Proxy error for ${url.pathname}:`, err);
      return new Response(`Bad Gateway: Flask backend unreachable at ${FLASK_BACKEND_URL}`, {
        status: 502,
        headers: { "content-type": "text/plain; charset=utf-8" },
      });
    }
  }

  const staticResp = await serveStatic(url.pathname);
  if (staticResp) return staticResp;

  // SPA fallback: let the client-side router handle unknown paths.
  return await serveIndex();
}

console.log(`mediaserver SPA server listening on http://0.0.0.0:${PORT}`);
console.log(`Proxying /api and /getfile to ${FLASK_BACKEND_URL}${FLASK_URL_PREFIX}`);
Deno.serve({ port: PORT, hostname: "0.0.0.0" }, handler);
