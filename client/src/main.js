// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import BootstrapVue from 'bootstrap-vue';
import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap-vue/dist/bootstrap-vue.css';
import Vue from 'vue';
import App from './App';
import router from './router';

Vue.use(BootstrapVue);
Vue.config.productionTip = false;
Vue.prototype.$eventHub = new Vue(); // Global event bus
Vue.prototype.$apiRoot = 'http://localhost:5000';

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>',
  methods: {
    getApiUrlFor(TargetRoute) {
      const apiLink = this.$apiRoot;
      const apiLinkIsInvalid = apiLink.endsWith('/');
      const targetRoute = TargetRoute;
      const targetRouteIsInvalid = !targetRoute.startsWith('/');

      if (apiLinkIsInvalid) {
        throw new Error('API Url must not end with a forward slash.')
      } else if (targetRouteIsInvalid) {
        throw new Error('Target route must start with a forward slash.')
      } else {
        return apiLink.concat(targetRoute)
      }
    }
  }
});
