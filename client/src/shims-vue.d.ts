/**
 * Ambient module declaration so TypeScript can resolve `*.vue` imports
 * in editors/tools that don't run the Vue (Volar) language plugin.
 * vue-tsc resolves the real SFC types itself and takes precedence.
 */
declare module '*.vue' {
  import type { DefineComponent } from 'vue'
  const component: DefineComponent<object, object, unknown>
  export default component
}
