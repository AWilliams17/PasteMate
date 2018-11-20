import axios from 'axios'

export default {
  namespaced: true,

  // TODO: UserID
  state: {
    userID: null,
    username: null
  },

  actions: {
    signUp(context, payload) {
      return new Promise((resolve, reject) => {
        axios.post('/api/user/register', payload, {withCredentials: true})
          .then((response) => {
            context.commit('UPDATE_USER', [response.data.username, response.data.userID]);
            resolve(response);
          })
          .catch((error) => {
            reject(error);
          });
      })
    },

    signIn(context, payload) {

    },

    signOut(context, payload) {

    },

    updateUser(context) {
      const csrfAccessTokenExists = this.$cookies.get('csrf_access_token');
      if (csrfAccessTokenExists) {
        axios.get('/api/auth/status', {withCredentials: true})
          .then((response) => {
            context.commit('UPDATE_USER', response.data.username);
          })
          .catch((error) => {
            if (error.status) { // Make sure it isn't a network error before trying to re-authenticate
              context.dispatch('attemptReAuthentication');
            }
          })
      } else {
        context.commit('UPDATE_USER', null);
      }
    },

    attemptReAuthentication(context) {
      axios.get('/api/auth/refresh', {withCredentials: true})
        .then((response) => {
          context.commit('UPDATE_USER', response.data.username);
        })
        .catch((error) => {
          if (error.status) {
            // this.$notificationHub.$emit('signout_notice', 'You are no longer authenticated.');
            // TODO: Dispatch an error notification
          }
        })
    }
  },

  mutations: {
    UPDATE_USER(state, payload) {
      [state.username, state.userID] = [...payload];
    }
  },

  getters: {
    username: state => {
      return state.username;
    }
  }
}
