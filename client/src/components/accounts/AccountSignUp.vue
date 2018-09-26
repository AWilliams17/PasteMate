<template>
  <b-container>
    <b-card header="Sign up to PasteMate" class="text-white bg-primary mb-3 mx-auto card-padding" style="max-width: 25rem;">
      <b-form>
        <b-form-group id="usernameFieldSet"
            horizontal
            :label-cols="4"
            label="Username"
            label-size="sm"
            label-for="usernameInput">
          <b-form-input id="usernameInput" size="sm"></b-form-input>
        </b-form-group>
        <b-form-group id="emailFieldSet"
                      horizontal
                      :label-cols="4"
                      label="Email"
                      label-size="sm"
                      label-for="emailInput">
          <b-form-input id="emailInput" type="email" size="sm"></b-form-input>
        </b-form-group>
        <b-form-group id="passwordFieldSet"
                      horizontal
                      :label-cols="4"
                      label="Password"
                      label-size="sm"
                      label-for="passwordInput">
          <b-form-input id="passwordInput" type="password" size="sm"></b-form-input>
        </b-form-group>
        <b-form-checkbox id="accountPrivateCheckbox" size="sm">Private Account</b-form-checkbox>
        <b-button type="submit" variant="primary" size="sm" class="float-right">Sign up</b-button>
      </b-form>
    </b-card>
  </b-container>
</template>

<script>
  export default {
    name: 'AccountSignUp',
  };
</script>

<style scoped>
  .card-padding {
    margin-top: 25px;
  }
</style>
