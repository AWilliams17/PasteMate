<template>
</template>

<script>
  import VuePaginator from 'vuejs-paginator';

  export default {
    name: 'paste-list',
    data() {
      return {
        pastes: [],
        resource_url: '/api/paste/list/' + this.$route.params.slug,
        options: {
          remote_data: 'pastes.data',
          remote_current_page: 'pastes.current_page',
          remote_last_page: 'pastes.last_page',
          remote_next_page_url: 'pastes.next_page_url',
          remote_prev_page_url: 'pastes.prev_page_url',
          next_button_text: 'Next',
          previous_button_text: 'Prev'
        }
      }
    },
    components: {
      VPaginator: VuePaginator
    },
    methods: {
      updateResource(data) {
        this.pastes = data;
        console.log(this.pastes)
      }
    }
  };
  // <v-paginator :resource_url="resource_url" :options="options" @update="updateResource"></v-paginator>
</script>
