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
            <b-form-input id="usernameInput" size="sm" v-model="form.username" required maxlength="12"></b-form-input>
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
            <b-form-input id="passwordInput" type="password" size="sm" maxlength="128" v-model="form.password" required></b-form-input>
          </b-form-group>
          <b-button type="submit" variant="primary" size="sm" class="float-right">Sign up</b-button>
        </b-form>
      </b-card>
    </b-col>
  </b-row>
</template>

<script>
  import {SIGN_UP, ADD_NOTIFICATION} from '../../store/action-types';

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
      onSubmit(evt) {
        evt.preventDefault();
        const payload = this.form;
        this.$store.dispatch(SIGN_UP, payload).then(() => {
          this.$router.push('/');
        }).catch((error) => {
          const errorList = Object.values(error.response.data.errors);
          errorList.forEach((error) => {
            this.$store.dispatch(ADD_NOTIFICATION, 'Error: ' + error);
          });
        })
      }
    }
  };
</script>
