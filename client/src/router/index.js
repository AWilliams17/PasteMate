import Vue from 'vue';
import Router from 'vue-router';
import Index from '@/components/Index';
import AccountSignUp from '@/components/accounts/AccountSignUp';

Vue.use(Router);

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Index',
      component: Index,
    },
    {
      path: '/sign_up',
      name: 'SignUp',
      component: AccountSignUp,
    },
  ],
  mode: 'history',
});
