import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import err404 from '../components/handlers/404.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/disciplinas',
      name: 'listDisciplinas',
      component: () => import('../views/SportsView.vue')
    },
    {
      path: '/usuario/disciplinas',
      name: 'disciplinas',
      component: () => import('../views/MySportsView.vue')
    },
    {
      path: '/perfil',
      name: 'perfile',
      component: () => import('../views/PerfileView.vue')
    },
    {
      path: '/:pathMatch(.*)',
      component: err404,
    },
    {
      path: '/estadisticas',
      name: 'estadisticas',
      component: () => import('../views/StatsView.vue')
    },
    {
      path: '/disciplinas/inscriptos/:id',
      name: 'sport-signedup',
      component: () => import('../views/SignedView.vue'),
      props: true,
    },
    {
      path: '/usuario/pagos',
      name: 'mis pagos',
      component: () => import('../views/MyPaymentsView.vue')
    },
    {
      path: '/usuario/pagos/new_payment',
      name: 'new-payment',
      component: () => import('../views/MyNewPaymentView.vue')
    },
    {
      path: '/carnet',
      name: 'carnet',
      component: () => import('../views/CarnetView.vue')
    }
  ]
})

export default router
