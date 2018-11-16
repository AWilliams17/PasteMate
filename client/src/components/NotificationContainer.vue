<template>
  <b-container>
    <b-alert show dismissible variant="dark" v-if="notifications" @dismissed="clearNotifications()">
      <div v-for="(value, key) in notifications" :key="key">
        <p>{{value}}</p>
      </div>
    </b-alert>
  </b-container>
</template>

<script>
  export default {
    name: 'notification-container',
    data() {
      return {
        notifications: []
      };
    },
    created() {
      this.$notificationHub.$on('notification', (notification) => {
        this.notifications.push(notification);
      });
    },
    methods: {
      clearNotifications() {
        this.notifications = [];
      }
    }
  };
</script>

<style scoped>
</style>
