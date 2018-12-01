import Vue from 'vue';
import Vuex from 'vuex';
import session from './modules/session';

Vue.use(Vuex);

const store = new Vuex.Store({
  modules: {session}
});

export default store;

if (process.env.NODE_ENV === 'development' && module.hot) {
  module.hot.accept(['./modules/session'], () => {
    const session = require('./modules/session').default;
    store.hotUpdate({modules: {session}});
  })
}
