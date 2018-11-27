// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import BootstrapVue from 'bootstrap-vue';
import VueHighlightJS from 'vue-highlightjs'
import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap-vue/dist/bootstrap-vue.css';
import Vue from 'vue';
import VueCookies from 'vue-cookies';
import VueResource from 'vue-resource';
import App from './App';
import router from './router';
import store from './_store/store';

Vue.use(BootstrapVue);
Vue.use(VueHighlightJS);
Vue.use(VueCookies);
Vue.use(VueResource);
Vue.config.productionTip = false;

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  store,
  components: { App },
  template: '<App/>'
});

router.beforeEach((to, from, next) => {
  // Redirect user to sign in page if trying to access a protected route.
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth);
  const currentUser = store.getters['user/userID'];
  if (requiresAuth && !currentUser) {
    next('/account/signin');
  } else {
    next();
  }
});
