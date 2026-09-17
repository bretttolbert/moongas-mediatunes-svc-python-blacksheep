<script setup lang="ts">
import { computed } from 'vue'
import { useRoute, type LocationQueryRaw } from 'vue-router'
import { configState } from '../configStore'

const route = useRoute()

interface NavLink {
  label: string
  path: string
  italic?: boolean
  /** Hide this link when the current path is one of these (mirrors header_impl_links.html). */
  hiddenOn: string[]
  /** Only shown when local playback is enabled. */
  localOnly?: boolean
}

const links: NavLink[] = [
  { label: 'albums', path: '/albums/index', hiddenOn: ['/albums/index', '/albums'] },
  { label: 'artists', path: '/artists/index', hiddenOn: ['/artists/index', '/artists'] },
  { label: 'genres', path: '/genres/index', hiddenOn: ['/genres/index', '/genres'] },
  { label: 'player', path: '/player/index', hiddenOn: ['/player/index', '/player'] },
  {
    label: 'name that tune',
    path: '/name-that-tune/index',
    italic: true,
    localOnly: true,
    hiddenOn: ['/name-that-tune/index'],
  },
  { label: 'tracks', path: '/tracks/index', hiddenOn: ['/tracks/index', '/tracks'] },
]

const localEnabled = computed(() => configState.config?.playbackMethodLocalEnabled ?? false)

const visibleLinks = computed(() =>
  links.filter((l) => !l.hiddenOn.includes(route.path) && (!l.localOnly || localEnabled.value)),
)

/** Open nav links in a new tab when on the player, to avoid disrupting playback. */
const linkTarget = computed(() => (route.path === '/player' ? '_blank' : undefined))

/** Year prev/next nav (header_impl_years.html); suppressed on routes with meta.noYears. */
const year = computed<number | null>(() => {
  if (route.meta.noYears === true) return null
  const raw = route.query.year
  const n = Number(Array.isArray(raw) ? raw[0] : raw)
  return Number.isFinite(n) && n > 0 ? n : null
})

function yearQuery(y: number): LocationQueryRaw {
  return { ...route.query, year: String(y) }
}
</script>

<template>
  <header>
    <div id="header">
      <table class="no-border w-100">
        <tr>
          <td v-for="link in visibleLinks" :key="link.path">
            <router-link :to="link.path" :target="linkTarget">
              <i v-if="link.italic">{{ link.label }}</i>
              <template v-else>{{ link.label }}</template>
            </router-link>
          </td>
          <template v-if="year !== null">
            <td>
              <router-link :to="{ path: route.path, query: yearQuery(year - 1) }">{{ year - 1 }}</router-link>
            </td>
            <td>
              <b>
                <router-link :to="{ path: route.path, query: yearQuery(year) }">{{ year }} </router-link>
              </b>
            </td>
            <td>
              <router-link :to="{ path: route.path, query: yearQuery(year + 1) }">{{ year + 1 }}</router-link>
            </td>
          </template>
        </tr>
      </table>
    </div>
  </header>
</template>
