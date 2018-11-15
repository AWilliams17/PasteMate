<template>
  <div class="sidebar-wrapper">
    <b-nav>
      <div class="logo">
        <a href="javascript:void(0)" class="simple-text logo-normal" style="text-align: center">
          Main Menu
        </a>
      </div>
      <b-nav-item>
        <i class="nc-icon nc-pencil"></i>
        <b-link href="/">New Paste</b-link>
      </b-nav-item>
      <b-nav-item>
        <i class="nc-icon nc-notes"></i>
        <b-link href="/">My Pastes</b-link>
      </b-nav-item>
      <b-nav-item>
        <i class="nc-icon nc-settings-gear-63"></i>
        <b-link href="/">Account Settings</b-link>
      </b-nav-item>
    </b-nav>
  </div>
</template>

<script>
  export default {
    name: 'nav-side'
  };
</script>

<style scoped>
</style>
