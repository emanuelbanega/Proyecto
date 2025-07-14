<script>
import { apiService } from '@/api'
import { useUserStore } from "../stores/modules/auth";

export default {
    data() {
        return {
            quotas: [],
            selected: null,
            imageData:null
        }
    },
    beforeCreate() {
        if (!(localStorage.getItem("user")) || (localStorage.getItem("user").length < 3)) {
            this.$router.push("/")
        }
    },
    async created() {
        await apiService.get("/me/quotas").then((response) => {
            this.quotas = response.data
        }).catch(e => {
            var data = e.response.data;
            alert(data.msg)
            useUserStore().logoutUser();
        })
    },
    methods:{
        selectQuota(position){
            this.selected = position;
        },
        cancel(){
            this.selected = null;
        },
        getBase64(file) {
            return new Promise((resolve, reject) => {
                const reader = new FileReader();
                const extension = file.name.split('.').pop();
                reader.readAsDataURL(file);
                reader.onload = () => resolve({
                    result:reader.result,
                    extension
                });
                reader.onerror = error => reject(error);
            });
        },
        changeImg() {
            this.getBase64(this.$refs.myImg.files[0]).then(
                data => this.imageData = { data:data.result, ext:data.extension }
            );

        },
        async make_payment() {
            let json = {
                "voucher_image": this.imageData.data.split(",")[1],
                "ext":this.imageData.ext,
                "quota_id":this.quotas[this.selected].id
            }
            console.log(json)
            await apiService.post(`/me/payments`, json)
                .then(response => {
                    if (response.status === 200) {
                        alert("La informacion del pago se subio correctamente")
                        window.location.reload()
                    }
                }).catch(e => {
                    if (e.response) {
                        var data = e.response.data;
                        alert(data.msg);
                    } else {
                        alert("Se perdió la conexión con el servidor")
                    }
                });
        },
    }
}

</script>
<template>
    <h1 style="color: white; margin: 10px;">Mis cuotas pendientes</h1>
    <h3 v-if="quotas.length === 0" style="color: gainsboro; margin: 10px;">No tiene cuotas para abonar</h3>
    <ul class="quotas-list" v-if="quotas.length > 0" v-for="(quota,index) in quotas" v-bind:key="quota.id">
        <li>
            <p><b>ID</b>: {{ quota.id }}</p>
            <p><b>Fecha de Vencimiento</b>: {{ quota.end_date }}</p>
            <p><b>Monto</b>: {{ quota.amount }} {{quota.currency_type}}</p>
            <button class="btn btn-secondary" v-on:click="selectQuota(index)">Pagar</button>
        </li>
    </ul>
    <div v-if="selected !== null" id="view-container">
        <div class="payment-view" v-if="selected !== null">
            <h2>Info de la cuota</h2>
            <p>Fecha de Vencimiento: {{quotas[selected].end_date}}</p>
            <p>Monto a pagar: {{quotas[selected].amount}} {{quotas[selected].currency_type}}</p>
            <h3>Suba el archivo o imagen del comprobante</h3>
            <form action @submit.prevent="make_payment" enctype="multipart/form-data">
                <div class="custom-file">
                    <input @change="changeImg" ref="myImg" title="archivo" type="file" class="custom-file-input"
                        name="archivo" required accept=".png, .jpg, .jpeg, .pdf" id="inputGroupFile">
                </div>
                <div class="options">
                    <button class="btn btn-primary" type="submit">Realizar pago</button>
                    <button class="btn btn-danger" v-on:click="cancel">Cancelar</button>
                </div>
            </form>
        </div>
    </div>
</template>

<style>
    #view-container {
        position: fixed;
        margin-top: auto;
        margin-bottom: auto;
        margin-left: auto;
        margin-right: auto;
        top: 0px;
        bottom: 0px;
        left: 0px;
        right: 0px;
        background-color: rgba(0, 0, 0, 0.433);
        width: 100%;
        height: 100%;
        display: flex;
        justify-content: center;
        align-items: center;
    }
    .payment-view {
        background-color: white;
        width: 80%;
        height: 70%;
        padding: 10px;
        border-radius: 10px;
        border: 10px solid gray;
    }
    .options {
        display: flex;
        justify-content: space-around;
        padding: 10px;
        margin-top: 50px;
    }
    .quotas-list {
        list-style: none;
    }
    .quotas-list li {
        background-color: whitesmoke;
        color: black;
        width: 300px;
        padding: 10px;
        border-radius: 10px;
        border: 2px solid gray;
    }
</style>