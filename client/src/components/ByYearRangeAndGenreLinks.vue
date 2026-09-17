<script setup lang="ts">
import { computed } from 'vue'
import type { LocationQueryRaw } from 'vue-router'
import { getYearRangeGenreMixes, type YearRangeGenreMix } from '../data/genreMixes'
import { configState } from '../configStore'

/** Port of x_by_year_range_and_genre.html / x_by_year_range_and_genre_tr.html. */
const props = defineProps<{
  indexType: 'albums' | 'artists'
}>()

const heading = computed(() => `${props.indexType[0].toUpperCase()}${props.indexType.slice(1)}`)

const presentYear = computed(
  () => configState.config?.presentYear ?? new Date().getFullYear(),
)

const mixes = computed(() => getYearRangeGenreMixes(presentYear.value))

function linkQuery(mix: YearRangeGenreMix): LocationQueryRaw {
  if (mix.genreOnly) {
    return { genre: mix.genres }
  }
  return { minYear: String(mix.minYear), maxYear: String(mix.maxYear), genre: mix.genres }
}

function linkLabel(mix: YearRangeGenreMix): string {
  if (mix.genreOnly) {
    return `${props.indexType} ${mix.genres.join(', ')}`
  }
  return `${props.indexType} ${mix.minYear}-${mix.maxYear} ${mix.genres.join(', ')}`
}
</script>

<template>
  <table class="w-100">
    <tr>
      <th>{{ heading }} by year range and genre(s)</th>
    </tr>
    <tr v-for="mix in mixes" :key="`${mix.minYear}-${mix.maxYear}-${mix.genres.join('|')}`">
      <td>
        <router-link :to="{ path: `/${indexType}`, query: linkQuery(mix) }">
          {{ linkLabel(mix) }}
        </router-link>
      </td>
    </tr>
  </table>
</template>
