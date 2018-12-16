/*
  TODO: This is basically meant to entrap any ERRCONNECTIONREFUSED errors or things like them
  so they are handled appropriately and an error message gets displayed to the clinet.
  It's also supposed to automatically check if a token is expired or not on
  requests and then refresh/sign out the user if it fails.
  So all of that needs to be done.
 */
import axios from 'axios';
import router from '../router'
import store from '../store';
import { dictContainsAnyOf } from './utils';
import { REFRESH_TOKEN, ADD_NOTIFICATION, RETRIEVE_USER } from '../store/action-types';

axios.defaults.withCredentials = true;
axios.defaults.xsrfHeaderName = 'X-CSRF-TOKEN';
axios.defaults.xsrfCookieName = 'csrf_access_token';

axios.interceptors.response.use(null, error => {
  const ErrorDict = error.response.data;
  const ErrorCode = error.response.status;

  if (ErrorCode === 404) {
    router.replace('/404');
  } else if (ErrorCode === 401) {
    if (dictContainsAnyOf(['token_unauthorized', 'token_revoked', 'token_invalid'], ErrorDict)) {
      router.replace('/account/signin');
    } else if (dictContainsAnyOf(['token_old', 'token_expired'], ErrorDict)) {
      store.dispatch(RETRIEVE_USER).catch(() => {
        store.dispatch(REFRESH_TOKEN)
          .catch(() => {
            store.dispatch(ADD_NOTIFICATION, 'Your session has expired. Please sign back in.');
            router.replace('/account/signin');
          })
      })
    } else {
      // TODO: Finish this up.
      return Promise.reject(error);
    }
  }
});

export default axios
