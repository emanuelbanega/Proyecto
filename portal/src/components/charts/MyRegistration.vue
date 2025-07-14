<script setup>
import { apiService } from "@/api";
import BarChart from "../charts/BarChart.vue";
</script>

<script>
export default {
  data() {
    return {
      chartData: null,
      chartOptions: null,
      loaded: false,
      error: false
    };
  },
  async created() {
    await apiService.get("/me/profile/history").then((response) => {
      let tmp = response.data;
      this.chartData = {
        labels: tmp.ArrMonth,
        datasets: [
          {
            label: "Actividades",
            backgroundColor: ["#0d6efd6b"],
            borderColor: '#0d6efd',
            borderWidth: 1,
            data: tmp.monthly_activity,
          },
        ],
      };
      this.chartOptions = {
        responsive: true,
        maintainAspectRatio: false,
      };
    }).catch(e => {
      console.log(e)
      this.error = true
    });;
    this.loaded = true;
  },
};
</script>

<template>
  <div style="font-weight: 700; color: burlywood; padding: 0 5px">
    <h6> Mi actividad: </h6>
    <BarChart v-if="loaded && !error" :chart-data="chartData" :chart-options="chartOptions" :width="300"
      :height="200" />
    <div v-if="!loaded && !error" class="spinner-border text-primary" role="status">
      <span class="sr-only">Loading...</span>
    </div>
    <p v-if="error" style="color: #fff;">Sin datos</p>
  </div>
</template>
