<template>
  <div>
    <b-navbar type="dark" toggleable="md" class="bg-primary navbar-expand-lg">
      <b-navbar-brand href="#">PasteMate</b-navbar-brand>
      <b-navbar-nav>
        <b-nav-item-dropdown text="Account" x-placement="bottom-start">
          <template v-if="1 == 0"> <!-- ToDo: If user is signed in -->
            <b-dropdown-item href="/sign_out">Sign out</b-dropdown-item>
            <b-dropdown-item href="/account_settings">Account Settings</b-dropdown-item>
          </template>
          <template v-else>
            <b-dropdown-item href="/sign_in">Sign in</b-dropdown-item>
            <b-dropdown-item href="/sign_up">Sign up</b-dropdown-item>
            <b-dropdown-item href="/reset_password">Reset Password</b-dropdown-item>
          </template>
        </b-nav-item-dropdown>
        <template v-if="1 == 0"> <!-- ToDo: If user is signed in -->
          <b-nav-item-dropdown text="Paste" x-placement="bottom-start">
            <b-dropdown-item href="/submit">Submit</b-dropdown-item>
            <b-dropdown-item href="/pastes">My Pastes</b-dropdown-item>
          </b-nav-item-dropdown>
        </template>
      </b-navbar-nav>
    </b-navbar>
  </div>
</template>

<script>
  export default {
    name: 'nav-bar',
    methods: {
      showSignUpModal: function showSignUpModal() {
        this.$emit('showSignUp');
      },
    },
  };
</script>
