import Vue from 'vue';
import Router from 'vue-router';
import index from '@/components/Index';

Vue.use(Router);

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Index',
      component: index,
    },
  ],
});
