<template>
  <b-row>
    <b-col cols="12">
      <template v-if="show_password_form">
        <b-card header="Password Required" class="mb-3 mx-auto" style="max-width: 25rem;">
          <b-form @submit.prevent="onSubmitPassword">
            <b-form-group id="passwordFieldSet"
                          horizontal
                          :label-cols="4"
                          label="Paste Password"
                          label-size="sm">
              <b-form-input id="passwordInput" type="password" size="sm" v-model="password" required></b-form-input>
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
              <b-button v-if="current_user_owns_paste || paste.open_edit"
                        type="submit"
                        variant="warning"
                        size="sm"
                        v-bind:to="'/paste/edit/' + this.$route.params.slug">Edit
              </b-button>
              <b-button v-if="current_user_owns_paste"
                        type="submit"
                        variant="danger"
                        size="sm"
                        @click="deletePaste">Delete
              </b-button>
            </div>
          </div>
        </div>
      </template>
    </b-col>
  </b-row>
</template>

<script>
  import axiosJWT from '../../_misc/axios_jwt';
  import { dispatchErrors } from '../../_misc/utils';
  import { ADD_NOTIFICATION } from '../../store/action-types';
  import 'highlight.js/styles/ocean.css';

  export default {
    name: 'paste-view',
    data() {
      return {
        path: '/api/paste/get/' + this.$route.params.slug,
        paste: {
          has_paste: false,
          title: '',
          language: '',
          content: '',
          submission_date: '',
          edit_date: '',
          expiration_date: null,
          open_edit: false,
          owner_name: ''
        },
        show_password_form: false,
        password: null
      }
    },
    computed: {
      username() {
        let user = this.$store.getters['session/user'];
        if (user) {
          return user.username;
        }
        return null;
      },
      current_user_owns_paste() {
         if (this.username) {
           return this.username === this.paste.owner_name;
        }
        return false;
      }
    },
    methods: {
      getPaste() {
        axiosJWT.get(this.path)
          .then((response) => {
            this.paste = response.data.paste;
            this.paste.submission_date = this.dateToLocalTime(this.paste.submission_date);
            if (this.paste.expiration_date) {
              this.paste.expiration_date = this.dateToLocalTime(this.paste.expiration_date);
            }
          })
          .catch((error) => {
            if (error.response.status === 401) {
              this.show_password_form = true;
            } else if (error.response.status === 404) {
              this.$router.push('/404');
            } else {
              dispatchErrors(error, this.$store);
            }
          })
      },
      onSubmitPassword() {
        axiosJWT.post(this.path, {'password': this.password})
          .then((response) => {
            this.show_password_form = false;
            this.password = null;
            this.paste = response.data.paste;
          })
          .catch((error) => {
            dispatchErrors(error, this.$store);
          })
      },
      deletePaste() {
        const pasteUUID = this.$route.params.slug;
        axiosJWT.get('/api/paste/delete/' + pasteUUID, {withCredentials: true})
          .then(() => {
            this.$store.dispatch(ADD_NOTIFICATION, 'Paste was successfully deleted.');
            this.$router.push('/');
          })
          .catch((error) => {
            dispatchErrors(error, this.$store);
          });
      },
      dateToLocalTime(dateStr) {
        let date = new Date(dateStr);
        date.setMinutes(date.getMinutes() - new Date().getTimezoneOffset());
        return date.toLocaleString();
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
