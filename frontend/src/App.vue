<template>
  <v-app>
    <div class="header">
      <h1>
        #hot16challenge2
      </h1>
      <span>statystyka</span>
    </div>
    <v-content class="content">
      <router-view></router-view>
    </v-content>
    <v-footer class="footer"
      ><a href="https://github.com/konysko/hot16challenge2-statistic" target="_blank">
        <img
          width="20px"
          height="20px"
          src="/img/icons/GitHub-Mark-Light-64px.png"
          srcset="/img/icons/GitHub-Mark-Light-32px.png, /img/icons/GitHub-Mark-Light-64px.png 2x"
        />
        <span>
          source code
        </span>
      </a>
    </v-footer>
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
  color: #fff;
  background: #de4000;
  padding: 80px;
  text-align: center;
}
.content {
  box-shadow: 0px 0px 20px 0px #00000051;
}
.footer {
  padding: 40px;
  justify-content: center;
}
.footer > a {
  color: #eee;
  text-decoration: none;
  display: flex;
  align-items: center;
  opacity: 50%;
}
.footer > a:hover {
  opacity: 75%;
}
.footer > a > span {
  margin-left: 10px;
}
</style>
