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
  @import './styles/variables.scss';
  @import '../node_modules/bootstrap/scss/bootstrap.scss';
  @import './styles/bootswatch.scss';
</style>
