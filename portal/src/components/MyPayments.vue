<script>
import { apiService } from '@/api'
import { useUserStore } from "../stores/modules/auth";

export default {
  data() {
    return {
      payments: [],
    };
  },
  beforeCreate() {
    if (!(localStorage.getItem("user")) || (localStorage.getItem("user").length < 3)) {
      this.$router.push("/")
    }
  },
  async created() {
    if ((localStorage.getItem("user")) && (localStorage.getItem("user").length > 2)) {
      await apiService.get("/me/payments").then((response) => {
        this.payments = response.data;
      }).catch(e => {
        var data = e.response.data;
        alert(data.msg);
        useUserStore().logoutUser();
      });
    }
  }
};
</script>
<template>
  <div v-if="payments.length > 0">
    <table class="tabla">
      <caption>
        <div>
          <h2>Listado de Pagos:</h2>
        </div>
      </caption>
      <thead>
        <tr>
          <th>Fecha</th>
          <th>Monto</th>
          <th>Estado</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="payment in payments" v-bind:key="payment.date">
          <td>{{ new Date(payment.date).toLocaleDateString() }}</td>
          <td>{{ payment.amount }}</td>
          <td v-if="payment.state">Aprobado</td>
          <td v-if="!payment.state">Pendiente de aprobacion</td>
        </tr>
      </tbody>
    </table>


  </div>
  <h3 style="color:white;margin:10px" v-if="!payments.length > 0">Aun no tiene cuotas pagas</h3>
  <router-link
    class="btn btn-primary"
    style="margin-left:10px"
    :to="{ name: 'new-payment' }"
    >Realizar pago
  </router-link>
</template>