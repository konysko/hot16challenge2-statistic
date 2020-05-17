<template>
  <v-app>
    <div class="header">
      <h1>
        #hot16challenge2
      </h1>
      <span>statystyki</span>
    </div>
    <v-content>
      <router-view></router-view>
    </v-content>
  </v-app>
</template>

<script>
export default {
  name: 'App',

  components: {},

  data: () => ({
    //
  })
};
</script>

<style scoped>
.header {
  background: #272727;
  color: #fff;
  padding: 80px;
  text-align: center;
}
</style>
