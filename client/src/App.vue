<template>
  <div id="app" class="wrapper">
    <nav-side class="sidebar" data="dark"/>
    <div class="main-panel" data="blue">
      <nav-header/>
      <div class="content">
        <notification-container/>
        <router-view :key="$route.fullPath"/>
      </div>
      <site-footer class="footer"/>
    </div>
  </div>
</template>

<script>
  import NavHeader from './components/navbar/Header'
  import NavSide from './components/navbar/Side'
  import SiteFooter from './components/Footer';
  import NotificationContainer from './components/NotificationContainer';
  import { RETRIEVE_USER, REFRESH_TOKEN, SET_SIGN_OUT_NOTIFICATION } from './store/action-types';

  export default {
    name: 'App',
    components: {
      NotificationContainer,
      NavHeader,
      NavSide,
      SiteFooter
    },

    created() {
      // Refresh user tokens if necessary on re-visit.
      if (this.$cookies.get('csrf_access_token')) {
        this.$store.dispatch(RETRIEVE_USER).catch(() => {
          this.$store.dispatch(REFRESH_TOKEN)
            .catch(() => {
              this.$store.dispatch(SET_SIGN_OUT_NOTIFICATION, 'You have been signed out.');
            })
        })
      }
    }
  }
</script>

<style lang="scss">
  @import "./assets/sass/black-dashboard.scss";
  @import "./assets/sass/overrides.scss";
  @import "./assets/css/nucleo_icons.css";
</style>
