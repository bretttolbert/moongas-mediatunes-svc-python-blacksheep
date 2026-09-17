<script setup lang="ts">
import { computed, onMounted, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import * as d3 from 'd3'
import cloud from 'd3-cloud'
import { api } from '../api'
import type { WordCloudType } from '../types'

/**
 * Port of word-cloud.html. Uses d3 v7 + d3-cloud from npm instead of the
 * vendored d3.v3.min.js / d3.layout.cloud.js.
 *
 * Rendered bare (no header/footer) like the original page.
 */
const route = useRoute()
const router = useRouter()

const container = ref<HTMLElement | null>(null)
const cloudType = computed(() => (route.meta.cloudType ?? 'genre') as WordCloudType)

const WIDTH = 1920
const HEIGHT = 1080

interface LayoutWord extends cloud.Word {
  text: string
  size: number
}

function fill(i: number): string {
  const m = i % 3
  if (m === 0) return '#1f77b4'
  if (m === 1) return '#aec7e8'
  if (m === 2) return '#ff7f0e'
  return '#ffffff'
}

async function renderCloud(): Promise<void> {
  const data =
    cloudType.value === 'genre'
      ? await api.wordCloudGenres()
      : await api.wordCloudArtists(route.query)

  const words: LayoutWord[] = data.words.map((w) => ({
    text: w.text,
    size: 10 + Math.random() * 90,
  }))

  cloud<LayoutWord>()
    .size([WIDTH, HEIGHT])
    .words(words)
    .padding(5)
    .rotate(() => ~~(Math.random() * 2) * 90)
    .font('Helvetica')
    .fontSize((d) => d.size)
    .on('end', (drawn: LayoutWord[]) => draw(drawn))
    .start()
}

function draw(words: LayoutWord[]): void {
  if (!container.value) return
  const el = container.value
  d3.select(el).select('svg').remove()
  d3.select(el)
    .append('svg')
    .attr('width', WIDTH)
    .attr('height', HEIGHT)
    .append('g')
    .attr('transform', `translate(${WIDTH / 2},${HEIGHT / 2})`)
    .selectAll('text')
    .data(words)
    .enter()
    .append('text')
    .style('font-size', (d) => `${d.size}px`)
    .style('font-family', 'Helvetica')
    .style('fill', (_d, i) => fill(i))
    .attr('text-anchor', 'middle')
    .attr('transform', (d) => `translate(${d.x},${d.y})rotate(${d.rotate})`)
    .text((d) => d.text)
    .on('click', (_event: MouseEvent, d) => {
      const href = router.resolve({
        path: '/albums',
        query: { [cloudType.value]: d.text },
      }).href
      window.open(href, '_blank')
    })
}

onMounted(() => {
  void renderCloud()
})
watch(
  () => route.query,
  () => {
    void renderCloud()
  },
)
</script>

<template>
  <div ref="container" id="container"></div>
</template>
