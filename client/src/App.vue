<template>
  <div id="app">
    <router-view/>
  </div>
</template>

<script>
  export default {
    name: 'App',
  };
</script>

<style lang="scss">
  @import './styles/_variables.scss';
  @import '../node_modules/bootstrap/scss/bootstrap.scss';
  @import './styles/_bootswatch.scss';
</style>
