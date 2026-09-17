<script setup lang="ts">
import { computed } from 'vue'
import { configState } from '../configStore'

/** Port of player_hints_index.html ("name that tune" quick-links). */
const presentYear = computed(() => configState.config?.presentYear ?? new Date().getFullYear())

interface ShuffleLink {
  label: string
  query: Record<string, string>
}

const links = computed<ShuffleLink[]>(() => {
  const py = presentYear.value
  const ret: ShuffleLink[] = [
    {
      label: `name that tune ${py - 75}-${py}`,
      query: { hints: '1', minYear: '1950', maxYear: String(py) },
    },
  ]
  const ranges: [number, number][] = [
    [2010, 2024],
    [2000, 2014],
    [1990, 2004],
    [1980, 1994],
    [1970, 1984],
    [1960, 1974],
  ]
  for (const [minYear, maxYear] of ranges) {
    ret.push({
      label: `name that tune ${minYear}-${maxYear}`,
      query: { hints: '1', minYear: String(minYear), maxYear: String(maxYear) },
    })
  }
  return ret
})

const years = computed(() => {
  const ret: number[] = []
  for (let y = presentYear.value; y >= 1950; y--) ret.push(y)
  return ret
})
</script>

<template>
  <div>
    <table class="w-100">
      <tr v-for="link in links" :key="link.label">
        <td>
          <router-link :to="{ path: '/player', query: link.query }"
            ><i>{{ link.label }}</i></router-link
          >
        </td>
      </tr>
      <tr v-for="year in years" :key="year">
        <td>
          <router-link :to="{ path: '/player', query: { hints: '1', year: String(year) } }"
            ><i>name that tune</i> {{ year }}</router-link
          >
        </td>
      </tr>
    </table>
  </div>
</template>
