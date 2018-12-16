import { ADD_NOTIFICATION } from '../store/action-types';

function dispatchErrors(error, store) {
  const errorList = Object.values(error.response.data.errors);
  errorList.forEach((error) => {
    store.dispatch(ADD_NOTIFICATION, ...error);
  })
}

function dictContainsAnyOf(keys, dict) { // checks if any of the keys in the keys list are a key in the dictionary.
  return keys.some(prop => dict[prop]) // since 'if x in y || z in y || a in y' etc is annoying.
}

export {
  dispatchErrors,
  dictContainsAnyOf
}
