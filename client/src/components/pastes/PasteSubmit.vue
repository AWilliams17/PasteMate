<template>
  <b-row>
    <b-col cols="12">
      <template v-if="!allow_edit">
          <b-alert show variant="warning" class="mx-auto" style="max-width: 30rem;">
            <p>This paste does not have open edit enabled, and you are not the owner of it.</p>
          </b-alert>
      </template>
      <template v-if="!show_password_form">
        <b-card v-bind:header="editing_paste ? 'Edit Paste' : 'Submit Paste'" class="mx-auto" style="max-width: 30rem;">
            <b-form @submit.prevent="onSubmit">
              <b-form-group id="titleFieldSet">
                <b-form-input id="titleInput" v-model="form.title" maxlength="24" required placeholder="Title..."></b-form-input>
              </b-form-group>
              <b-form-group id="contentFieldSet">
                <b-form-textarea id="contentInput"
                                 :rows="4"
                                 :max-rows="12"
                                 v-model="form.content"
                                 required
                                 placeholder="Paste Content..."
                                 class="paste-box"
                                 maxlength="600000"
                                 @keydown.native.tab.prevent="onTab">
                </b-form-textarea>
              </b-form-group>
              <b-form-group id="languageInputGroup">
                <b-form-select id="languageInput"
                               :options="languages"
                               required
                               v-model="form.language"
                               style="background-color: #27293d;">
                </b-form-select>
              </b-form-group>
              <template v-if="show_owner_options">
                <b-form-group id="expirationInputGroup">
                  <b-form-select id="expirationInput"
                                 :options="expiration"
                                 required
                                 v-model="form.expiration"
                                 style="background-color: #27293d;">
                  </b-form-select>
                </b-form-group>
                <template v-if="!editing_paste">
                <b-form-group id="passwordFieldSet"
                              :label-cols="4">
                  <b-form-input id="passwordInput"
                                v-model="form.password"
                                type="password"
                                label="Warning: Passwords are final"
                                placeholder="Password">
                  </b-form-input>
                </b-form-group>
                </template>
                <b-form-group>
                  <b-form-checkbox id="openEditCheckbox"
                                   v-model="form.open_edit"
                                   value=true
                                   unchecked-value=false>
                    Open Edit
                  </b-form-checkbox>
                </b-form-group>
              </template>
              <b-button type="submit" :disabled="!allow_edit" variant="primary" size="sm" class="float-right">Submit</b-button>
            </b-form>
          </b-card>
      </template>
      <template v-else>
        <b-card header="Password Required" class="mb-3 mx-auto" style="max-width: 25rem;">
          <b-form @submit.prevent="onSubmitPassword">
            <b-form-group id="passwordFieldSet"
                          horizontal
                          :label-cols="4"
                          label="Paste Password"
                          description="To continue, please enter this paste's password."
                          label-size="sm">
              <b-form-input id="passwordInput" type="password" size="sm" v-model="form.password" required></b-form-input>
            </b-form-group>
            <b-button type="submit" variant="primary" size="sm" class="float-right">Submit</b-button>
          </b-form>
        </b-card>
      </template>
    </b-col>
  </b-row>
</template>

<script>
  import axiosJWT from '../../_misc/axios_jwt';
  import { ADD_NOTIFICATION } from '../../store/action-types';
  import LanguageList from '../../_misc/highlightjs_languages';

  export default {
    name: 'paste-submit',
    data() {
      return {
        languages: [
          { 'text': 'None', value: 'Plaintext' },
          ...LanguageList.language_list
        ],
        expiration: [
          {'text': 'Never expires', value: 0},
          {'text': 'Expires in 10 minutes', value: 1},
          {'text': 'Expires in 1 hour', value: 2},
          {'text': 'Expires in 1 day', value: 3},
          {'text': 'Expires in 1 week', value: 4},
          {'text': 'Expires in 1 month', value: 5},
          {'text': 'Expires in 6 months', value: 6},
          {'text': 'Expires in 1 year', value: 7}
        ],
        form: {
          title: '',
          content: '',
          password: '',
          open_edit: false,
          expiration: 0,
          language: 'Plaintext'
        },
        editing_paste: false,
        has_paste: false,
        owner_name: '',
        pasteUUID: null,
        show_password_form: false,
        allow_edit: true
      };
    },
    mounted() {
      this.PasteUUID = this.$route.params.slug;
      if (this.PasteUUID) {
        this.editing_paste = true;
        this.getPasteInformation();
      }
    },
    computed: {
      username() {
        let user = this.$store.getters['session/user'];
        if (user) {
          return user.username;
        }
        return null;
      },
      show_owner_options() {
        if (!this.editing_paste) {
          return true;
        } else {
          if (this.username && this.has_paste) {
            return this.username === this.owner_name;
          }
          return false;
        }
      }
    },
    methods: {
      onSubmit() {
        let payload = this.form;
        const postURL = this.editing_paste ? '/api/paste/update/' + this.PasteUUID : '/api/paste/submit';
        axiosJWT.post(postURL, payload)
          .then((response) => {
            this.$router.push('/paste/view/' + response.data.paste_uuid);
          })
          .catch((error) => {
            const errorList = Object.values(error.response.data.errors);
            errorList.forEach((error) => {
              this.$store.dispatch(ADD_NOTIFICATION, error);
            })
          })
      },
      onSubmitPassword() {
        let payload = {'password': this.form.password};
        axiosJWT.post('/api/paste/get/' + this.PasteUUID, payload, {withCredentials: true})
          .then((response) => {
            this.has_paste = true;
            this.show_password_form = false;
            this.setPasteInformation(response);
          })
          .catch((error) => {
            this.$store.dispatch(ADD_NOTIFICATION, error.response.data.error);
          });
      },
      getPasteInformation() {
        axiosJWT.get('/api/paste/get/' + this.PasteUUID, {withCredentials: true})
          .then((response) => {
            this.has_paste = true;
            this.setPasteInformation(response);
          })
          .catch((error) => {
            if (error.response.status === 401) {
              this.show_password_form = true;
            } else {
              this.$store.dispatch(ADD_NOTIFICATION, error.response.data.error);
            }
          });
      },
      setPasteInformation(response) {
        this.owner_name = response.data.paste.owner_name;
        this.form.title = response.data.paste.title;
        this.form.language = response.data.paste.language;
        this.form.content += response.data.paste.content;
        this.form.open_edit = response.data.paste.open_edit;
        this.allow_edit = (this.owner_name === this.username || this.form.open_edit)
      },
      onTab(evt) { // Four space tab indention
        let startValue = evt.target.selectionStart;
        let currentValue = evt.target.value;
        evt.target.value = currentValue.substr(0, startValue) + '    ' + currentValue.substr(evt.target.selectionEnd);
        evt.target.selectionStart = evt.target.selectionEnd = startValue + 4;
      }
    }
  }
</script>
<style scoped>
  .paste-box {
    resize: vertical;
    max-height: 5000px;
    border: 1px solid #2b3553;
    border-radius: 0.4285rem;
    font-size: 0.75rem;
    line-height: 16px;
  }
  .paste-box:focus {
    border: 1px solid #e14eca;
    background-color: transparent;
    -webkit-box-shadow: none;
    box-shadow: none;
  }
</style>
