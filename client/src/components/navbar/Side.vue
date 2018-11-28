<template>
  <div class="sidebar-wrapper">
    <b-nav>
      <div class="logo">
        <a href="javascript:void(0)" class="simple-text logo-normal" style="text-align: center">
          Main Menu
        </a>
      </div>
      <b-link to="/paste/submit" class="nav-link" router-link="li">
        <i class="nc-icon nc-pencil"></i>
        <p>Submit Paste</p>
      </b-link>
      <b-link to="/paste/list/1" class="nav-link" router-link="li">
        <i class="nc-icon nc-notes"></i>
        <p>My Pastes</p>
      </b-link>
      <!--
      <b-link to="/account/manage" class="nav-link" router-link="li">
        <i class="nc-icon nc-settings-gear-63"></i>
        <p>Manage Account</p>
      </b-link>
      -->
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
