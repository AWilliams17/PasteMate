import Vue from 'vue';
import Router from 'vue-router';
import Index from '@/components/Index';
import AccountSignUp from '@/components/accounts/AccountSignUp';
import AccountSignIn from '@/components/accounts/AccountSignIn';

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
    {
      path: '/sign_in',
      name: 'SignIn',
      component: AccountSignIn,
    },
  ],
  mode: 'history',
});
