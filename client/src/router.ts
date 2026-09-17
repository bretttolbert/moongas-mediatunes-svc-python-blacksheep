import { createRouter, createWebHistory } from 'vue-router'

const AlbumsIndexView = () => import('./views/AlbumsIndexView.vue')
const AlbumsView = () => import('./views/AlbumsView.vue')
const ArtistsIndexView = () => import('./views/ArtistsIndexView.vue')
const ArtistsView = () => import('./views/ArtistsView.vue')
const ArtistView = () => import('./views/ArtistView.vue')
const ArtistGeoCodesView = () => import('./views/ArtistGeoCodesView.vue')
const GenresIndexView = () => import('./views/GenresIndexView.vue')
const GenresView = () => import('./views/GenresView.vue')
const GenreView = () => import('./views/GenreView.vue')
const TracksIndexView = () => import('./views/TracksIndexView.vue')
const TracksView = () => import('./views/TracksView.vue')
const PlayerIndexView = () => import('./views/PlayerIndexView.vue')
const PlayerView = () => import('./views/PlayerView.vue')
const NameThatTuneIndexView = () => import('./views/NameThatTuneIndexView.vue')
const WordCloudView = () => import('./views/WordCloudView.vue')

/**
 * Paths mirror the original Flask routes (app/main/routes.py) so existing
 * links/bookmarks keep working. Filter state lives in the query string,
 * exactly as before.
 *
 * Route meta:
 * - bare: no header/footer (word clouds)
 * - noYears: header without the year prev/next nav (player, tracks)
 */
export const router = createRouter({
  history: createWebHistory('/'),
  routes: [
    { path: '/', name: 'root', component: AlbumsIndexView },
    { path: '/albums', name: 'albums', component: AlbumsView },
    { path: '/albums/index', name: 'albums-index', component: AlbumsIndexView },
    { path: '/tracks', name: 'tracks', component: TracksView, meta: { noYears: true } },
    { path: '/tracks/index', name: 'tracks-index', component: TracksIndexView },
    { path: '/artists', name: 'artists', component: ArtistsView },
    { path: '/artists/index', name: 'artists-index', component: ArtistsIndexView },
    { path: '/artist', name: 'artist', component: ArtistView },
    { path: '/genres', name: 'genres', component: GenresView },
    { path: '/genres/index', name: 'genres-index', component: GenresIndexView },
    { path: '/genre', name: 'genre', component: GenreView },
    {
      path: '/artist-countries',
      name: 'artist-countries',
      component: ArtistGeoCodesView,
      meta: { geoKind: 'countries' },
    },
    {
      path: '/artist-regions',
      name: 'artist-regions',
      component: ArtistGeoCodesView,
      meta: { geoKind: 'regions' },
    },
    {
      path: '/artist-cities',
      name: 'artist-cities',
      component: ArtistGeoCodesView,
      meta: { geoKind: 'cities' },
    },
    {
      path: '/artist-languages',
      name: 'artist-languages',
      component: ArtistGeoCodesView,
      meta: { geoKind: 'languages' },
    },
    { path: '/player', name: 'player', component: PlayerView, meta: { noYears: true } },
    { path: '/player/index', name: 'player-index', component: PlayerIndexView },
    {
      path: '/name-that-tune/index',
      name: 'name-that-tune-index',
      component: NameThatTuneIndexView,
    },
    {
      path: '/genres-cloud',
      name: 'genres-cloud',
      component: WordCloudView,
      meta: { bare: true, cloudType: 'genre' },
    },
    {
      path: '/artists-cloud',
      name: 'artists-cloud',
      component: WordCloudView,
      meta: { bare: true, cloudType: 'artist' },
    },
  ],
})
