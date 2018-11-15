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
        logged_in: false
      }
    },
    components: {
      NavHeader,
      NavSide,
      SiteFooter
    },
    methods: {
      getApiUrlFor(TargetRoute) {
        const apiLink = this.$parent.$apiRoot;
        const apiLinkIsInvalid = apiLink.endsWith('/');
        const targetRoute = TargetRoute;
        const targetRouteIsInvalid = !targetRoute.startsWith('/');

        if (apiLinkIsInvalid) {
          throw new Error('API Url must not end with a forward slash.')
        } else if (targetRouteIsInvalid) {
          throw new Error('Target route must start with a forward slash.')
        } else {
          return apiLink.concat(targetRoute)
        }
      },
      getAuthStatus() {
        const statusPath = this.getApiUrlFor('/auth/status/');
        axios.get(statusPath, {withCredentials: true}).then((response) => {
          if (response.status === 401) {
            // Now, try to re-authenticate the user with a refresh function
            // If that fails, ask them to re-authenticate.
          } else if (response.status === 200) {
            // Success
          } else {
            // Tell them it failed to get their status
          }
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
</style>
