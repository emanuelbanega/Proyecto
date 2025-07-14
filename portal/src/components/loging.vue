<script>
import { useUserStore } from '../stores/modules/auth'
// import {useUserTokenStore} from '../stores/userToken'

var myModalEl;
var modal;

export default {
    name: 'login',
    components: {

    },
    data: function () {
        return {
            user: {
                user: null,
                password: null,
            },
            error: false,
            error_msg: "",
            loading: false,
        }
    },
    methods: {
        async login() {
            // modal para ocultar el login en caso de exito
            myModalEl = document.getElementById('login');
            modal = bootstrap.Modal.getInstance(myModalEl);

            let json = {
                "user": this.user.user,
                "password": this.user.password,
            }

            this.loading = true;
            await useUserStore().loginUser(json).catch(e => {
                console.log(e)
                if (e.response.data) {
                    var data = e.response.data;
                    this.error = true;
                    this.error_msg = data.msg;
                }
            })
            this.loading = false;

            //Cleaning
            this.user = {
                user: null,
                password: null
            }
            if (useUserStore().state.isLoggedIn) {
                modal.toggle()
                this.$router.push('/')
            }

        },
    }
}
</script>
<template>
    <!-- //// Modal - Iniciar sesión //// -->
    <div class="modal fade" id="login">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">Inicia de sesión</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <form @submit.prevent="login">
                        <!-- ALERTA -->
                        <div class="alert alert-danger" role="alert" v-if="error">
                            {{ error_msg }}
                        </div>
                        <!-- CORREO -->
                        <div class="input-group mb-3">
                            <span class="input-group-text">Correo</span>
                            <input class="form-control" v-model="user.user" type="email" name="email"
                                placeholder="Ingrese el email" autocomplete="email" required maxlength="50">
                        </div>
                        <!-- PASSWORD -->
                        <div class="input-group mb-3">
                            <span class="input-group-text">Password</span>
                            <input class="form-control" v-model="user.password" type="password" name="password"
                                placeholder="Ingrese la contraseña" maxlength="30" autocomplete="current-password"
                                required>
                        </div>
                        <div class="d-grid gap-2">
                            <button v-if="!loading" type="submit" class="btn btn-primary">
                                <!-- Cierra el modal -->
                                Iniciar sesión
                            </button>
                            <button v-if="loading" class="btn btn-primary" type="button" disabled>
                                <span class="spinner-grow spinner-grow-sm" role="status" aria-hidden="true"></span>
                                Loading...
                            </button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
</template>