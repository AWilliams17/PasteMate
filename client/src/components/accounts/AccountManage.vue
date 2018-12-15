<template>
  <b-row>
    <b-col cols="12">
      <template v-if="showMainForm">
        <b-card header="Account Management Options" class="mb-3 mx-auto" style="max-width: 35rem;">
          <b-form>
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
                          label="Your Email"
                          label-size="sm">
              <b-form-input id="emailInput"
                            size="sm"
                            :readonly="true"
                            :value="email">
              </b-form-input>
            </b-form-group>
            <b-button @click="showDeletionForm = true" variant="danger" size="sm" class="float-left">Delete Account</b-button>
            <div class="float-right">
              <b-button @click="showPasswordForm = true" variant="warn" size="sm" class="float-right">Change Password</b-button>
              <b-button @click="showEmailForm = true" variant="warn" size="sm" class="float-right">Change Email</b-button>
            </div>
          </b-form>
        </b-card>
      </template>
      <template v-if="showPasswordForm || showEmailForm">
        <b-card v-bind:header="showPasswordForm ? 'Change Password' : 'Change Email'" class="mb-3 mx-auto" style="max-width: 35rem;">
          <b-form @submit.prevent="onDetailChange">
            <b-form-group id="currentPasswordFieldSet"
                          horizontal
                          :label-cols="4"
                          label="Current Password"
                          label-size="sm">
              <b-form-input id="passwordInput" v-model="password" type="password" size="sm" required></b-form-input>
            </b-form-group>
            <template v-if="showPasswordForm">
              <b-form-group id="passwordFieldSet"
                            horizontal
                            :label-cols="4"
                            label="New Password"
                            label-size="sm">
                <b-form-input id="passwordInput" v-model="newDetails.password" type="password" size="sm" required></b-form-input>
              </b-form-group>
            </template>
            <template v-if="showEmailForm">
              <b-form-group id="emailFieldSet"
                            horizontal
                            :label-cols="4"
                            label="New Email"
                            label-size="sm">
                <b-form-input id="passwordInput" v-model="newDetails.email" type="email" size="sm" required></b-form-input>
              </b-form-group>
            </template>
            <b-button @click="resetForms"
                      variant="primary" size="sm" class="float-left">Cancel
            </b-button>
            <b-button type="submit" variant="primary" size="sm" class="float-right">Submit</b-button>
          </b-form>
        </b-card>
      </template>
      <template v-if="showDeletionForm">
        <b-card header="Delete Account" class="mb-3 mx-auto" style="max-width: 35rem;">
          <b-form @submit.prevent="onDeletionConfirmation">
            <b-form-group id="currentPasswordFieldSet" horizontal :label-cols="4"
                          label="Current Password" label-size="sm">
              <b-form-input id="passwordInput" v-model="password" type="password" size="sm" required></b-form-input>
            </b-form-group>
            <p>Are you sure you want to delete your account? All your pastes will be lost.</p>
            <b-button @click="resetForms = false" variant="primary" size="sm" class="float-left">Cancel</b-button>
            <b-button type="submit" variant="primary" size="sm" class="float-right">Yes, delete my account.
            </b-button>
          </b-form>
        </b-card>
      </template>
    </b-col>
  </b-row>
</template>

<script>
  import axiosJWT from '../../_misc/axios_jwt';
  import { ADD_NOTIFICATION, UPDATE_EMAIL, DELETE_USER } from '../../store/action-types';
  import { dispatchErrors } from '../../_misc/utils';

  export default {
    name: 'account-manage',
    data() {
      return {
        showPasswordForm: false,
        showDeletionForm: false,
        showEmailForm: false,
        newDetails: {
          email: '',
          password: ''
        },
        password: ''
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
      },
      showMainForm() {
        return !this.showPasswordForm && !this.showDeletionForm && !this.showEmailForm;
      }
    },
    methods: {
      async onDetailChange() {
        const payload = this.showPasswordForm ? {
          'newPassword': this.newDetails.password,
          'currentPassword': this.password
        } : {
          'newEmail': this.newDetails.email,
          'currentPassword': this.password
        };
        if (this.showEmailForm) {
          try {
            await this.$store.dispatch(UPDATE_EMAIL, payload);
            this.$store.dispatch(ADD_NOTIFICATION, 'Operation successful.');
            this.resetForms()
          } catch (error) {
            dispatchErrors(error);
          }
        } else {
          axiosJWT.post('/api/user/update_password', payload)
            .then(() => {
              this.$store.dispatch(ADD_NOTIFICATION, 'Operation successful.');
              this.resetForms()
            })
            .catch((error) => {
              dispatchErrors(error);
            })
        }
      },

      async onDeletionConfirmation() {
        try {
          const payload = {'currentPassword': this.password};
          await this.$store.dispatch(DELETE_USER, payload);
          this.$store.dispatch(ADD_NOTIFICATION, 'Operation successful.');
          this.$router.push('/');
        } catch (error) {
          dispatchErrors(error);
        }
      },

      resetForms() {
        this.showPasswordForm = this.showEmailForm = false;
        this.password = '';
      }
    }
  };
</script>
