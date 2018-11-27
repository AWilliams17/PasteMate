import Vue from 'vue';
import Router from 'vue-router';
import Index from '@/components/Index';
import AccountSignUp from '@/components/accounts/AccountSignUp';
import AccountSignIn from '@/components/accounts/AccountSignIn';
import AccountPasswordReset from '@/components/accounts/AccountPasswordReset';
import AccountSignOut from '@/components/accounts/AccountSignOut';
import AccountManage from '@/components/accounts/AccountManage';
import PasteEdit from '@/components/pastes/PasteEdit';
import PasteSubmit from '@/components/pastes/PasteSubmit';
import PasteView from '@/components/pastes/PasteView';
import PasteList from '@/components/pastes/PasteList';
import NotFound from '@/components/404';

Vue.use(Router);

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Index',
      component: Index
    },
    {
      path: '/account/signup',
      name: 'Sign Up',
      component: AccountSignUp
    },
    {
      path: '/account/signin',
      name: 'Sign In',
      component: AccountSignIn
    },
    {
      path: '/account/signout',
      name: 'Sign Out',
      component: AccountSignOut
    },
    {
      path: '/account/manage',
      name: 'Manage Account',
      component: AccountManage,
      meta: {
        requiresAuth: true
      }
    },
    {
      path: '/account/passwordreset',
      name: 'Reset Password',
      component: AccountPasswordReset,
      meta: {
        requiresAuth: true
      }
    },
    {
      path: '/paste/submit',
      name: 'Submit Paste',
      component: PasteSubmit,
      meta: {
        requiresAuth: true
      }
    },
    {
      path: '/paste/edit',
      name: 'Edit Paste',
      component: PasteEdit,
      meta: {
        requiresAuth: true
      }
    },
    {
      path: '/paste/view/:slug',
      name: 'View Paste',
      component: PasteView
    },
    {
      path: '/paste/list',
      name: 'Submitted Pastes',
      component: PasteList,
      meta: {
        requiresAuth: true
      }
    },
    { path: '*', redirect: '/404' },
    {
      path: '/404',
      name: '404 Not Found',
      component: NotFound
    }
  ],
  mode: 'history'
});
