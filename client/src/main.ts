import { createApp } from 'vue'
import App from './App.vue'
import { router } from './router'
import { ensureConfigLoaded } from './configStore'

import './assets/mediaserver.css'
import './assets/age_verification.css'

const app = createApp(App)
app.use(router)

// Load the server config before mounting so views can rely on it
// (playback methods, age verification, limits).
ensureConfigLoaded().finally(() => {
  app.mount('#app')
})
