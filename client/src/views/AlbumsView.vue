<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import { api, getfileUrl } from '../api'
import { configState } from '../configStore'
import { formatResults } from '../utils/format'
import { queryList, queryScalar } from '../utils/queryParams'
import type { AlbumInfo } from '../types'

/** Port of albums.html (album cover grid). */
const route = useRoute()

const albums = ref<AlbumInfo[]>([])
const loading = ref(false)
const error = ref<string | null>(null)

async function load(): Promise<void> {
  loading.value = true
  error.value = null
  try {
    const data = await api.albums(route.query)
    albums.value = data.albums
  } catch (e) {
    error.value = e instanceof Error ? e.message : String(e)
    albums.value = []
  } finally {
    loading.value = false
  }
}

watch(() => route.query, load, { immediate: true })

const filterArtists = computed(() => queryList(route.query, 'artist'))
const filterGenres = computed(() => queryList(route.query, 'genre'))
const filterYear = computed(() => queryScalar(route.query, 'year'))
const filterMinYear = computed(() => queryScalar(route.query, 'minYear'))
const filterMaxYear = computed(() => queryScalar(route.query, 'maxYear'))

const maxResults = computed(() => configState.config?.maxResultsAlbumCovers ?? 500)
</script>

<template>
  <div>
    <div>
      <i>
        <template v-if="filterArtists.length">{{ filterArtists.join(', ') }} </template>
        <template v-if="filterGenres.length">{{ filterGenres.join(', ') }} </template>
        <template v-if="filterYear">{{ filterYear }} </template>
        <template v-if="filterMinYear">{{ filterMinYear }} - </template>
        <template v-if="filterMaxYear">{{ filterMaxYear }} </template>
      </i>
      <br />
    </div>

    <div class="results-info">
      {{ formatResults(albums.length, maxResults) }}
      <router-link class="button-link" :to="{ path: '/player', query: route.query }"
        >shuffle</router-link
      >:
    </div>
    <div v-if="error" class="error">{{ error }}</div>
    <div v-else-if="loading">loading…</div>
    <div id="trackList">
      <router-link
        v-for="album in albums"
        :key="`${album.artist}|${album.album}|${album.year}`"
        :to="{
          path: '/tracks',
          query: { albumartist: album.artist, album: album.album, year: String(album.year) },
        }"
      >
        <img
          :src="getfileUrl(album.coverPath)"
          :class="albums.length > 1 ? 'cover-img' : 'cover-img single-img'"
          width="1000"
          height="1000"
        />
      </router-link>
    </div>
  </div>
</template>
