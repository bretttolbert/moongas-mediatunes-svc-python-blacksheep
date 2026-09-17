<script setup lang="ts">
/** Port of genres_index.html. */
</script>

<template>
  <div>
    <table class="w-100">
      <tr>
        <td>
          <router-link :to="{ path: '/genres', query: { sort: 'count' } }"
            >genres (sorted by count)</router-link
          >
        </td>
      </tr>
      <tr>
        <td>
          <router-link :to="{ path: '/genres', query: { sort: 'name' } }"
            >genres (sorted by name)</router-link
          >
        </td>
      </tr>
      <tr>
        <td><router-link to="/genres-cloud">genres word cloud</router-link></td>
      </tr>
    </table>
  </div>
</template>
