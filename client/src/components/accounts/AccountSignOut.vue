<template>
  <b-container>
    <b-container style="margin-top: 15px;">
      <div class="alert alert-dismissible alert-info">
        <strong>{{ message }}</strong>
      </div>
    </b-container>
  </b-container>
</template>

<script>
  import axios from 'axios';

  export default {
    name: 'AccountSignOut',
    data() {
      return {
        message: 'Logging out...',
      };
    },
    methods: {
      invalidateAccessToken(AccessToken) {
        if (AccessToken !== null) {
          return axios.get('http://127.0.0.1:5000/invalidate_access', {headers: { Authorization: 'Bearer ' + AccessToken}});
        }
        return null;
      },
      invalidateRefreshToken(RefreshToken) {
        if (RefreshToken !== null) {
          return axios.get('http://127.0.0.1:5000/invalidate_refresh', {headers: { Authorization: 'Bearer ' + RefreshToken}});
        }
        return null;
      },
      invalidateTokens(AccessToken, RefreshToken) {
        const accessRevoked = this.invalidateAccessToken(AccessToken);
        const refreshRevoked = this.invalidateRefreshToken(RefreshToken);
        if (accessRevoked !== null || refreshRevoked !== null) {
          const tokenPromises = [];
          if (accessRevoked !== null) {
            tokenPromises.append(accessRevoked);
          }
          if (refreshRevoked !== null) {
            tokenPromises.append(refreshRevoked);
          }
          return tokenPromises;
        }
        return null;
      },
    },
    created() {
      const AccessToken = this.$cookie.get('access_token');
      const RefreshToken = this.$cookie.get('refresh_token');
      if (AccessToken !== null || RefreshToken !== null) {
        const invalidateTokensPromises = this.invalidateTokens(AccessToken, RefreshToken);
        Promise.all(invalidateTokensPromises).then((values) => {
          if (values.includes(false)) {
            this.message = 'Failed to sign out.';
          } else {
            this.$cookie.remove('access_token');
            this.$cookie.remove('refresh_token');
            this.$eventHub.$emit('signed-out');
            this.message = 'You have been signed out.';
          }
        });
      } else {
        this.message = 'You are not signed in!';
      }
    },
  };
</script>
