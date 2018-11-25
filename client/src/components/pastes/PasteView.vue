<template>
  <p></p>
</template>

<script>
  import axios from 'axios';

  export default {
    name: 'paste-view',
    data() {

    },
    methods: {
      getPaste() {
        axios.get('/api/paste/submit')
      }
    },
    created() {
      this.getPaste();
    }
  };
</script>
