<template>
  <div class="card mb-3 mx-auto" style="max-width: 250rem;">
    <div class="card-header text-center">
      <h3 style="margin-bottom: 5px;">Viewing Pastes submitted by {{this.$store.getters['user/username'] }}</h3>
      <v-paginator style="text-align: center" :resource_url="resource_url" :options="options" @update="updateResource"></v-paginator>
    </div>
    <div class="card-body">
      <b-container>
        <b-list-group v-for="paste in pastes" :key="paste.id">
            <b-list-group-item v-bind:to="'/paste/view/' + paste.uuid" class="paste-details-container">
              <b-container>
                <div class="float-left" style="margin-top: 6px">
                  <b-badge variant="primary">Title: {{paste.title}}</b-badge>
                  <b-badge variant="dark">Language: {{paste.language}}</b-badge>
                  <b-badge v-if="paste.expiration_date" variant="danger">Expiration Date: {{paste.expiration_date}}</b-badge>
                  <b-badge v-if="paste.edit_date" variant="light">Last Edit: {{paste.edit_date}}</b-badge>
                  <b-badge variant="warning">Open Edit: {{paste.open_edit ? 'Yes' : 'No'}}</b-badge>
                  <b-badge variant="info">Password: {{paste.password_protected ? 'Yes' : 'No'}}</b-badge>
                </div>
                <div class="float-right">
                  <b-button v-bind:to="'/paste/edit/' + paste.uuid" variant="warning" size="sm">Edit</b-button>
                  <b-button v-bind:to="'/paste/delete/' + paste.uuid" variant="danger" size="sm">Delete</b-button>
                </div>
              </b-container>
            </b-list-group-item>
        </b-list-group>
      </b-container>
    </div>
  </div>
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
</script>

<style scoped>
  .list-group-item {
    margin-bottom: 15px;
    background-color: #2f3148;;
    border-color: #1a1b27b8;
  }
  .paste-details-container {
    padding-top: 5px;
    padding-bottom: 5px;
  }
</style>
