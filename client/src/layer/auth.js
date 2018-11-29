import axios from 'axios'

export const login = (data) => {
  return axios.post('/api/user/login', data, {withCredentials: true})
}

export const signUp = (data) => {
  return axios.post('/api/user/register', data)
}

export const signOut = (data) => {
  return axios.get('/api/auth/revoke', {withCredentials: true})
}

export const refresh = () => {
  return axios.get('/api/auth/refresh', {withCredentials: true})
}

export const getUser = () => {
  return axios.get('/api/auth/current_user', {withCredentials: true})
}
