<script>
import { apiService } from '@/api'
import { useUserStore } from "../stores/modules/auth";
import { useLoadingView } from "../stores/loadingView";

export default {
  data() {
    return {
      sports: [],
      loadingView: useLoadingView(),
    };
  },
  beforeCreate() {
    if (!(localStorage.getItem("user")) || (localStorage.getItem("user").length < 3)) {
      this.$router.push("/")
    }
  },
  async created() {
    if ((localStorage.getItem("user")) && (localStorage.getItem("user").length > 2)) {
      this.loadingView.loadingView = true;
      await apiService
        .get("/me/sports")
        .then((response) => {
          this.sports = response.data;
        })
        .catch((e) => {
          var data = e.response.data;
          alert(data.msg);
          useUserStore().logoutUser();
        });
      this.loadingView.loadingView = false;
    }
  },
};
</script>

<template>
  <div v-if="sports.length > 0">
    <table class="tabla">
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
        <tr v-for="sport in sports" v-bind:key="sport.Nombre">
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
  <div v-if="!loadingView.loadingView && !sports.length > 0">Error al obtener disciplinas</div>
</template>

<style>

</style>
