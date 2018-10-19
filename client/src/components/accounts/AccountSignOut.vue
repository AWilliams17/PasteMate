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
          axios.get('http://127.0.0.1:5000/invalidate_access', {headers: { Authorization: 'Bearer ' + AccessToken}});
          return true;
        }
        return false;
      },
      invalidateRefreshToken(RefreshToken) {
        if (RefreshToken !== null) {
          axios.get('http://127.0.0.1:5000/invalidate_refresh', {headers: { Authorization: 'Bearer ' + RefreshToken}});
          return true;
        }
        return false;
      },
      invalidateTokensAndClearStorage(AccessToken, RefreshToken) {
        const accessRevoked = this.invalidateAccessToken(AccessToken);
        const refreshRevoked = this.invalidateRefreshToken(RefreshToken);
        if (accessRevoked || refreshRevoked) {
          localStorage.clear();
          return true;
        }
        return false;
      },
    },
    created() {
      const AccessToken = localStorage.getItem('access_token');
      const RefreshToken = localStorage.getItem('refresh_token');
      const InvalidationResult = this.invalidateTokensAndClearStorage(AccessToken, RefreshToken);
      if (InvalidationResult) {
        this.message = 'You have been logged out.';
      } else {
        this.message = 'You are not logged in!';
      }
    },
  };
</script>
