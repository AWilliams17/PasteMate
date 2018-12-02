<template>
  <b-row>
    <b-col cols="12">
      <b-card header="Account Management Options" class="mb-3 mx-auto" style="max-width: 35rem;">
        <b-form @submit="onSubmit">
          <b-form-group id="usernameFieldSet"
                        horizontal
                        :label-cols="4"
                        label="Your Username"
                        label-size="sm">
            <b-form-input id="usernameInput"
                          :value="username"
                          size="sm"
                          :readonly="true"
                          maxlength="12">
            </b-form-input>
          </b-form-group>
          <b-form-group id="emailFieldSet"
                        horizontal
                        :label-cols="4"
                        label="New Email"
                        label-size="sm">
            <b-form-input id="emailInput"
                          size="sm"
                          v-model="form.email"
                          :placeholder="email"
                          required>
            </b-form-input>
          </b-form-group>
          <b-form-group id="passwordFieldSet"
                        horizontal
                        :label-cols="4"
                        label="New Password"
                        description="Your current password is hidden for security reasons."
                        label-size="sm">
            <b-form-input id="passwordInput" type="password" size="sm" v-model="form.password" maxlength="128" required></b-form-input>
          </b-form-group>
          <b-button type="submit" variant="primary" size="sm" class="float-right">Submit</b-button>
        </b-form>
      </b-card>
    </b-col>
  </b-row>
</template>

<script>
  export default {
    name: 'account-manage',
    data() {
      return {
        form: {
          'email': null,
          'password': null
        }
      }
    },
    computed: {
      user() {
        let user = this.$store.getters['session/user'];
        if (user) {
          return user;
        }
        return null;
      },
      username() {
        if (this.user) {
          return this.user.username;
        }
        return '';
      },
      email() {
        if (this.user) {
          return this.user.email;
        }
        return '';
      }
    },
    methods: {
      onSubmit(evt) {
        evt.preventDefault();
      }
    }
  };
</script>
