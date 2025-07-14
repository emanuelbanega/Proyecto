<script setup>
import compDefaultersChart from "../components/charts/DefaultersChart.vue";
import compMembersChart from "../components/charts/MembersChart.vue";
import compGendersChart from "../components/charts/GendersChart.vue";
</script>

<template>
  <div>
    <h2 style="text-align: left; color: white; padding-left: 10px">
      Asociados morosos y no morosos:
    </h2>
    <div style="position: relative; margin: 5vh; height: 50vh; width: 50vh" class="Chart">
      <compDefaultersChart />
    </div>
    <h2 style="text-align: left; color: white; padding-left: 10px">
      Miembros por mes este año:
    </h2>
    <div style="position: relative; margin: 5vh; height: 50vh; width: 100vh" class="Chart">
      <compMembersChart />
    </div>
    <h2 style="text-align: left; color: white; padding-left: 10px">
      Distribucion generos por disciplina:
    </h2>
    <div style="position: relative; margin: 5vh; height: 50vh; width: 100vh" class="Chart">
      <compGendersChart />
    </div>
  </div>
</template>
