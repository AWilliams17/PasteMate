<template>
  <b-row>
    <b-col cols="12">
      <b-card :header="header" class="mb-3 mx-auto" style="max-width: 30rem;">
        <strong style="color: #4c7df7">{{ this.body }}</strong>
      </b-card>
    </b-col>
  </b-row>
</template>

<script>
  import { SIGN_OUT } from '../../store/action-types';

  export default {
    name: 'account-sign-out',
    data() {
      return {
        header: 'Signing out',
        body: 'Attempting to sign out, please wait...'
      };
    },
    computed: {
      user() {
        return this.$store.getters['session/user'];
      }
    },
    created() {
      if (this.user) {
        this.$store.dispatch(SIGN_OUT)
          .then(() => {
            [this.header, this.body] = ['Signed out', 'You have been signed out.'];
          })
          .catch((error) => {
            [this.header, this.body] = ['Failed to sign out', 'Error occurred while signing out: ' + error.message];
          })
      } else {
        [this.header, this.body] = ['Not signed in', 'You are not signed in!'];
      }
    }
  };
</script>
