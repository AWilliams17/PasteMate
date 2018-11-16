<template>
  <b-container>
    <b-alert show dismissible variant="dark" v-if="notifications.length > 0" @dismissed="clearNotifications()">
      <div v-for="(value, key) in notifications" :key="key">
        <strong>{{value}}</strong>
      </div>
    </b-alert>
    <b-alert show dismissible variant="dark" v-if="sign_out_notice" @dismissed="clearSignOutNotice()">
      <strong>You have been signed out due to inactivity.</strong>
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
        sign_out_notice: false
      };
    },
    created() {
      this.$notificationHub.$on('notification', (notification) => {
        this.notifications.push(notification);
      });
      this.$notificationHub.$on('signout_notice', () => {
        this.sign_out_notice = true;
      });
    },
    methods: {
      clearNotifications() {
        this.notifications = [];
      },
      clearSignOutNotice() {
        this.sign_out_notice = false;
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
