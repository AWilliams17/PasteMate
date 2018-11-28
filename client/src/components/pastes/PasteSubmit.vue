<template>
  <b-row>
    <b-col cols="12">
      <b-card v-bind:header="this.editing_paste ? 'Edit Paste' : 'Submit Paste'" class="mx-auto" style="max-width: 30rem;">
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
          <template v-if="this.$store.getters['user/username'] !== owner_name">
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
      </b-card>
    </b-col>
  </b-row>
</template>

<script>
  import axios from 'axios';
  import LanguageList from '../../_misc/highlightjs_languages';

  export default {
    name: 'paste-submit',
    data() {
      return {
        editing_paste: false,
        owner_name: this.$store.getters['user/username'],
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
        }
      };
    },
    created() {
      const PasteUUID = this.$route.params.slug;
      if (PasteUUID) {
        this.getPasteInformation(PasteUUID);
      }
    },
    methods: {
      onSubmit(evt) {
        evt.preventDefault();
        const payload = this.form;
        axios.defaults.xsrfHeaderName = 'X-CSRF-TOKEN';
        axios.defaults.xsrfCookieName = 'csrf_access_token';
        if (this.editing_paste) {
          const PasteUUID = this.$route.params.slug;
          axios.post('/api/paste/edit/' + PasteUUID, payload, {withCredentials: true})
            .then((response) => {
              this.$router.push('/paste/view/' + response.data.paste_uuid);
            })
            .catch((error) => {
              this.$store.dispatch('notification/addNotification', 'Error: ' + error);
            });
        } else {
          axios.post('/api/paste/submit', payload, {withCredentials: true})
            .then((response) => {
              this.$router.push('/paste/view/' + response.data.paste_uuid);
            })
            .catch((error) => {
              this.$store.dispatch('notification/addNotification', 'Error: ' + error);
            });
        }
      },
      onTab(evt) { // Four space tab indention
        evt.preventDefault();
        let startValue = evt.target.selectionStart;
        let currentValue = evt.target.value;
        evt.target.value = currentValue.substr(0, startValue) + '    ' + currentValue.substr(evt.target.selectionEnd);
        evt.target.selectionStart = evt.target.selectionEnd = startValue + 4;
      },
      getPasteInformation(PasteUUID) {
        axios.get('/api/paste/edit/' + PasteUUID, {withCredentials: true})
          .then((response) => {
            this.editing_paste = true;
            this.form.title = response.data.paste.title;
            this.form.language = response.data.paste.language;
            this.form.content += response.data.paste.content;
          })
          .catch((error) => {
            this.$store.dispatch('notification/addNotification', 'Error: ' + error);
          });
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
  }
  .paste-box:focus {
    border: 1px solid #e14eca;
    background-color: transparent;
    -webkit-box-shadow: none;
    box-shadow: none;
  }
</style>
