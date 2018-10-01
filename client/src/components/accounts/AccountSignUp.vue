<template>
  <b-container>
    <b-container style="margin-top: 15px;">
      <div class="alert alert-dismissible alert-danger" v-if="error_messages.error">
        <p v-if="error_messages.username"><strong>Error: </strong>{{ error_messages.username }}</p>
        <p v-if="error_messages.email"><strong>Error: </strong>{{ error_messages.email }}</p>
        <p v-if="error_messages.password"><strong>Error: </strong>{{ error_messages.password }}</p>
      </div>
    </b-container>
    <b-card header="Sign up to PasteMate" class="text-white bg-primary mb-3 mx-auto card-padding" style="max-width: 25rem;">
      <b-form @submit="onSubmit">
        <b-form-group id="usernameFieldSet"
            horizontal
            :label-cols="4"
            label="Username"
            label-size="sm"
            label-for="usernameInput" v-bind:class="{ 'label-error-color': error_messages.username }">
          <b-form-input id="usernameInput" size="sm" v-model="form.username" required></b-form-input>
        </b-form-group>
        <b-form-group id="emailFieldSet"
                      horizontal
                      :label-cols="4"
                      label="Email"
                      label-size="sm"
                      label-for="emailInput" v-bind:class="{ 'label-error-color': error_messages.email }"
                      description="If this is not a valid email address you will not be able to reset your password.">
          <b-form-input id="emailInput" type="email" size="sm" v-model="form.email" required></b-form-input>
        </b-form-group>
        <b-form-group id="passwordFieldSet"
                      horizontal
                      :label-cols="4"
                      label="Password"
                      label-size="sm"
                      label-for="passwordInput" v-bind:class="{ 'label-error-color': error_messages.password }">
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
        error_messages: {
          error: false,
          username: '',
          email: '',
          password: '',
        },
        form: {
          username: '',
          email: '',
          password: '',
        },
      };
    },
    methods: {
      signUp(payload) {
        const signUpPath = 'http://127.0.0.1:5000/sign_up';
        axios.post(signUpPath, payload)
          .then(() => {
            // On Success, go and redirect back to home
          })
          // eslint-disable-next-line
          .catch((error) => {
          // On error, display an error flash
        });
      },
      onSubmit(evt) {
        evt.preventDefault();
        // Create a payload using the values from the form, then call signUp()
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
