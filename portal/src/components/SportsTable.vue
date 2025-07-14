<script>
import { apiService } from '@/api'
import { useLoadingView } from "../stores/loadingView";
export default {
  data() {
    return {
      sports: [],
      loadingView: useLoadingView(),
    };
  },
  async created() {
    this.loadingView.loadingView = true;
    await apiService
      .get("/club/sports")
      .then((response) => {
        this.sports = response.data;
      })
      .catch((e) => {
        var data = e.response.data;
        alert(data.msg);
      });
    this.loadingView.loadingView = false;
  },
};
</script>

<template>
  <div v-if="sports.length > 0">
    <table class="tabla table-striped">
      <caption>
        <div>
          <h2>Listado de disciplinas:</h2>
        </div>
      </caption>
      <thead>
        <tr>
          <th>Nombre</th>
          <th>Horarios</th>
          <th>Instructores</th>
          <th>Costo mensual</th>
          <th>Inscriptos</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="sport in sports" v-bind:key="sport.id">
          <td>{{ sport.Name }}</td>
          <td>{{ sport.Schedule }}</td>
          <td>{{ sport.Teachers }}</td>
          <td>{{ sport.Fee }}</td>
          <td v-if="sport.Signedup.length > 0">
            <router-link
              class="btn btn-primary"
              :to="{ name: 'sport-signedup', params: { id: sport.id } }"
              >Inscriptos
            </router-link>
          </td>
          <td v-else>-</td>
        </tr>
      </tbody>
    </table>
  </div>
  <div v-if="!loadingView.loadingView && !sports.length > 0">
    No hay disciplinas
  </div>
</template>

<style></style>
