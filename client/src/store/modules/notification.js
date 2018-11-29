export default {
  namespaced: true,

  state: {
    notifications: [],
    sign_out_notification: null // I may want to make it a different message, so I won't use a boolean.
  },

  actions: {
    addNotification(context, payload) {
      context.commit('ADD_NOTIFICATION', payload);
    },

    setSignOutNotification(context, payload) {
      context.commit('SET_SIGN_OUT_NOTIFICATION', payload);
    },

    clearNotifications(context) {
      context.commit('CLEAR_NOTIFICATIONS');
    },

    clearSignOutNotification(context) {
      context.commit('CLEAR_SIGN_OUT_NOTIFICATION');
    }
  },

  mutations: {
    ADD_NOTIFICATION(state, payload) {
      state.notifications.push(payload);
    },

    SET_SIGN_OUT_NOTIFICATION(state, payload) {
      state.sign_out_notification = payload;
    },

    CLEAR_NOTIFICATIONS(state) {
      state.notifications = [];
    },

    CLEAR_SIGN_OUT_NOTIFICATION(state) {
      state.sign_out_notification = null;
    }
  },

  getters: {
    notifications: state => {
      return state.notifications;
    },

    sign_out_notification: state => {
      return state.sign_out_notification;
    }
  }
}
