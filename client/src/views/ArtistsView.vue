<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import { useRoute, type LocationQueryRaw } from 'vue-router'
import { api } from '../api'
import { configState } from '../configStore'
import { formatResults } from '../utils/format'
import { queryList, queryScalar } from '../utils/queryParams'
import type { ArtistCount } from '../types'

/** Port of artists.html (artist counts table). */
const route = useRoute()

const artists = ref<ArtistCount[]>([])
const loading = ref(false)
const error = ref<string | null>(null)

async function load(): Promise<void> {
  loading.value = true
  error.value = null
  try {
    const data = await api.artists(route.query)
    artists.value = data.artists
  } catch (e) {
    error.value = e instanceof Error ? e.message : String(e)
    artists.value = []
  } finally {
    loading.value = false
  }
}

watch(() => route.query, load, { immediate: true })

const maxResults = computed(() => configState.config?.maxResults ?? 50000)

/**
 * Sort header links preserve genre/minYear/maxYear
 * (mirrors the url_for calls in artists.html).
 */
function sortQuery(sort: string): LocationQueryRaw {
  return {
    genre: queryList(route.query, 'genre'),
    minYear: queryScalar(route.query, 'minYear') ?? undefined,
    maxYear: queryScalar(route.query, 'maxYear') ?? undefined,
    sort,
  }
}
</script>

<template>
  <div>
    <div class="results-info">
      {{ formatResults(artists.length, maxResults) }}
      <router-link class="button-link" :to="{ path: '/player', query: route.query }"
        >shuffle</router-link
      >:
    </div>
    <div v-if="error" class="error">{{ error }}</div>
    <div v-else-if="loading">loading…</div>
    <div v-else id="trackList">
      <table class="w-100">
        <tr>
          <th>
            <router-link :to="{ path: '/artists', query: sortQuery('count') }">Count</router-link>
          </th>
          <th>
            <router-link :to="{ path: '/artists', query: sortQuery('name') }">Artist</router-link>
          </th>
        </tr>
        <tr v-for="artist in artists" :key="artist.name">
          <td>{{ artist.count }}</td>
          <td>
            <router-link :to="{ path: '/artist', query: { artist: artist.name } }">{{
              artist.name
            }}</router-link>
          </td>
        </tr>
      </table>
    </div>
  </div>
</template>
