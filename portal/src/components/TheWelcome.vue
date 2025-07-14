<script>
import { apiService } from '@/api'

export default {
  data() {
    return {
      searchText: "",
      sports: [],
      descHome: "",
      userInfo: null,
      focus: false
    };
  },
  async created() {
    await apiService.get("/club/sports").then((response) => {
      let someSports = response.data
      this.sports = [someSports[0], someSports[1], someSports[2]]
    });
    await apiService.get("/club/data/info_and_contact").then((response) => {
      if (response.data) {
        this.descHome = response.data["descHome"]
      }
    });
  },
  mounted() {
    const searchBar = document.getElementById("buscador")
    searchBar.addEventListener('focus', () => this.focus = !this.focus)
    searchBar.addEventListener('focusout', () => this.focus = !this.focus)
  },
  computed: {
    async getUserInfo() {
      if (this.searchText !== "") {
        await apiService.get("/club/associated/" + this.searchText)
          .then((response) => {
            const associated_info = response.data
            this.userInfo = associated_info
          }).catch(() => {
            console.log("No se encontro")
            this.userInfo = null
          })
      }
    }
  }
};
</script>

<template>
  <div class="welcomeView">
    <h1>Bienvenido al Portal del Club de Socios</h1>
    <p>
      {{ descHome }}
    </p>
  </div>
  <div class="searchBar">
    <label for="buscador">
      <h4>Ver estado de la cuota societaria</h4>
    </label><br>
    <input class="buscador" id="buscador" name="buscador" type="number" placeholder="Ingrese # de socio"
      v-model="searchText">
    <div class="associatedInfo" v-if="getUserInfo && userInfo !== null && searchText !== '' && focus">
      <p>Nombre: {{ userInfo.name }}</p>
      <p v-if="userInfo.defeated_quotas > 0">Estado Societario: Moroso</p>
      <p v-if="userInfo.defeated_quotas === 0">Estado Societario: Sin deudas</p>
      <p v-if="userInfo.defeated_quotas > 0">Cuotas Vencidas: {{ userInfo.defeated_quotas }}</p>
      <p v-if="userInfo.sports.length > 0">Disciplinas: </p>
      <ul v-if="userInfo.sports.length > 0">
        <li v-for="sport in userInfo.sports">{{ sport }}</li>
      </ul>
    </div>
    <div class="associatedInfo" v-if="getUserInfo && userInfo === null && searchText !== '' && focus">
      <p style="text-align:center">Sin resultados</p>
    </div>
  </div>
  <div class="sportList">
    <h2>Disciplinas populares</h2>
    <ul>
      <li v-for="sport in sports" v-bind:key="sport.Nombre">
        <h4>{{ sport.Name }}</h4>
        <p>{{ sport.Schedule }}</p>
        <p>{{ sport.Teachers }}</p>
        <p>{{ sport.Fee }}</p>
      </li>
    </ul>
    <a class="btn btn-primary" href="/disciplinas">Ver mas</a>
  </div>
</template>

<style>
input[type=number]::-webkit-inner-spin-button,
input[type=number]::-webkit-outer-spin-button {
  -webkit-appearance: none;
  margin: 0;
}

.searchBar {
  margin-top: 50px;
}

.searchBar input {
  background-color: rgb(31, 30, 30);
  padding: 10px;
  border-radius: 10px;
  border: 1px solid grey;
  color: white;
  width: 300px;
}

.sportList {
  margin-top: 50px;
}

.sportList ul {
  list-style: none;
  display: flex;
  flex-wrap: wrap;
  justify-content: space-around;
  margin-top: 50px;
}

.sportList li {
  background-color: #4743437d;
  padding: 20px;
  width: 400px;
  border-radius: 20px;
}

.sportList a {
  text-decoration: none;
  margin-left: 90%;
}

.associatedInfo {
  width: 300px;
  background-color: white;
  color: black;
  position: absolute;
  padding: 10px;
}
</style>
