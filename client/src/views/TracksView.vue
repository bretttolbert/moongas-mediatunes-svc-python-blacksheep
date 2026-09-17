<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import { useRoute, type LocationQueryRaw } from 'vue-router'
import { api, getfileUrl } from '../api'
import { configState } from '../configStore'
import { formatResults } from '../utils/format'
import { queryList, queryScalar } from '../utils/queryParams'
import type { MediaFile } from '../types'

/** Port of tracks.html (track listing table). */
const route = useRoute()

const files = ref<MediaFile[]>([])
const coverPath = ref('')
const loading = ref(false)
const error = ref<string | null>(null)

async function load(): Promise<void> {
  loading.value = true
  error.value = null
  try {
    const data = await api.tracks(route.query)
    files.value = data.files
    coverPath.value = data.coverPath
  } catch (e) {
    error.value = e instanceof Error ? e.message : String(e)
    files.value = []
    coverPath.value = ''
  } finally {
    loading.value = false
  }
}

watch(() => route.query, load, { immediate: true })

const albumParam = computed(() => queryList(route.query, 'album'))
const albumArtistParam = computed(() => queryScalar(route.query, 'albumartist'))
const artistParam = computed(() => queryScalar(route.query, 'artist'))
const maxResults = computed(() => configState.config?.maxResults ?? 50000)

/** "Shuffle Album" link query (uses albumartist when present, else artist). */
const shuffleAlbumQuery = computed<LocationQueryRaw | null>(() => {
  const album = albumParam.value[0]
  if (!album) return null
  if (albumArtistParam.value) return { albumartist: albumArtistParam.value, album }
  if (artistParam.value) return { artist: artistParam.value, album }
  return null
})
</script>

<template>
  <div>
    <div class="results-info">
      {{ formatResults(files.length, maxResults) }}
      <router-link class="button-link" :to="{ path: '/player', query: route.query }"
        >shuffle</router-link
      >:
    </div>
    <div v-if="error" class="error">{{ error }}</div>
    <div v-else-if="loading">loading…</div>
    <template v-else>
      <div v-if="albumParam.length > 0 && coverPath.length > 0">
        <br />
        <img
          :src="getfileUrl(coverPath)"
          id="coverImg"
          class="cover-img single-img"
          width="1000"
          height="1000"
        />
      </div>
      <div v-if="albumParam.length > 0 && shuffleAlbumQuery">
        <router-link class="navLink" :to="{ path: '/player', query: shuffleAlbumQuery }"
          >Shuffle Album <i>{{ albumParam[0] }}</i></router-link
        >
        <br />
      </div>
      <div id="trackList">
        <table class="w-100">
          <tr>
            <th>Year</th>
            <th>Genre</th>
            <th>Artist</th>
            <th>Album</th>
            <th>Title</th>
          </tr>
          <tr v-for="file in files" :key="file.path">
            <td>
              <router-link :to="{ path: '/albums', query: { year: String(file.year) } }">{{
                file.year
              }}</router-link>
            </td>
            <td>
              <router-link :to="{ path: '/artists', query: { genre: file.genre } }">{{
                file.genre
              }}</router-link>
            </td>
            <td>
              <router-link :to="{ path: '/albums', query: { artist: file.artist } }">{{
                file.artist
              }}</router-link>
            </td>
            <td>
              <router-link
                :to="{ path: '/tracks', query: { artist: file.artist, album: file.album } }"
                >{{ file.album }}</router-link
              >
            </td>
            <td>
              <router-link
                :to="{
                  path: '/player',
                  query: { title: file.title, artist: file.artist, album: file.album },
                }"
                >{{ file.title }}</router-link
              >
            </td>
          </tr>
        </table>
      </div>
    </template>
  </div>
</template>
