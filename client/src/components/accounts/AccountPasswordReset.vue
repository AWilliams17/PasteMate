<template>
  <b-container>
    <b-card header="Reset Account Password" class="text-white bg-primary mb-3 mx-auto card-padding" style="max-width: 25rem;">
      <b-form>
        <b-form-group id="emailFieldSet"
                      horizontal
                      :label-cols="4"
                      label="Account Email"
                      label-size="sm"
                      label-for="emailInput"
                      description="Enter the email address associated with your account.">
          <b-form-input id="emailInput" size="sm"></b-form-input>
        </b-form-group>
        <b-button type="submit" variant="primary" size="sm" class="float-right">Reset</b-button>
      </b-form>
    </b-card>
  </b-container>
</template>

<script>
  export default {
    name: 'AccountPasswordReset',
  };
</script>

<style scoped>
  .card-padding {
    margin-top: 25px;
  }
</style>
