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
      <template v-else-if="paste !== null">
        <p>{{paste.title}}</p>
        <p>{{paste.language}}</p>
        <p>{{paste.expiration_date}}</p>
        <p>{{paste.submission_date}}</p>
        <p>{{paste.edit_date}}</p>
      </template>
      <template v-else>
        <b-alert show variant="dark">
          <div>
            <strong>{{information_alert_msg}}</strong>
          </div>
        </b-alert>
      </template>
    </b-col>
  </b-row>
</template>

<script>
  import axios from 'axios';

  export default {
    name: 'paste-view',
    data() {
      return {
        path: '/api/paste/view/' + this.$route.params.slug,
        paste: null,
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
          })
          .catch((error) => {
            console.log(error.response);
            this.information_alert_msg = 'Error: ' + error.response;
          })
      }

    },
    created() {
      this.getPaste();
    }
  };
</script>
