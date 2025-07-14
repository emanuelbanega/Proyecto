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
      error: false,
    };
  },
  async created() {
    await apiService
      .get("/sports/data/genders")
      .then((response) => {
        let tmp = response.data;
        this.chartData = {
          labels: tmp.sport_names,
          datasets: [
            {
              label: "Hombres",
              backgroundColor: ["#0d6efd6b"],
              borderColor: "#0d6efd",
              borderWidth: 1,
              data: tmp.genders[0],
            },
            {
              label: "Mujeres",
              backgroundColor: ["#dc3545"],
              borderColor: "#0d6efd",
              borderWidth: 1,
              data: tmp.genders[1],
            },
            {
              label: "Otros",
              backgroundColor: ["#6f42c1"],
              borderColor: "#0d6efd",
              borderWidth: 1,
              data: tmp.genders[2],
            },
          ],
        };
        this.chartOptions = {
          responsive: true,
          maintainAspectRatio: true,
          aspectRatio: 2,
        };
      })
      .catch((e) => {
        console.log(e);
        this.error = true;
      });
    this.loaded = true;
  },
};
</script>

<template>
  <div style="font-weight: 700; color: burlywood;">
    <BarChart v-if="loaded && !error" :chart-data="chartData" :chart-options="chartOptions"
    />
    <div v-if="!loaded && !error" class="spinner-border text-primary" role="status">
      <span class="sr-only">Loading...</span>
    </div>
    <p v-if="error" style="color: #fff">Sin datos</p>
  </div>
</template>
