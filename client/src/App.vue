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

  export default {
    name: 'App',
    components: {
      NotificationContainer,
      NavHeader,
      NavSide,
      SiteFooter
    },
    created() {
      // this.getAuthStatus();
    }
  }
</script>

<style lang="scss">
  @import "./assets/sass/black-dashboard.scss";
  @import "./assets/sass/overrides.scss";
  @import "./assets/css/nucleo_icons.css";
</style>
