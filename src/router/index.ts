import { createRouter, createWebHistory } from 'vue-router'
import GameView from '@/views/GameView.vue'
import ShopView from '@/views/ShopView.vue'
import InvestmentView from '@/views/InvestmentView.vue'
import RankingView from '@/views/RankingView.vue'
import ProfileView from '@/views/ProfileView.vue'
import DailyView from '@/views/DailyView.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'game',
      component: GameView,
      meta: { title: 'Quantum Nexus' }
    },
    {
      path: '/shop',
      name: 'shop',
      component: ShopView,
      meta: { title: 'Quantum Shop' }
    },
    {
      path: '/investment',
      name: 'investment',
      component: InvestmentView,
      meta: { title: 'Quantum Investments' }
    },
    {
      path: '/ranking',
      name: 'ranking',
      component: RankingView,
      meta: { title: 'Quantum Rankings' }
    },
    {
      path: '/profile',
      name: 'profile',
      component: ProfileView,
      meta: { title: 'Quantum Profile' }
    },
    {
      path: '/daily',
      name: 'daily',
      component: DailyView,
      meta: { title: 'Daily Quantum' }
    }
  ]
})

export default router