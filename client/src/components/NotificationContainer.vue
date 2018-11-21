<template>
  <b-container>
    <b-alert show dismissible variant="dark" v-if="notifications.length > 0" @dismissed="clearNotifications()">
      <div v-for="(value, key) in notifications" :key="key">
        <strong>{{value}}</strong>
      </div>
    </b-alert>
    <b-alert show dismissible variant="danger" v-if="sign_out_notification" @dismissed="clearSignOutNotification()">
      <strong>{{sign_out_notification}}</strong>
      <b-link @click="openSignInPage()" style="font-weight: bold;">
        Press here to open the sign in page (in a new tab).
      </b-link>
    </b-alert>
  </b-container>
</template>

<script>
  export default {
    name: 'notification-container',
    computed: {
      notifications() {
        return this.$store.getters['notification/notifications'];
      },

      sign_out_notification() {
        return this.$store.getters['notification/sign_out_notification'];
      }
    },

    methods: {
      openSignInPage() {
        const route = this.$router.resolve({path: '/account/signin'});
        window.open(route.href, '_blank');
        this.clearSignOutNotification();
      },

      clearNotifications() {
        this.$store.dispatch('notification/clearNotifications')
      },

      clearSignOutNotification() {
        this.$store.dispatch('notification/clearSignOutNotification')
      }
    }
  };
</script>

<style scoped>
</style>
