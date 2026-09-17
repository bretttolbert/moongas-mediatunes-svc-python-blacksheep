import { reactive } from 'vue'
import { api } from './api'
import type { ServerConfig } from './types'

/**
 * Global reactive store for the server-provided configuration
 * (playback methods, feature flags, limits). Loaded once at startup.
 */
export const configState = reactive({
  config: null as ServerConfig | null,
  error: null as string | null,
})

let loadPromise: Promise<void> | null = null

export function ensureConfigLoaded(): Promise<void> {
  if (!loadPromise) {
    loadPromise = api
      .config()
      .then((cfg) => {
        configState.config = cfg
      })
      .catch((e: unknown) => {
        configState.error = e instanceof Error ? e.message : String(e)
      })
  }
  return loadPromise
}
