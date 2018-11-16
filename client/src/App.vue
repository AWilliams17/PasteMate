<template>
  <div id="app" class="wrapper">
    <nav-side class="sidebar" data="dark"/>
    <div class="main-panel" data="blue">
      <nav-header/>
      <div class="content">
        <notification-container/>
        <router-view/>
      </div>
      <site-footer class="footer"/>
    </div>
  </div>
</template>

<script>
  import NavHeader from '@/components/navbar/Header'
  import NavSide from '@/components/navbar/Side'
  import SiteFooter from '@/components/Footer';
  import NotificationContainer from '@/components/NotificationContainer';
  import axios from 'axios'

  export default {
    name: 'App',
    data() {
      return {
        username: null,
        authenticated: false
      }
    },
    components: {
      NotificationContainer,
      NavHeader,
      NavSide,
      SiteFooter
    },
    methods: {
      getAuthStatus() {
        const statusPath = this.$parent.getApiUrlFor('/api/auth/status');
        // If this is their first visit, I don't want a signed out notice appearing, since they
        // never signed in to begin with. There's probably a better way to do this, but this will work for now.
        const csrfAccessTokenExists = this.$cookies.get('csrf_access_token');
        console.log(csrfAccessTokenExists);
        if (csrfAccessTokenExists) {
          axios.get(statusPath, {withCredentials: true})
            .then((response) => {
              this.username = response.data.current_username;
              this.authenticated = true;
            })
            .catch((error) => {
              if (error.status) { // Make sure it isn't a network error before trying to re-authenticate
                this.authenticated = false;
                this.attemptReAuthentication();
              }
            })
        } else {
          this.username = null;
          this.authenticated = false;
        }
      },
      attemptReAuthentication() {
        const refreshPath = this.$parent.getApiUrlFor('/api/auth/refresh');
        axios.get(refreshPath, {withCredentials: true})
          .then((response) => {
            this.username = response.data.current_username;
            this.authenticated = true;
          })
          .catch((error) => {
            if (error.status) {
              this.$notificationHub.$emit('signout_notice', 'You are no longer authenticated.');
            }
          })
      }
    },
    created() {
      this.getAuthStatus();
      this.interval = setInterval(() => this.getAuthStatus(), 10000); // Check auth status every 10 seconds
      this.$eventHub.$on('status-update', () => {
        this.getAuthStatus()
      });
    }
  }
</script>

<style lang="scss">
  @import "./assets/sass/black-dashboard.scss";
  @import "./assets/sass/overrides.scss";
  @import "./assets/css/nucleo_icons.css";
</style>
