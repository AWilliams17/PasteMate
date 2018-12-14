<template>
  <b-row>
    <b-col cols="12">
      <b-card header="Sign in to PasteMate" class="mb-3 mx-auto" style="max-width: 25rem;">
        <b-form @submit.prevent="onSubmit">
          <b-form-group id="emailFieldSet"
                        horizontal
                        :label-cols="4"
                        label="Email"
                        label-size="sm">
            <b-form-input id="emailInput" size="sm" v-model="email" maxlength="64" required></b-form-input>
          </b-form-group>
          <b-button type="submit" variant="primary" size="sm" class="float-right">Send Reset Link</b-button>
        </b-form>
      </b-card>
    </b-col>
  </b-row>
</template>

<script>
  import { ADD_NOTIFICATION } from '../../store/action-types';
  import axiosJWT from '../../_misc/axios_jwt';

  export default {
    name: 'account-password-reset',
    data() {
      return {
        'email': ''
      }
    },
    methods: {
      onSubmit() {
        const payload = {'email': this.email};
        axiosJWT.post('/api/user/reset_password', payload)
          .then((response) => {
            this.$store.dispatch(ADD_NOTIFICATION, response.data.success);
            this.$router.push('/');
          })
          .catch((error) => {
            const errorList = Object.values(error.response.data.errors);
            errorList.forEach((error) => {
              this.$store.dispatch(ADD_NOTIFICATION, ...error);
            });
          })
      }
    }
  };
</script>
