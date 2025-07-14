<script setup>
import { apiService } from "@/api";
import { useLoadingView } from "../../stores/loadingView";
import PieChart from "../charts/PieChart.vue";
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
      chartData: null,
      chartOptions: null,
      loaded: false,
      empty: true,
      error: false,
    };
  },
  async created() {
    await apiService
      .get("/sport/data/genders/" + this.id)
      .then((response) => {
        let tmp = response.data;
        if (!(tmp.males == 0 && tmp.females == 0 && tmp.others == 0)) {
          this.chartData = {
            labels: ["Hombre", "Mujer", "Otro"],
            datasets: [
              {
                backgroundColor: ["#0d6efd", "#dc3545", "#6f42c1"],
                data: [tmp.males, tmp.females, tmp.others],
              },
            ],
          };
          this.chartOptions = {
            responsive: true,
            aspectRatio: 1,
            maintainAspectRatio: true,
          };
          this.empty = false;
        }
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
