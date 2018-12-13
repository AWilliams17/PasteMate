import axiosJWT from '../_misc/axios_jwt';

export const login = (data) => {
  return axiosJWT.post('/api/user/login', data)
};

export const signUp = (data) => {
  return axiosJWT.post('/api/user/register', data)
};

export const signOut = () => {
  return axiosJWT.get('/api/auth/revoke')
};

export const refresh = () => {
  return axiosJWT.get('/api/auth/refresh')
};

export const getUser = () => {
  return axiosJWT.get('/api/auth/current_user')
};

export const updatePassword = (data) => {
  return axiosJWT.post('/api/user/update_password', data)
};

export const updateEmail = (data) => {
  return axiosJWT.post('/api/user/update_email', data)
};
