<template>
  <b-container>
    <b-container style="margin-top: 15px;">
      <div class="alert alert-dismissible alert-danger" v-if="errors">
        <strong v-if="misc_error">Unaccounted for error occurred: {{ misc_error }}</strong>
        <div v-else>
          <div v-for="(value, key) in errors" :key="key">
            <strong>{{ key[0].toUpperCase() + key.slice(1) }}:</strong> {{ value[0] }}
          </div>
        </div>
      </div>
    </b-container>
    <b-card header="Sign up to PasteMate" class="text-white bg-primary mb-3 mx-auto card-padding" style="max-width: 25rem;">
      <b-form @submit="onSubmit">
        <b-form-group id="usernameFieldSet"
            horizontal
            :label-cols="4"
            label="Username"
            label-size="sm">
          <b-form-input id="usernameInput" size="sm" v-model="form.username" required></b-form-input>
        </b-form-group>
        <b-form-group id="emailFieldSet"
                      horizontal
                      :label-cols="4"
                      label="Email"
                      label-size="sm"
                      description="If this is not a valid email address you will not be able to reset your password.">
          <b-form-input id="emailInput" type="email" size="sm" v-model="form.email" required></b-form-input>
        </b-form-group>
        <b-form-group id="passwordFieldSet"
                      horizontal
                      :label-cols="4"
                      label="Password"
                      label-size="sm">
          <b-form-input id="passwordInput" type="password" size="sm" v-model="form.password" required></b-form-input>
        </b-form-group>
        <b-button type="submit" variant="primary" size="sm" class="float-right">Sign up</b-button>
      </b-form>
    </b-card>
  </b-container>
</template>

<script>
  import axios from 'axios';

  export default {
    name: 'AccountSignUp',
    data() {
      return {
        form: {
          username: '',
          email: '',
          password: '',
        },
        misc_error: null,
        errors: null,
      };
    },
    methods: {
      signUp(payload) {
        const signUpPath = 'http://127.0.0.1:5000/sign_up';
        axios.post(signUpPath, payload)
          .then((response) => {
            if (!response.data.success) {
              this.errors = response.data.errors;
            } else {
              localStorage.setItem('access_token', response.data.access_token);
              localStorage.setItem('refresh_token', response.data.access_token);
              this.$eventHub.$emit('user-event');
              this.$router.push('/');
            }
          })
          .catch((error) => {
            this.misc_error = error.message;
        });
      },
      onSubmit(evt) {
        evt.preventDefault();
        const payload = this.form;
        this.signUp(payload);
      },
    },
  };
</script>

<style scoped>
  .card-padding {
    margin-top: 25px;
  }
  p {
    margin-bottom: 2px;
  }
  .label-error-color {
    color: #d71c1c;
  }
</style>
