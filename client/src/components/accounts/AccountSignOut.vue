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
    created() {
      const AccessToken = localStorage.getItem('access_token');
      const RefreshToken = localStorage.getItem('refresh_token');
      if (AccessToken !== null || RefreshToken !== null) {
        if (AccessToken !== null) {
          axios.get('http://127.0.0.1:5000/invalidate_access', {headers: { Authorization: 'Bearer ' + AccessToken}});
        }
        if (RefreshToken !== null) {
          axios.get('http://127.0.0.1:5000/invalidate_refresh', {headers: { Authorization: 'Bearer ' + RefreshToken}});
        }
        localStorage.clear();
        this.$eventHub.$emit('logged-out');
        this.message = 'You have been logged out.';
      } else {
        this.message = 'You are not logged in!';
      }
    },
  };
</script>
