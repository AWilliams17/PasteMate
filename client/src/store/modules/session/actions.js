import * as auth from '../../../layer/auth'

export const signUp = ({commit}, data) => {
  return auth.signUp(data)
    .then(response => {
      commit('SET_AUTH', response.data)
      return response
    })
}

export const signIn = ({commit}, data) => {
  return auth.login(data)
    .then(response => {
      commit('SET_AUTH', response.data)
      return response
    })
}

export const signOut = ({ commit }) => {
  return auth.signOut().then(response => {
    commit('SET_AUTH', null)
    return response
  })
}

export const refreshToken = ({dispatch}) => {
  return auth.refresh()
    .then(response => {
      dispatch('retrieveUser')
      return response
    })
}

export const retrieveUser = ({ commit }) => {
  return auth.getUser().then(response => {
    commit('SET_AUTH', response.data)
    return response
  })
}
