<template>
  <div id="app">
    <nav-bar/>
    <router-view/>
  </div>
</template>

<script>
  import NavBar from '@/components/NavBar';

  export default {
    name: 'App',
    components: {
      NavBar,
    },
  };
</script>

<style lang="scss">
  @import './styles/_variables.scss';
  @import '../node_modules/bootstrap/scss/bootstrap.scss';
  @import './styles/_bootswatch.scss';
</style>
