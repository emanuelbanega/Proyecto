<script setup>

import { RouterLink, RouterView } from 'vue-router';
import { ref } from 'vue'
import login from './components/loging.vue';
import compHeader from './components/Header.vue';
import compFooter from './components/Footer.vue';
import { useUserStore } from "./stores/modules/auth"
import compLoading from "./components/LoadingComp.vue";
import { Chart } from 'chart.js'


const storeUser = useUserStore();
Chart.defaults.color = '#fff'

</script>

<template>
  <compHeader></compHeader>
  <compLoading />
  <login v-if="!storeUser.state.loading" />
  <div class="content">
    <RouterView />
  </div>
  <compFooter></compFooter>
</template>

<style>
body {
  background-image: url("../public/fondo-home.jpeg");
  background-repeat: no-repeat;
  background-size: cover;
  background-attachment: fixed;
  overflow-x: hidden;
  position: relative;
  padding-bottom: 95px;
  min-height: 100vh;
}

.content {
  overflow-x: auto;
}
</style>
