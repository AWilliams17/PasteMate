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
      if (this.$parent.logged_in) {
        const revokeAccessPath = this.$parent.getApiUrlFor('/auth/revoke/');
        axios.get(revokeAccessPath, {withCredentials: true}).then((response) => {
          this.logged_in = response;
          this.$eventHub.$emit('status-update');
          this.message = 'You have been logged out.';
        });
      } else {
        this.message = 'You are not logged in!';
      }
    },
  };
</script>
