import axios from 'axios'

export default {
  namespaced: true,

  state: {
    user: {
      username: null,
      authorized: false
    }
  },

  actions: {
    signUp(context, payload) {
      axios.post('/api/user/register', payload, {withCredentials: true})
        .then((response) => {
          if (!response.data.success) {
            // this.$notificationHub.emit('notification', response.data.errors);
            // TODO: Dispatch an error notification
          } else {
            context.commit('UPDATE_USER', payload);
          }
        })
        /* eslint-disable handle-callback-err */
        .catch((error) => {
          // this.$notificationHub.emit('notification', error.message);
          // TODO: Dispatch an error notification
        });
    },

    signIn(context, payload) {

    },

    signOut(context, payload) {

    },

    retrieveUser(context) {
      const csrfAccessTokenExists = this.$cookies.get('csrf_access_token');
      if (csrfAccessTokenExists) {
        axios.get('/api/auth/status', {withCredentials: true})
          .then((response) => {
            context.commit('_UPDATE_USER', [response.data.username, true]);
          })
          .catch((error) => {
            if (error.status) { // Make sure it isn't a network error before trying to re-authenticate
              context.commit('_UPDATE_USER', [this.state.user.username, false]);
              context.dispatch('attemptReAuthentication');
            }
          })
      } else {
        context.commit('_UPDATE_USER', [null, false]);
      }
    },

    attemptReAuthentication(context) {
      axios.get('/api/auth/refresh', {withCredentials: true})
        .then((response) => {
          context.commit('_UPDATE_USER', [response.data.username, true]);
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
      state.user = {...payload};
    }
  }
}
