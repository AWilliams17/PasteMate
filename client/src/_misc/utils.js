import { ADD_NOTIFICATION } from '../store/action-types';

function dispatchErrors(error, store) {
  const errorList = Object.values(error.response.data.errors);
  console.log('f');
  errorList.forEach((error) => {
    store.dispatch(ADD_NOTIFICATION, ...error);
  })
}

export {
  dispatchErrors
}
