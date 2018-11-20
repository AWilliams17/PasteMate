// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import BootstrapVue from 'bootstrap-vue';
import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap-vue/dist/bootstrap-vue.css';
import Vue from 'vue';
import VueCookies from 'vue-cookies';
import App from './App';
import router from './router';
import store from './_store/store';

Vue.use(BootstrapVue);
Vue.use(VueCookies);
Vue.config.productionTip = false;
Vue.prototype.$eventHub = new Vue(); // Global event bus
Vue.prototype.$notificationHub = new Vue(); // Global error bus

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  store,
  components: { App },
  template: '<App/>'
});

// router.beforeEach((to, from, next) => {
  // TODO: Make this redirect them to an access denied if authorization is required
  // TODO: Also, redirect them from the login/register page if they are already logged in.
// });
