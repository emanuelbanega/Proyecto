<script setup>
import compSignedTable from "../components/SignedTable.vue";
import compGenderChart from "../components/charts/GenderChart.vue";
import { apiService } from "@/api";
</script>
<script>
export default {
  props: {
    id: {
      type: Number,
      required: true,
    },
  },
  data() {
    return {
      sport: {},
    };
  },
  async created() {
    await apiService
      .get("/sport/" + this.id)
      .then((response) => {
        this.sport = response.data;
      })
      .catch((e) => {
        var data = e.response.data;
        alert(data.msg);
      });
  },
};
</script>

<template>
  <h1 style="color: white; padding: 10px 0px 0px 10px">
    {{ sport.name }} {{ sport.division }}
  </h1>
  <div style="margin: 5vw">
    <compSignedTable :id="id" />
  </div>
  <h2 style="text-align: center; color: white">Distribucion de Generos:</h2>
  <div
    style="position: relative; margin: auto; height: 50vh; width: 50vh"
    class="Chart"
  >
    <compGenderChart :id="id" />
  </div>
</template>
