<template>
  <b-row>
    <b-col cols="12">
      <b-card v-bind:header="paste_edit_info.editing_paste ? 'Edit Paste' : 'Submit Paste'" class="mx-auto" style="max-width: 30rem;">
        <template v-if="!paste_edit_info.show_password_form">
          <b-form @submit="onSubmit">
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
                               @keydown.native.tab="onTab">
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
            <template v-if="paste_edit_info.show_owner_only">
              <b-form-group id="expirationInputGroup">
                <b-form-select id="expirationInput"
                               :options="expiration"
                               required
                               v-model="form.expiration"
                               style="background-color: #27293d;">
                </b-form-select>
              </b-form-group>
              <b-form-group id="passwordFieldSet"
                            :label-cols="4">
                <b-form-input id="passwordInput"
                              v-model="form.password"
                              type="password"
                              placeholder="Password">
                </b-form-input>
              </b-form-group>
              <b-form-group>
                <b-form-checkbox id="openEditCheckbox"
                                 v-model="form.open_edit"
                                 value=true
                                 unchecked-value=false>
                  Open Edit
                </b-form-checkbox>
              </b-form-group>
            </template>
            <b-button type="submit" variant="primary" size="sm" class="float-right">Submit</b-button>
          </b-form>
        </template>
        <template v-else>
          <b-card header="Password Required" class="mb-3 mx-auto" style="max-width: 25rem;">
            <b-form @submit="submitPassword">
              <b-form-group id="passwordFieldSet"
                            horizontal
                            :label-cols="4"
                            label="Paste Password"
                            description="To continue, please enter this paste's password."
                            label-size="sm">
                <b-form-input id="passwordInput" size="sm" v-model="password" required></b-form-input>
              </b-form-group>
              <b-button type="submit" variant="primary" size="sm" class="float-right">Submit</b-button>
            </b-form>
          </b-card>
        </template>
      </b-card>
    </b-col>
  </b-row>
</template>

<script>
  import axios from 'axios';
  import { ADD_NOTIFICATION } from '../../store/action-types';
  import LanguageList from '../../_misc/highlightjs_languages';

  export default {
    name: 'paste-submit',
    data() {
      return {
        current_user: this.$store.getters['user/username'],
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
          password: null,
          open_edit: false,
          expiration: 0,
          language: 'Plaintext'
        },
        paste_edit_info: {
          editing_paste: false,
          show_password_form: false,
          has_paste: false,
          requires_password: false,
          password: '',
          show_owner_only: (this.current_user === this.owner_name),
          owner_name: null
        }
      };
    },
    mounted() {
      const PasteUUID = this.$route.params.slug;
      if (PasteUUID) {
        this.paste_edit_info.editing_paste = true;
        this.getPasteInformation(PasteUUID);
      }
    },
    methods: {
      onSubmit(evt) {
        evt.preventDefault();
        const payload = this.form;
        axios.defaults.xsrfHeaderName = 'X-CSRF-TOKEN';
        axios.defaults.xsrfCookieName = 'csrf_access_token';
        if (!this.paste_edit_info.editing_paste) {
          axios.post('/api/paste/submit', payload, {withCredentials: true})
            .then((response) => {
              this.$router.push('/paste/view/' + response.data.paste_uuid);
            })
            .catch((error) => {
              this.$store.dispatch(ADD_NOTIFICATION, 'Error: ' + error);
            });
        } else {
          if (this.paste_edit_info.requires_password) {
            this.paste_edit_info.show_password_form = true;
          } else {
            const PasteUUID = this.$route.params.slug;
            this.updatePaste(PasteUUID);
          }
        }
      },
      getPasteInformation(PasteUUID) {
        axios.get('/api/paste/edit/get/' + PasteUUID, {withCredentials: true})
          .then((response) => {
            this.has_paste = true;
            this.setPasteInformation(response);
          })
          .catch((error) => {
            if (error.response.status === 401) {
              this.paste_edit_info.show_password_form = true;
              this.paste_edit_info.requires_password = true;
            } else {
              this.$store.dispatch(ADD_NOTIFICATION, 'Error: ' + error);
            }
          });
      },
      getPasteInformationWithPassword(PasteUUID, Password) {
        axios.post('/api/paste/edit/get/' + PasteUUID, Password, {withCredentials: true})
          .then((response) => {
            this.paste_edit_info.has_paste = true;
            this.paste_edit_info.show_password_form = true;
            this.setPasteInformation(response);
          })
          .catch((error) => {
            this.$store.dispatch(ADD_NOTIFICATION, 'Error: ' + error);
          });
      },
      updatePaste(PasteUUID) {
        const payload = this.form;
        axios.post('/api/paste/edit/post/' + PasteUUID, payload, {withCredentials: true})
          .then(() => {
            this.$router.push('/paste/view/' + PasteUUID);
          })
          .catch((error) => {
            this.$store.dispatch(ADD_NOTIFICATION, 'Error: ' + error);
          });
      },
      updatePasteWithPassword(PasteUUID, Password) {
        let payload = this.form;
        payload['paste_password'] = Password;
        axios.post('/api/paste/edit/post/' + PasteUUID, payload, {withCredentials: true})
          .then(() => {
            this.$router.push('/paste/view/' + PasteUUID);
          })
          .catch((error) => {
            this.$store.dispatch(ADD_NOTIFICATION, 'Error: ' + error);
          });
      },
      setPasteInformation(response) {
        this.paste_edit_info.owner_name = response.data.paste.owner_name;
        this.form.title = response.data.paste.title;
        this.form.language = response.data.paste.language;
        this.form.content += response.data.paste.content;
      },
      submitPassword(evt) {
        evt.preventDefault();
        const PasteUUID = this.$route.params.slug;
        if (!this.has_paste) {
          this.getPasteInformationWithPassword(PasteUUID, this.password);
        } else {
          const Password = this.paste_edit_info.password;
          this.updatePasteWithPassword(PasteUUID, Password);
        }
        this.password = '';
      },
      onTab(evt) { // Four space tab indention
        evt.preventDefault();
        let startValue = evt.target.selectionStart;
        let currentValue = evt.target.value;
        evt.target.value = currentValue.substr(0, startValue) + '    ' + currentValue.substr(evt.target.selectionEnd);
        evt.target.selectionStart = evt.target.selectionEnd = startValue + 4;
      }
    }
  };
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
