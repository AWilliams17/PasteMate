<template>
  <b-container class="card-padding">
    <b-card header-tag="header">
      <h6 slot="header" class="mb-0">What is this</h6>
      <p class="card-text">This is basically just a PasteBin clone. It has paste expiration from never up to
      a week, and it also has open editing support (anyone can edit the paste), support for
      176 languages, and password protected pastes.</p>
    </b-card>
    <b-card class="card-padding" header-tag="header">
      <h6 slot="header" class="mb-0">Languages supported</h6>
      <p class="card-text">PasteMate uses highlight.js - a list of supported languages
        can be found <a href="https://highlightjs.org/static/demo/">here</a>.
      </p>
    </b-card>
  </b-container>
</template>

<script>
  export default {
    name: 'Index',
  };
</script>

<style scoped>
  .card-padding {
    margin-top: 25px;
  }
</style>
