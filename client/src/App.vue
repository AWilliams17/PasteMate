<template>
  <div id="app">
    <nav-bar/>
    <router-view/>
  </div>
</template>

<script>
  import NavBar from '@/components/NavBar'
  import axios from 'axios'

  export default {
    name: 'App',
    data() {
      return {
        logged_in: false
      }
    },
    components: {
      NavBar
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

<style>
  @import '../static/css/style.red.css';
  @import '../static/css/font.css';
  @import '../static/css/custom.css';
</style>
