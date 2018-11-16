<template>
  <b-row>
    <b-col cols="12">
      <b-card :header="header" class="mb-3 mx-auto" style="max-width: 30rem;">
        <strong style="color: #4c7df7">{{this.body}}</strong>
      </b-card>
    </b-col>
  </b-row>
</template>

<script>
  import axios from 'axios';

  export default {
    name: 'account-sign-out',
    data() {
      return {
        header: 'Signing out',
        body: 'Attempting to sign out, please wait...'
      };
    },
    created() {
      if (this.$parent.username !== null) {
        this.revokeTokens();
      } else {
        this.header = 'Not signed in';
        this.body = 'You are not signed in!';
      }
    },
    methods: {
      revokeTokens() {
        const revokeTokenPath = this.$root.getApiUrlFor('/api/auth/revoke');
        axios.get(revokeTokenPath, {withCredentials: true})
          .then(() => {
            this.header = 'Signed out';
            this.body = 'You have been signed out.';
            this.$eventHub.$emit('status-update');
          })
          .catch((error) => {
            this.header = 'Failed to sign out';
            if (error.status) {
              this.body = 'Failed to sign out: ' + error.message
            } else {
              this.body = 'Network error occurred.';
            }
          })
      }
    }
  };
</script>
