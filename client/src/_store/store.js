import user from './modules/user';
import notification from './modules/notification';
import Vuex from 'vuex';
import Vue from 'vue';

Vue.use(Vuex);

export default new Vuex.Store({
  modules: {
    user,
    notification
  }
});
