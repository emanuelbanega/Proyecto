<script>
import { apiService } from '@/api'
import { useUserStore } from "../stores/modules/auth";

export default {
  data() {
    return {
        credential: null
    };
  },
  beforeCreate() {
    if (!(localStorage.getItem("user")) || (localStorage.getItem("user").length < 3)) {
      this.$router.push("/")
    }
  },
  async created() {
    if ((localStorage.getItem("user")) && (localStorage.getItem("user").length > 2)) {
      await apiService.get("/me/credential").then((response) => {
        this.credential = response.data;
      }).catch(e => {
        var data = e.response.data;
        alert(data.msg);
        useUserStore().logoutUser();
      });
    }
  },
  methods: {
    esMoroso(estado){
        if (estado) {
            return "Moroso"
        } else {
            return "Al dia"
        }
    }
  }
};
</script>
<template>
    <div id="recibo" class="recibo-pdf">
        <h2>Club Deportivo Villa Elisa</h2>
        <div id="recibo-content">
            <img class="img_user" v-bind:src="credential.photo"
        alt="foto de usuario" data-image-width="700" data-image-height="700" style="width: 200px;height:200px">
        <div style="display:flex;flex-direction: column;">
            <small>{{credential.name}} {{credential.surname}}</small>
            <small>DNI: {{credential.document_number}}</small>
            <small>Socio: #{{credential.id}}</small>
            <small>Fecha de alta: {{credential.discharge_date}}</small>
            <small>Estado: {{ esMoroso(credential.estado) }}</small>
            <img class="img_user" v-bind:src="credential.qr"
            alt="foto de carnet" data-image-width="700" data-image-height="700" style="width: 100px;height:100px">
        </div>
    </div>
</div>
<router-link
    class="btn btn-primary"
    style="margin-left:10px"
    :to="{ name: 'perfile' }"
    >Volver
</router-link>
</template>

<style scoped>
.recibo {
    border: 1px solid black;
    color: white;
    margin: 20px;
    width: 500px;
    padding: 20px;
    border-radius: 10px;
    background-color: rgb(100, 214, 25);
}

.recibo ul {
    list-style: none;
    margin-left: 10px;
}

.recibo button {
    padding: 7px;
    margin-top: 5px;
}

.recibo-pdf {
    background-color: white;
    margin: 20px;
    width: 500px;
    padding: 20px;
    border-radius: 10px;
}

#recibo-content {
    display: flex;
    justify-content: space-between;
}
</style>