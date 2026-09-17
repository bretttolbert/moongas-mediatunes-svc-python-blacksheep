<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import type { TrackInfo } from '../types'

/**
 * TypeScript/Vue port of hints.js + hints.html ("name that tune" mode).
 */
const props = defineProps<{
  track: TrackInfo | null
}>()

const emit = defineEmits<{
  reveal: []
}>()

const showYear = ref(false)
const showFirstLetter = ref(false)
const showSecondLetter = ref(false)
/** Once details are shown, hints are locked (matches hideAndLockHints()). */
const revealed = ref(false)

/** resetHints() from hints.js */
function reset(): void {
  showYear.value = false
  showFirstLetter.value = false
  showSecondLetter.value = false
  revealed.value = false
}

defineExpose({ reset })

watch(() => props.track, reset)

function revealAll(): void {
  revealed.value = true
  showYear.value = false
  showFirstLetter.value = false
  showSecondLetter.value = false
  emit('reveal')
}

const firstLetter = computed(() => props.track?.artist?.[0] ?? '')
const secondLetter = computed(() =>
  props.track && props.track.artist.length > 1 ? props.track.artist[1] : '(no second letter)',
)
</script>

<template>
  <div>
    Hints:
    <input type="checkbox" class="hintChk" id="hintYearChk" v-model="showYear" :disabled="revealed" />
    <label for="hintYearChk">Year</label>
    <input
      type="checkbox"
      class="hintChk"
      id="hintArtist1stLetterChk"
      v-model="showFirstLetter"
      :disabled="revealed"
    />
    <label for="hintArtist1stLetterChk">Artist 1st Letter</label>
    <input
      type="checkbox"
      class="hintChk"
      id="hintArtist2ndLetterChk"
      v-model="showSecondLetter"
      :disabled="revealed"
    />
    <label for="hintArtist2ndLetterChk">Artist 2nd Letter</label>
    <button id="showBtn" class="btn btn-secondary btn-lg" :disabled="revealed" @click="revealAll">
      Show Details <i class="bi bi-puzzle-fill"></i>
    </button>
    <div id="hintYear" class="hint" v-show="showYear && !revealed">
      Year: {{ track?.year }}
    </div>
    <div id="hintArtist1stLetter" class="hint" v-show="showFirstLetter && !revealed">
      Artist 1st Letter: {{ firstLetter }}
    </div>
    <div id="hintArtist2ndLetter" class="hint" v-show="showSecondLetter && !revealed">
      Artist 2nd Letter: {{ secondLetter }}
    </div>
  </div>
</template>
