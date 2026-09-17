<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { queryList } from '../utils/queryParams'

/** Port of genre.html (single genre hub page). */
const route = useRoute()
const genreLabel = computed(() => queryList(route.query, 'genre').join(','))
</script>

<template>
  <div class="genre">
    <table class="genre">
      <tr>
        <th>{{ genreLabel }}</th>
      </tr>
      <tr>
        <td>
          <router-link class="button-link" :to="{ path: '/albums', query: route.query }"
            >albums</router-link
          >
        </td>
      </tr>
      <tr>
        <td>
          <router-link class="button-link" :to="{ path: '/artists', query: route.query }"
            >artists</router-link
          >
        </td>
      </tr>
      <tr>
        <td>
          <router-link class="button-link" :to="{ path: '/tracks', query: route.query }"
            >tracks</router-link
          >
        </td>
      </tr>
      <tr>
        <td>
          <router-link class="button-link" :to="{ path: '/player', query: route.query }"
            >shuffle</router-link
          >
        </td>
      </tr>
    </table>
  </div>
</template>
