<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import { configState } from '../configStore'

/** Port of the inline script in age_verification.html. */
const confirmed = ref(localStorage.getItem('ageConfirmed') === 'true')
const enabled = computed(() => configState.config?.ageVerification ?? false)
const visible = computed(() => enabled.value && !confirmed.value)

watch(
  visible,
  (v) => {
    document.body.classList.toggle('age-verification-active', v)
  },
  { immediate: true },
)

function yes(): void {
  localStorage.setItem('ageConfirmed', 'true')
  confirmed.value = true
}

function no(): void {
  // Redirect if they are not old enough
  window.location.href = 'https://www.google.com'
}
</script>

<template>
  <!-- v-if controls presence, so display:flex inline (CSS has display:none by default,
       which the original inline script overrode via element.style) -->
  <div v-if="visible" id="age-verification-overlay" style="display: flex">
    <div id="age-verification-modal">
      <h1>Content Warning</h1>
      <p>This website contains content intended for mature audiences only (18+).</p>
      <p>Are you 18 years or older?</p>
      <button id="age-yes" @click="yes">Yes, I am 18+</button>
      <button id="age-no" @click="no">No, exit</button>
    </div>
  </div>
</template>
