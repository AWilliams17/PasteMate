<template>
  <b-row>
    <b-col cols="12">
      <b-card header="Submit a Paste" class="mx-auto" style="max-width: 30rem;">
        <b-form @submit="onSubmit">
          <b-form-group id="titleFieldSet">
            <b-form-input id="titleInput" v-model="form.title" required placeholder="Title..."></b-form-input>
          </b-form-group>
          <b-form-group id="contentFieldSet">
            <b-form-textarea id="contentInput"
                             :rows="4"
                             :max-rows="12"
                             v-model="form.content"
                             required
                             placeholder="Paste Content..."
                             class="paste-box">
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
                             v-model="form.openEdit"
                             value=true
                             unchecked-value=false>
              Open Edit
            </b-form-checkbox>
          </b-form-group>
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
        languages: [
          { 'text': 'None', value: 'None' },
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
          openEdit: false,
          expiration: 0,
          language: 'None'
        }
      };
    },
    methods: {
      onSubmit(evt) {
        evt.preventDefault();
        const payload = this.form;
        console.log('submitted');
        axios.defaults.xsrfHeaderName = 'X-CSRF-TOKEN';
        axios.defaults.xsrfCookieName = 'csrf_access_token';
        axios.post('/api/paste/submit', payload, {withCredentials: true})
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
