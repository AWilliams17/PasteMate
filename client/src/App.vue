<template>
  <div id="app" class="wrapper">
    <nav-side class="sidebar" data="dark"/>
    <div class="main-panel" data="blue">
      <nav-header/>
      <div class="content">
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
  import axios from 'axios'

  export default {
    name: 'App',
    data() {
      return {
        logged_in: false,
        username: null
      }
    },
    components: {
      NavHeader,
      NavSide,
      SiteFooter
    },
    methods: {
      getAuthStatus() {
        const statusPath = this.$parent.getApiUrlFor('/api/auth/status');
        axios.get(statusPath, {withCredentials: true})
          .then((response) => {
            console.log(response.data);
        })
          .catch((error) => {
            console.log(error.message);
        })
      }
    },
    created() {
      this.getAuthStatus();
      this.$eventHub.$on('status-update', () => {
        this.getAuthStatus()
      })
    }
  }
</script>

<style lang="scss">
  @import "./assets/sass/black-dashboard.scss";
  @import "./assets/sass/overrides.scss";
  @import "./assets/css/nucleo_icons.css";
</style>
