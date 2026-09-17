<script setup lang="ts">
import { computed } from 'vue'
import { GENRE_MIXES } from '../data/genreMixes'

/** Port of x_by_genre.html / x_by_genre_tr.html. */
const props = defineProps<{
  indexType: 'albums' | 'artists'
}>()

const heading = computed(() => `${props.indexType[0].toUpperCase()}${props.indexType.slice(1)}`)
</script>

<template>
  <table class="w-100">
    <tr>
      <th>{{ heading }} by genre(s)</th>
    </tr>
    <tr v-for="mix in GENRE_MIXES" :key="mix.genres.join('|')">
      <td>
        <router-link :to="{ path: `/${indexType}`, query: { genre: mix.genres } }">
          {{ indexType }} {{ mix.genres.join(', ') }}
        </router-link>
      </td>
    </tr>
  </table>
</template>
