export const SET_AUTH = (state, user) => {
  state.user = user;
};

export const UPDATE_EMAIL = (state, email) => {
  state.user.email = email;
};

export const ADD_NOTIFICATION = (state, message) => {
  state.notifications.push(message);
};

export const CLEAR_NOTIFICATIONS = (state) => {
  state.notifications = [];
};
