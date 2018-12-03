/*
  TODO: This is basically meant to entrap any ERRCONNECTIONREFUSED errors or things like them
  so they are handled appropriately and an error message gets displayed to the clinet.
  It's also supposed to automatically check if a token is expired or not on
  requests and then refresh/sign out the user if it fails.
  So all of that needs to be done.
 */
import axios from 'axios';
// import { REFRESH_TOKEN, SET_SIGN_OUT_NOTIFICATION } from '../store/action-types';

axios.defaults.withCredentials = true;
axios.defaults.xsrfHeaderName = 'X-CSRF-TOKEN';
axios.defaults.xsrfCookieName = 'csrf_access_token';

axios.interceptors.response.use(null, error => {
  return Promise.reject(error);
});

export default axios
