<template>
  <b-container>
    <b-alert show dismissible variant="dark" v-if="notifications.length > 0" @dismissed="clearNotifications()">
      <div v-for="(value, key) in notifications" :key="key">
        <strong>{{value}}</strong>
      </div>
    </b-alert>
    <b-alert show dismissible variant="dark" v-if="sign_out_notice" @dismissed="clearSignOutNotice()">
      <strong>{{sign_out_reason}}</strong>
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
        sign_out_notice: false,
        sign_out_reason: ''
      };
    }, // TODO: This is all kind of iffy. Could make this way better.
    created() {
      this.$notificationHub.$on('notification', (notification) => {
        this.notifications.push(notification);
      });
      this.$notificationHub.$on('signout_notice', (reason) => {
        this.sign_out_notice = true;
        this.sign_out_reason = reason;
      });
    },
    methods: {
      clearNotifications() {
        this.notifications = [];
      },
      clearSignOutNotice() {
        this.sign_out_notice = false;
        this.sign_out_reason = '';
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
