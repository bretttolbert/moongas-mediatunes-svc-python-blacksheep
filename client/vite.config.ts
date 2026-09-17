import { defineConfig, loadEnv } from 'vite'
import vue from '@vitejs/plugin-vue'

// Vite runs under Node. Load env from .env files AND process.env.
// (loadEnv only returns VITE_*-prefixed vars, so merge in process.env too.)
const env = { ...loadEnv('', process.cwd(), ''), ...process.env }

// Flask backend serving the JSON API and media files.
const flaskBackend = env.FLASK_BACKEND_URL ?? 'http://127.0.0.1:5000'
// Must match flaskConfig.urlPrefix in mediaserver-config.yml (empty when unset).
const flaskPrefix = env.FLASK_URL_PREFIX ?? ''

// Proxy options shared by /api and /getfile.
const proxyOpts = {
  target: flaskBackend,
  changeOrigin: true,
  rewrite: (p: string) => `${flaskPrefix}${p}`,
} as const

export default defineConfig({
  plugins: [vue()],
  server: {
    port: 5173,
    proxy: {
      '/api': proxyOpts,
      '/getfile': proxyOpts,
    },
  },
})
