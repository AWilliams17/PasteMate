<template>
  <b-row>
    <b-col cols="12">
      <b-card header="Sign in to PasteMate" class="mb-3 mx-auto" style="max-width: 25rem;">
        <b-form @submit.prevent="onSubmit">
          <b-form-group id="usernameFieldSet"
                        horizontal
                        :label-cols="4"
                        label="Username"
                        label-size="sm">
            <b-form-input id="usernameInput" size="sm" v-model="form.username" maxlength="12" required></b-form-input>
          </b-form-group>
          <b-form-group id="passwordFieldSet"
                        horizontal
                        :label-cols="4"
                        label="Password"
                        label-size="sm">
            <b-form-input id="passwordInput" type="password" size="sm" maxlength="128" v-model="form.password" required></b-form-input>
          </b-form-group>
          <b-button type="submit" variant="primary" size="sm" class="float-right">Sign in</b-button>
        </b-form>
      </b-card>
    </b-col>
  </b-row>
</template>

<script>
import { SIGN_IN, ADD_NOTIFICATION } from '../../store/action-types';

export default {
  name: 'account-sign-in',
  data() {
    return {
      form: {
        username: '',
        password: ''
      }
    };
  },
  methods: {
    async onSubmit() {
      try {
        const payload = this.form;
        await this.$store.dispatch(SIGN_IN, payload);
        this.$router.push('/');
      } catch (error) {
        const errorList = Object.values(error.response.data.errors);
        errorList.forEach((error) => {
          this.$store.dispatch(ADD_NOTIFICATION, error);
        })
      }
    }
  }
}
</script>
