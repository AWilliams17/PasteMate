<template>
  <b-container>
    <b-alert show dismissible variant="dark" v-if="notifications.length > 0" @dismissed="clearNotifications()">
      <div v-for="(value, key) in notifications" :key="key">
        <strong>{{value}}</strong>
      </div>
    </b-alert>
  </b-container>
</template>

<script>
  export default {
    name: 'notification-container',
    computed: {
      notifications() {
        return this.$store.getters['session/notifications'];
      }
    },

    methods: {
      clearNotifications() {
        this.$store.dispatch('session/clearNotifications');
      }
    }
  };
</script>
