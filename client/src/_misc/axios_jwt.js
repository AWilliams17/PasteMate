import axios from 'axios';
// import { REFRESH_TOKEN, SET_SIGN_OUT_NOTIFICATION } from '../store/action-types';

const AxiosJWT = axios.create({
  withCredentials: true,
  headers: {
    xsrfHeaderName: 'X-CSRF-TOKEN',
    xsrfCookieName: 'csrf_access_token'
  }
});

AxiosJWT.interceptors.response.use(null, error => {
  console.log(error);
  return Promise.reject(error);
});

export default AxiosJWT
