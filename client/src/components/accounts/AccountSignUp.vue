<template>
  <b-row>
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
        }
      };
    },
    methods: {
      signUp(payload) {
        const signUpPath = this.$root.getApiUrlFor('/api/user/register');
        axios.post(signUpPath, payload, {withCredentials: true})
          .then((response) => {
            if (!response.data.success) {
              this.$notificationHub.emit('notification', response.data.errors);
            } else {
              console.log(response.data);
              console.log(response.headers);
              this.$eventHub.$emit('status-update');
              this.$router.push('/');
            }
          })
          .catch((error) => {
            this.$notificationHub.emit('notification', error.message);
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
