export const SET_AUTH = (state, user) => {
  state.user = user
};

export const ADD_NOTIFICATION = (state, message) => {
  state.notifications.push(message);
};

export const SET_SIGN_OUT_NOTIFICATION = (state, message) => {
  state.signOutNotification = message;
};

export const CLEAR_NOTIFICATIONS = (state) => {
  state.notifications = [];
};

export const CLEAR_SIGN_OUT_NOTIFICATION = (state) => {
  state.signOutNotification = null;
};
