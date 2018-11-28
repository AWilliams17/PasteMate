<template>
  <b-row>
    <b-col cols="12">
      <template v-if="show_password_form">
        <b-card header="Password Required" class="mb-3 mx-auto" style="max-width: 25rem;">
          <b-form @submit="submitPassword">
            <b-form-group id="passwordFieldSet"
                          horizontal
                          :label-cols="4"
                          label="Paste Password"
                          label-size="sm">
              <b-form-input id="passwordInput" size="sm" v-model="password" required></b-form-input>
            </b-form-group>
            <b-button type="submit" variant="primary" size="sm" class="float-right">Submit</b-button>
          </b-form>
        </b-card>
      </template>
      <template v-else>
        <div class="card mb-3 mx-auto" style="max-width: 250rem;">
          <div class="card-header">
            <div>
              <b-badge variant="primary">Title: {{paste.title}}</b-badge>
              <b-badge variant="info">Submitted: {{paste.submission_date}}</b-badge>
              <b-badge v-if="paste.expiration_date" variant="danger">Expiration Date: {{paste.expiration_date}}</b-badge>
              <b-badge v-if="paste.edit_date" variant="light">Last Edit: {{paste.edit_date}}</b-badge>
              <b-badge variant="warning">Open Edit: {{paste.open_edit ? 'Yes' : 'No'}}</b-badge>
              <b-badge variant="dark">Language: {{paste.language}}</b-badge>
            </div>
          </div>
          <div class="card-body">
            <div id="code-container">
              <pre v-highlightjs v-for="line in paste.content" :key="line.id">
                <code v-bind:class="paste.language.toLowerCase()">{{line}}</code>
              </pre>
            </div>
          </div>
          <div class="card-footer">
            <div class="float-right">
              <b-button v-if="this.$store.getters['user/username'] === paste.owner_name || paste.open_edit"
                        type="submit"
                        variant="warning"
                        size="sm"
                        v-bind:to="'/paste/edit/' + this.$route.params.slug">Edit
              </b-button>
              <b-button v-if="this.$store.getters['user/username'] === paste.owner_name"
                        type="submit"
                        variant="danger"
                        size="sm"
                        @click="deletePaste">Delete
              </b-button>
            </div>
          </div>
        </div>
      </template>
      <template v-if="paste.deletion_inbound">
        <b-alert variant="warning" show>
          This paste has reached its expiration date and will be deleted shortly.
        </b-alert>
      </template>
    </b-col>
  </b-row>
</template>

<script>
  import axios from 'axios';
  import 'highlight.js/styles/ocean.css';

  export default {
    name: 'paste-view',
    data() {
      return {
        path: '/api/paste/view/' + this.$route.params.slug,
        paste: {
          has_paste: false,
          title: '',
          language: '',
          content: '',
          submission_date: '',
          edit_date: '',
          expiration_date: '',
          open_edit: '',
          owner_name: '',
          deletion_inbound: false
        },
        show_password_form: false,
        password: ''
      }
    },
    methods: {
      getPaste() {
        axios.get(this.path)
          .then((response) => {
            this.paste = response.data.paste;
            console.log(this.paste.edit_date);
          })
          .catch((error) => {
            if (error.response.status === 401) {
              this.show_password_form = true;
            } else if (error.response.status === 404) {
              this.$router.push('/404');
            } else {
              this.$store.dispatch('notification/addNotification', 'Error: ' + error.response.data.error);
            }
          })
      },
      submitPassword(evt) {
        evt.preventDefault();
        axios.post(this.path, {'password': this.password})
          .then((response) => {
            this.show_password_form = false;
            this.password = null;
            this.paste = response.data.paste;
          })
          .catch((error) => {
            this.$store.dispatch('notification/addNotification', 'Error: ' + error.response.data.error);
          })
      },
      deletePaste() {
        const pasteUUID = this.$route.params.slug;
        axios.get('/api/paste/delete/' + pasteUUID, {withCredentials: true})
          .then(() => {
            this.$store.dispatch('notification/addNotification', 'Paste was successfully deleted.');
            this.$router.push('/')
          })
          .catch((error) => {
            this.$store.dispatch('notification/addNotification', 'Error: ' + error);
          });
      }
    },
    created() {
      this.getPaste();
    }
  };
</script>

<style>
  #code-container {
    counter-reset: line;
    max-height: 500px;
    overflow: auto;
  }
  pre {
    margin: 0;
    padding: 0;
    display: grid;
  }
  code {
    counter-increment: line;
    padding-top: 0!important;
    padding-bottom: 0!important;
    background-color: #2b305a!important;
  }
  code::before {
    content: counter(line);
    display: inline-block;
    width: 3.5em;
    border-right: 1px solid #28283b;
    padding: 0 .10em;
    margin-right: .5em;
    color: #888;
    -webkit-user-select: none;
  }
</style>
