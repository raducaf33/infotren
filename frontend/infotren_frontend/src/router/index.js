import { createRouter, createWebHistory } from 'vue-router'
import BuyTicket from '../views/BuyTicket.vue'
import Login from '../views/Login.vue'
import SignUp from '../views/SignUp.vue'
import UserProfile from '../views/UserProfile.vue'
import Contact from '../views/Contact.vue'
import AdminDashboard from '../views/AdminDashboard.vue'



const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: BuyTicket
    },
    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/About.vue')
    },
    {
      path: '/contact',
      name: 'contact',
      component: Contact
    },

    {
      path: '/login',
      name: 'login',
      component: Login
    },
    {
      path: '/signup',
      name: 'signup',
      component: SignUp
    },

    {
      path:'/user-profile',
      name: 'userprofile',
      component: UserProfile
    },

    { 
      path: '/admin-dashboard', 
      component: AdminDashboard, 
      name: 'AdminDashboard',
      meta: { requiresAdmin: true },
    },




  
  ]
})

// Navigation guard
router.beforeEach((to, from, next) => {
  const isAdmin = localStorage.getItem('is_admin') === 'true';
  const isLoggedIn = !!localStorage.getItem('access_token');

  if (to.meta.requiresAdmin && (!isLoggedIn || !isAdmin)) {
    next('/login'); // Redirecționează utilizatorii non-admin la login
  } else {
    next(); // Permite accesul
  }
});

export default router
