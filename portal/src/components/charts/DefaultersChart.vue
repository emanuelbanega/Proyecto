<script setup>
import { apiService } from "@/api";
import { useLoadingView } from "../../stores/loadingView";
import PieChart from "../charts/PieChart.vue";
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
      .get("/club/data/defaulters")
      .then((response) => {
        let tmp = response.data;
        this.chartData = {
          labels: ["No-Morosos", "Morosos"],
          datasets: [
            {
              backgroundColor: ["#0d6efd", "#dc3545"],
              data: [tmp.non_defaulters, tmp.defaulters],
            },
          ],
        };
        this.chartOptions = {
          responsive: true,
          aspectRatio: "1",
          maintainAspectRatio: true,
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
    <PieChart v-if="loaded && !error" :chart-data="chartData" :chart-options="chartOptions"
    />
    <div v-if="!loaded && !error" class="spinner-border text-primary" role="status">
      <span class="sr-only">Loading...</span>
    </div>
    <p v-if="error" style="color: #fff">Sin datos</p>
  </div>
</template>
