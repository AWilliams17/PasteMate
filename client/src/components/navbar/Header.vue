<template>
  <b-navbar type="inverse" class="navbar-expand-lg navbar-absolute">
    <b-container fluid>
      <div class="navbar-wrapper">
        <div v-bind:class="{toggled : sideOpen}" class="navbar-toggle d-inline">
          <button v-on:click="openSideBar()" type="button" class="navbar-toggler">
            <span class="navbar-toggler-bar bar1"></span>
            <span class="navbar-toggler-bar bar2"></span>
            <span class="navbar-toggler-bar bar3"></span>
          </button>
        </div>
        <b-navbar-brand href="#">PasteMate</b-navbar-brand>
      </div>
      <b-navbar-nav class="ml-auto">
        <b-nav-item-dropdown right id="dropdown-menu">
          <template slot="button-content">
            <strong>Profile</strong>
          </template>
          <b-dropdown-item href="#">Sign In</b-dropdown-item>
          <b-dropdown-item href="#">Sign Up</b-dropdown-item>
          <b-dropdown-item href="#">Forgot Password</b-dropdown-item>
        </b-nav-item-dropdown>
      </b-navbar-nav>
    </b-container>
  </b-navbar>
</template>

<script>
  export default {
    name: 'nav-header',
    data() {
      return {
        sideOpen: false
      }
    },
    methods: {
      openSideBar() {
        const root = document.getElementsByTagName('html')[0];
        this.sideOpen = !this.sideOpen;
        if (this.sideOpen) {
          root.setAttribute('class', 'nav-open');
        } else {
          root.removeAttribute('class', 'nav-open');
        }
      }
    }
  };
</script>

<style scoped>
</style>
