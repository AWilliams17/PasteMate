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
            context.commit('UPDATE_USER', [null, null]);
            reject(error);
          });
      })
    },

    signIn(context, payload) {

    },

    signOut(context, payload) {

    },

    authenticateUser(context) {
      return new Promise((resolve, reject) => {
        axios.get('/api/auth/refresh', {withCredentials: true})
          .then((response) => {
            context.commit('UPDATE_USER', [response.data.username, response.data.userID]);
            resolve(response);
          })
          .catch((error) => {
            context.commit('UPDATE_USER', [null, null]);
            reject(error);
          });
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
    },

    userID: state => {
      return state.userID;
    }
  }
}
