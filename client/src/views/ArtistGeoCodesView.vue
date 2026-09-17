<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import { api } from '../api'
import { configState } from '../configStore'
import { formatResults } from '../utils/format'
import type { GeoCountItem, GeoKind } from '../types'

/**
 * Port of artist_geo_codes.html, covering the four geo pages:
 * /artist-countries, /artist-regions, /artist-cities, /artist-languages.
 */
const route = useRoute()

const items = ref<GeoCountItem[]>([])
const loading = ref(false)
const error = ref<string | null>(null)

const kind = computed(() => (route.meta.geoKind ?? 'countries') as GeoKind)
const geoType = computed(() => items.value[0]?.name ?? '')

async function load(): Promise<void> {
  loading.value = true
  error.value = null
  try {
    const data = await api.artistGeo(kind.value)
    items.value = data.items
  } catch (e) {
    error.value = e instanceof Error ? e.message : String(e)
    items.value = []
  } finally {
    loading.value = false
  }
}

watch(() => route.path, load, { immediate: true })

const maxResults = computed(() => configState.config?.maxResults ?? 50000)

/** Link to the artists page with this item's criteria (mirrors the url_for-built URLs). */
function itemQuery(item: GeoCountItem): Record<string, string> {
  return { sort: 'count', ...item.criteria }
}
</script>

<template>
  <div>
    <div class="results-info">
      {{ formatResults(items.length, maxResults) }}
      <router-link class="button-link" :to="{ path: '/player', query: route.query }"
        >shuffle</router-link
      >:
    </div>
    <div v-if="error" class="error">{{ error }}</div>
    <div v-else-if="loading">loading…</div>
    <div v-else id="trackList">
      <table class="w-100">
        <tr>
          <th>Count</th>
          <th>{{ geoType }}</th>
        </tr>
        <tr v-for="item in items" :key="item.value">
          <td>{{ item.count }}</td>
          <td>
            <router-link :to="{ path: '/artists', query: itemQuery(item) }">{{
              item.value
            }}</router-link>
          </td>
        </tr>
      </table>
    </div>
  </div>
</template>
