<template>
  <div>
    <b-navbar type="dark" toggleable="md" class="bg-primary navbar-expand-lg">
      <b-navbar-brand><b-link to="/">PasteMate</b-link></b-navbar-brand>
      <b-navbar-nav>
        <b-nav-item-dropdown text="Account" x-placement="bottom-start">
          <template v-if="user"> <!-- ToDo: If user is signed in -->
            <b-dropdown-item><b-link to="/sign_out">Sign out</b-link></b-dropdown-item>
            <b-dropdown-item><b-link to="/account_settings">Account Settings</b-link></b-dropdown-item>
          </template>
          <template v-else>
            <b-dropdown-item><b-link to="/sign_in">Sign in</b-link></b-dropdown-item>
            <b-dropdown-item><b-link to="/sign_up">Sign up</b-link></b-dropdown-item>
            <b-dropdown-item><b-link to="/reset_password">Reset Password</b-link></b-dropdown-item>
          </template>
        </b-nav-item-dropdown>
        <template v-if="user"> <!-- ToDo: If user is signed in -->
          <b-nav-item-dropdown text="Paste" x-placement="bottom-start">
            <b-dropdown-item><b-link to="/submit">Submit Paste</b-link></b-dropdown-item>
            <b-dropdown-item><b-link to="/pastes">My Pastes</b-link></b-dropdown-item>
          </b-nav-item-dropdown>
        </template>
      </b-navbar-nav>
    </b-navbar>
  </div>
</template>

<script>
  export default {
    name: 'nav-bar',
    data() {
      return {
        user: null,
      };
    },
    created() {
      this.$eventHub.$on('logged-in', () => {
        this.$parent.getCurrentUser().then((response) => {
          if (response.data !== null) {
            this.user = response.data;
          } else {
            this.user = null;
          }
        });
      });
      this.$eventHub.$on('logged-out', () => {
        this.user = null;
      });
    },
  };
</script>

<style scoped>
  a:hover {
    text-decoration: None;
    color: #fff;
  }
</style>
