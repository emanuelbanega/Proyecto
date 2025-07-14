<script>
import { apiService } from "@/api";
import { useLoadingView } from "../stores/loadingView";

export default {
  props: {
    id: {
      type: Number,
      required: true,
    },
  },
  data() {
    return {
      associates: [],
      loadingView: useLoadingView(),
    };
  },
  async created() {
    this.loadingView.loadingView = true;
    await apiService
      .get("/sport/signedup/" + this.id)
      .then((response) => {
        this.associates = response.data;
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
  <div v-if="associates.length > 0">
    <table class="tabla table-striped">
      <caption>
        <div>Listado de inscriptos:</div>
      </caption>
      <thead>
        <tr>
          <th>Nombre</th>
          <th>Apellido</th>
          <th>Genero</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="each in associates" v-bind:key="each.id">
          <td>{{ each.name }}</td>
          <td>{{ each.surname }}</td>
          <td>{{ each.gender }}</td>
        </tr>
      </tbody>
    </table>
  </div>
  <div v-if="!loadingView.loadingView && !associates.length > 0" style="color: white; font-size: 30px">
    No hay inscriptos!
  </div>
</template>
