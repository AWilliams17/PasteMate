<template>
  <b-container>
    <b-alert show dismissible variant="dark" v-if="notifications.length > 0" @dismissed="clearNotifications()">
      <div v-for="(value, key) in notifications" :key="key">
        <strong>{{value}}</strong>
      </div>
    </b-alert>
    <b-alert show dismissible variant="danger" v-if="signed_out_message !== ''" @dismissed="clearSignOutNotice()">
      <strong>{{signed_out_message}}</strong>
      <b-link @click="openSignInPage()" style="font-weight: bold;">
        Press here to open the sign in page (in a new tab).
      </b-link>
    </b-alert>
  </b-container>
</template>

<script>
  export default {
    name: 'notification-container',
    data() {
      return {
        notifications: [],
        signed_out_message: ''
      };
    }, // TODO: This is all kind of iffy. Could make this way better.
    created() {
      this.$notificationHub.$on('notification', (notification) => {
        this.notifications.push(notification);
      });
      this.$notificationHub.$on('signout_notice', (message) => {
        this.signed_out_message = message;
      });
    },
    methods: {
      clearNotifications() {
        this.notifications = [];
      },
      clearSignOutNotice() {
        this.signed_out_message = '';
      },
      openSignInPage() {
        const route = this.$router.resolve({path: '/account/signin'});
        window.open(route.href, '_blank');
        this.clearSignOutNotice();
      }
    }
  };
</script>

<style scoped>
</style>
