<template>
  <b-row>
    <b-col cols="12">
      <b-card header="Reset Password" class="mb-3 mx-auto" style="max-width: 25rem;">
        <template v-if="show_reset_form">
          <b-form @submit.prevent="onSubmitPassword">
            <b-form-group id="passwordFieldSet"
                          horizontal
                          :label-cols="4"
                          label="New Password"
                          label-size="sm">
              <b-form-input id="passwordInput" size="sm" type="password" v-model="password" maxlength="256" required></b-form-input>
            </b-form-group>
            <b-button type="submit" variant="primary" size="sm" class="float-right">Update Password</b-button>
          </b-form>
        </template>
        <template v-else>
          <b-form @submit.prevent="onSubmitEmail">
            <b-form-group id="emailFieldSet"
                          horizontal
                          :label-cols="4"
                          label="Email"
                          label-size="sm">
              <b-form-input id="emailInput" size="sm" type="email" v-model="email" maxlength="64" required></b-form-input>
            </b-form-group>
            <b-button type="submit" variant="primary" size="sm" class="float-right">Send Reset Link</b-button>
          </b-form>
        </template>
      </b-card>
    </b-col>
  </b-row>
</template>

<script>
  import { ADD_NOTIFICATION } from '../../store/action-types';
  import axiosJWT from '../../_misc/axios_jwt';
  import { dispatchErrors } from '../../_misc/utils';

  export default {
    name: 'account-password-reset',
    data() {
      return {
        email: '',
        password: '',
        token: null
      }
    },
    mounted() {
      this.token = this.$route.params.slug;
    },
    computed: {
      show_reset_form() {
        return this.token;
      }
    },
    methods: {
      onSubmitEmail() {
        const payload = {'email': this.email};

        axiosJWT.post('/api/user/reset_password', payload)
          .then((response) => {
            this.$store.dispatch(ADD_NOTIFICATION, response.data.success);
            this.$router.push('/');
          })
          .catch((error) => {
            dispatchErrors(error, this.$store);
          })
      },

      onSubmitPassword() {
        const payload = {'token': this.token, 'password': this.password};

        axiosJWT.post('/api/user/reset_password_finalize', payload)
          .then((response) => {
            this.$store.dispatch(ADD_NOTIFICATION, response.data.success);
            this.$router.push('/account/signin');
          })
          .catch((error) => {
            dispatchErrors(error, this.$store);
          })
      }
    }
  };
</script>
