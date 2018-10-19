<template>
  <div id="app">
    <nav-bar/>
    <router-view/>
  </div>
</template>

<script>
  import NavBar from '@/components/NavBar';
  import axios from 'axios';

  export default {
    name: 'App',
    components: {
      NavBar,
    },
    methods: {
      getCurrentUser() {
        const bearer = localStorage.getItem('access_token');
        if (bearer !== null) {
          return axios.get('http://127.0.0.1:5000/current_user', {headers: { Authorization: 'Bearer ' + bearer}});
        }
        return null;
      },
    },
  };
</script>

<style lang="scss">
  @import './styles/_variables.scss';
  @import '../node_modules/bootstrap/scss/bootstrap.scss';
  @import './styles/_bootswatch.scss';
</style>
