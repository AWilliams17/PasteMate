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
              <b-badge v-if="paste.expiration_date !== null" variant="danger">Expiration Date: {{paste.expiration_date}}</b-badge>
              <b-badge v-if="paste.edit_date !== null" variant="light">Last Edit: {{paste.edit_date}}</b-badge>
              <b-badge variant="warning">Open Edit: {{paste.open_edit ? 'Yes' : 'No'}}</b-badge>
              <b-badge variant="dark">Language: {{paste.language}}</b-badge>
            </div>
          </div>
          <div class="card-body">
            <pre v-highlightjs="paste.content">
              <code id="code_container"></code>
            </pre>
          </div>
          <div class="card-footer">
            <div class="float-right">
              <b-button v-if="this.$store.getters['user/username'] === paste.owner_name || paste.open_edit"
                        type="submit"
                        variant="warning"
                        size="sm">Edit
              </b-button>
              <b-button v-if="this.$store.getters['user/username'] === paste.owner_name"
                        type="submit"
                        variant="danger"
                        size="sm">Delete
              </b-button>
            </div>
          </div>
        </div>
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
          title: '',
          language: '',
          content: '',
          submission_date: '',
          edit_date: '',
          expiration_date: '',
          open_edit: '',
          owner_name: ''
        },
        show_password_form: false,
        password: '',
        information_alert_msg: 'Getting paste, please wait...'
      }
    },
    methods: {
      getPaste() {
        axios.get(this.path)
          .then((response) => {
            this.paste = response.data.paste;
            this.initHighlighting();
          })
          .catch((error) => {
            if (error.response.status === 401) {
              this.show_password_form = true;
            } else {
              this.information_alert_msg = 'Error: ' + error.response.data.error_message;
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
            this.initHighlighting();
          })
          .catch((error) => {
            console.log(error.response);
            this.information_alert_msg = 'Error: ' + error.response;
          })
      },
      initHighlighting() {
        let CodeContainer = document.getElementById('code_container');
        let CodeLines = CodeContainer.getElementsByTagName('span');
        console.log(CodeLines);
        let language = this.paste.language.toLowerCase();
        if (language === 'none') {
          language = 'nohighlight'
        }
        CodeContainer.className += ' ' + this.paste.language.toLowerCase();
        for (let i = 0; i < CodeLines.length; i++) {
          CodeLines[i].className += 'code-line';
        }
        console.log(this.$parent.hljs);
      }
    },
    created() {
      this.getPaste();
    }
  };
</script>

<style>
  pre {
    counter-reset: line;
  }

  code span {
    counter-increment: line;
  }

  code span::before {
    content: counter(line);
    display: inline-block;
    width: 1.5em; /* Fixed width */
    border-right: 1px solid #28283b;
    padding: 0 .5em;
    margin-right: .5em;
    color: #888;
    -webkit-user-select: none;
  }
</style>
