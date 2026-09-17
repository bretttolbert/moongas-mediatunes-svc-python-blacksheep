<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import AppHeader from './components/AppHeader.vue'
import AppFooter from './components/AppFooter.vue'
import AgeVerification from './components/AgeVerification.vue'

const route = useRoute()
const bare = computed(() => route.meta.bare === true)
</script>

<template>
  <AgeVerification />
  <template v-if="bare">
    <router-view />
  </template>
  <template v-else>
    <AppHeader />
    <main>
      <router-view />
    </main>
    <AppFooter />
  </template>
</template>
