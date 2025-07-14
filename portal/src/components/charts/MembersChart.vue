<script setup>
import { apiService } from "@/api";
import { useLoadingView } from "../../stores/loadingView";
import LineChart from "../charts/LineChart.vue";
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
      .get("/club/data/associates")
      .then((response) => {
        let tmp = response.data;
        this.chartData = {
          labels: [
            "Enero",
            "Febrero",
            "Marzo",
            "Abril",
            "Mayo",
            "Junio",
            "Julio",
            "Agosto",
            "Septiembre",
            "Octubre",
            "Noviembre",
            "Diciembre",
          ],
          datasets: [
            {
              label: "Asociados",
              backgroundColor: ["#0d6efd"],
              borderColor: '#05CBE1',
              pointBackgroundColor: 'white',
              pointBorderColor: 'white',
              borderWidth: 1,
              data: tmp.monthly_members,
            },
          ],
        };
        this.chartOptions = {
          responsive: true,
          aspectRatio: 2,
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
    <LineChart v-if="loaded && !error" :chart-data="chartData" :chart-options="chartOptions"
    />
    <div v-if="!loaded && !error" class="spinner-border text-primary" role="status">
      <span class="sr-only">Loading...</span>
    </div>
    <p v-if="error" style="color: #fff">Sin datos</p>
  </div>
</template>
