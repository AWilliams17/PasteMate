<template>
  <b-row>
    <b-container>
      <div class="alert alert-dismissible alert-dark" v-if="errors">
        <strong v-if="misc_error">Unaccounted for error occurred: {{ misc_error }}</strong>
        <div v-else>
          <div v-for="(value, key) in errors" :key="key">
            <strong>{{ key[0].toUpperCase() + key.slice(1) }}:</strong> {{ value[0] }}
          </div>
        </div>
      </div>
    </b-container>
    <b-col cols="12">
      <b-card header="Sign up to PasteMate" class="mb-3 mx-auto" style="max-width: 25rem;">
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
          <b-button  type="submit" variant="primary" size="sm" class="float-right">Sign up</b-button>
        </b-form>
      </b-card>
    </b-col>
  </b-row>
</template>

<script>
  import axios from 'axios';

  export default {
    name: 'account-sign-up',
    data() {
      return {
        form: {
          username: '',
          email: '',
          password: ''
        },
        misc_error: null,
        errors: null
      };
    },
    methods: {
      signUp(payload) {
        const signUpPath = this.$root.getApiUrlFor('/api/user/register');
        axios.post(signUpPath, payload, {withCredentials: true})
          .then((response) => {
            if (!response.data.success) {
              this.errors = response.data.errors;
            } else {
              console.log(response.data);
              console.log(response.headers);
              this.$eventHub.$emit('status-update');
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
      }
    }
  };
</script>

<style scoped>
</style>
