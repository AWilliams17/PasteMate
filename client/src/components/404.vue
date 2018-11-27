<template>
  <b-row>
    <b-col cols="12">
      <b-card header-tag="header">
        <h6 slot="header" class="mb-0">404 - Not found</h6>
        <p class="card-text">The requested route was not found on the server.</p>
      </b-card>
    </b-col>
  </b-row>
</template>

<script>
  export default {
    name: 'NotFound'
  };
</script>

<style scoped>
</style>
