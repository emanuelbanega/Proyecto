<script>
import { ref } from "vue";
import { apiService } from '@/api'
import { useUserStore } from "../stores/modules/auth";
import { useLoadingView } from "../stores/loadingView";
import formProfile from "../components/form/FormProfile.vue"
import compRegistrationChart from "../components/charts/MyRegistration.vue";

export default {
    components: {
        formProfile,
        compRegistrationChart
    },
    data() {
        return {
            profile: ref({
                user: "",
                email: "",
                first_name: "",
                last_name: "",
                photo: "",
                description: "",
                number: "",
                document_type: "",
                document_number: "",
                gender: "",
                address: "",
                phone: "",
                has_credential: "",
            }),
            editDes: ref(false),
            loadingEditDes: false,
            editImg: ref(false),
            loadingEditImg: false,
            newImg: null,
            validImg: false,
            loadingView: useLoadingView()
        };
    },
    beforeCreate() {
        if (!(localStorage.getItem("user")) || (localStorage.getItem("user").length < 3)) {
            this.$router.push("/")
        }
    },
    async created() {
        if ((localStorage.getItem("user")) && (localStorage.getItem("user").length > 2)) {
            this.loadingView.loadingView = true
            await apiService.get('/me/profile')
                .then(response => {
                    if (response.status === 200) {
                        this.profile.user = response.data.user;
                        useUserStore().state.user.user = this.profile.user
                        this.profile.email = response.data.email;
                        this.profile.first_name = response.data.first_name;
                        this.profile.last_name = response.data.last_name;
                        this.profile.photo = response.data.photo;
                        useUserStore().state.user.photo = response.data.photo;
                        this.profile.description = response.data.description;
                        this.profile.number = response.data.number;
                        if (this.profile.number.length < 5) {
                            for (let index = this.profile.number.length; index < 5; index++) {
                                this.profile.number = "0" + this.profile.number
                            }
                        }
                        this.profile.document_type = response.data.document_type;
                        this.profile.document_number = response.data.document_number;
                        this.setGender(response.data.gender);
                        this.profile.address = response.data.address;
                        this.profile.phone = response.data.phone;
                        this.profile.has_credential = response.data.has_credential;
                    }
                }).catch(e => {
                    var data = e.response.data;
                    if (e.response.status !== 401) {
                        alert(data.msg);
                    } else {
                        alert("Se venció la sesión")
                    }
                    useUserStore().logoutUser(this.$router);
                });
            this.loadingView.loadingView = false;
        }
    },
    methods: {
        setGender(gender) {
            if (gender === 'M') {
                this.profile.gender = "Hombre"
            } else if (gender === 'F') {
                this.profile.gender = "Mujer"
            } else {
                this.profile.gender = gender
            }
        },
        btnEditDes() {
            this.editDes = !this.editDes
        },
        btnEditImg() {
            this.editImg = !this.editImg
        },
        getBase64(file) {
            return new Promise((resolve, reject) => {
                const reader = new FileReader();
                reader.readAsDataURL(file);
                reader.onload = () => resolve(reader.result);
                reader.onerror = error => reject(error);
            });
        },
        changeImg() {
            const extensionesValidas = ".png, .jpg, .jpeg";
            const obj = document.getElementById("inputGroupFile");
            var ruta = obj.value;

            // capturando extensión del archivo
            var extension = ruta.substring(ruta.lastIndexOf('.') + 1).toLowerCase();

            var extensionValida = extensionesValidas.indexOf(extension);

            if (extensionValida < 0) {
                this.validImg = false;
                obj.classList.remove('is-valid');
                obj.classList.add('is-invalid');
            } else {
                this.validImg = true;
                obj.classList.remove('is-invalid');
                obj.classList.add('is-valid');

                this.getBase64(this.$refs.myImg.files[0]).then(
                    data => this.newImg = data
                );
            }

        },
        async actImg() {
            let json = {
                "photo": this.newImg.split(",")[1],
            }
            if (this.validImg) {
                this.loadingEditImg = true;
                await apiService.post(`/me/profile/photo`, json)
                    .then(response => {
                        if (response.status === 200) {
                            window.location.reload();
                        }
                    }).catch(e => {
                        if (e.response) {
                            var data = e.response.data;
                            if (e.response.status !== 401) {
                                alert(data.msg);
                            } else {
                                alert("Se venció la sesión")
                                useUserStore().logoutUser();
                            }
                        } else {
                            alert("Se perdió la conexión con el servidor")
                        }
                    });
                this.loadingEditImg = false;
            } else {
                alert("no, no, no")
            }
        },
    }
}
</script>

<template>
    <div v-if="!loadingView.loadingView" class="contenedor_perfil">
        <h1 class="nom-pagina">Perfil</h1>
        <div class="contenedor_acerca_de_mi">
            <h4 class="titulo_acerca_mi">Datos personales <a v-if="!editDes" id="btn-edit"
                    title="Editar descripción usuario"><i class="fa-solid fa-pen-to-square"
                        v-on:click="btnEditDes"></i></a></h4>
            <div v-if="!editDes">
                <span style="font-weight: 700;">Nombre de Usuario: </span>
                <br>{{ profile.user }}<br>
                <span style="font-weight: 700;">Nombre: </span>
                <br>{{ profile.first_name }} {{ profile.last_name }}<br>
                <span style="font-weight: 700;">Dirección: </span>
                <br>{{ profile.address }}<br>
                <span style="font-weight: 700;">Telefono: </span><br>
                <label v-if="profile.phone">{{ profile.phone }}</label>
                <label v-if="!profile.phone"> - </label>
                <br>
                <br>
                <span style="font-weight: 700;">Acerca de mí </span><br>
                <p class="parrafo_acerca_mi">{{ profile.description }}</p>
                <router-link
                    v-if="profile.has_credential === 'Con carnet'"
                    class="btn btn-primary"
                    style="margin-left:10px"
                    :to="{ name: 'carnet' }"
                    >Ver Carnet Digital
                </router-link>
            </div>
            <div v-else class="div-form-des">
                <formProfile :profile="this.profile" />
                <a class="btn btn-sm btn-danger" title="cancelar" v-on:click="btnEditDes">Cancelar</a>
            </div>

        </div>
        <div class="contenedor_img_user">
            <div style="text-align: center;">
                <img class="img_user" v-bind:src="profile.photo" alt="foto de usuario" data-image-width="700"
                    data-image-height="700">
                <h4>Cambiar foto de perfil <a v-if="!editImg" id="btn-edit" title="Actualizar foto de perfil"
                        v-on:click="btnEditImg"><i class="fa-solid fa-pen-to-square"></i></a></h4>
                <div v-if="editImg">
                    <form action @submit.prevent="actImg" enctype="multipart/form-data">
                        <div class="mb-3">
                            <input @change="changeImg" ref="myImg" title="archivo" type="file" class="form-control"
                                name="archivo" required accept=".png, .jpg, .jpeg" id="inputGroupFile"
                                aria-label="file example">
                            <div class="invalid-feedback" style="background-color: black;"> <i
                                    class="fa-solid fa-triangle-exclamation"></i>
                                <b>Error!</b> Solo se admiten imagenes de tipo: '.png', '.jpg', '.jpeg'
                            </div>
                            <!-- <div class="invalid-feedback">
                                Solo se admiten imagenes de tipo: '.png', '.jpg', '.jpeg'
                                <p class="form__input-error"> <i class="fa-solid fa-triangle-exclamation"></i>
                                    <b>Error!</b>
                                    Solo se
                                    admiten imagenes de tipo: '.png', '.jpg',
                                    '.jpeg'
                                </p>
                            </div> -->
                        </div>
                        <div class="input-group-append">
                            <button v-if="loadingEditImg" class="btn btn-sm btn-info" type="button" disabled>
                                <span class="spinner-grow spinner-grow-sm" role="status" aria-hidden="true"></span>
                                Actualizando...
                            </button>
                            <button v-if="!loadingEditImg" type="submit" class="btn btn-sm btn-info"
                                :disabled="!validImg">actualizar</button>
                            <a class="btn btn-sm btn-danger" title="cancelar" v-on:click="btnEditImg">Cancelar</a>
                        </div>
                    </form>
                </div>
            </div>
        </div>
        <div class="contenedor_detalles">
            <p class="parrafo_detalles">
                <span style="font-weight: 700;"># Socio: </span>
                <br>{{ profile.number }}<br>
                <span style="font-weight: 700;">Genero: </span>
                <br>{{ profile.gender }}<br>
                <span style="font-weight: 700;">Documento: </span>
                <br>{{ profile.document_type }} {{ profile.document_number }}<br>
                <span style="font-weight: 700;">Email: </span>
                <br>{{ profile.email }}<br>
            </p>
            <div class="Chart">
                <compRegistrationChart />
            </div>
        </div>
    </div>
</template>

<style scoped>
i {
    margin: 2px 10px;
    font-size: 18px;
}

.contenedor_perfil {

    text-align: center;
    max-height: 100%;
    max-width: 100vw;
    min-height: 86vh;
    height: 100%;
    padding-bottom: 20px;
    background-color: #00000073;
    color: azure;
    display: grid;
    grid-gap: 20px;
    grid-template-columns: repeat(3, 1fr);
    grid-template-rows: repeat(2, auto);

    grid-template-areas: "nom-pagina nom-pagina nom-pagina"
        "contenedor_acerca_de_mi contenedor_img_user contenedor_detalles";
}

.form-img {
    display: grid;
    justify-content: center;
    text-align: center;
    margin-top: 10px;
}

input {
    margin: 0 5px;
}

.nom-pagina {
    grid-area: nom-pagina;
    text-align: center;
    font-size: 2rem;
}


.contenedor_acerca_de_mi {
    grid-area: contenedor_acerca_de_mi;
    margin-left: 5px;
}

.btn {
    margin-left: 5px;
    margin-top: 5px;
}

#btn-edit {
    background: none;
    border: none;
    color: burlywood;
    cursor: pointer;

}

.contenedor_img_user {
    grid-area: contenedor_img_user;
}

.contenedor_detalles {
    grid-area: contenedor_detalles;
}

.img_user {
    border-radius: 50%;
    object-fit: cover;
    width: 20rem;
    height: 20rem;
    margin: 0 auto;
    display: flex;
    flex: 1;
    align-items: center;
    justify-content: center;
}

h4,
span {
    color: burlywood;
}


@media screen and (max-width: 790px) {
    .contenedor_perfil {
        grid-template-columns: repeat(1, 1fr);
        grid-template-rows: repeat(4, auto);
        grid-gap: 10px;
        grid-template-areas: "nom-pagina"
            "contenedor_acerca_de_mi"
            "contenedor_img_user"
            "contenedor_detalles";
        width: 100%;
    }

    .img_user {
        width: 50%;
        height: 50%;
    }

    .Chart {
        max-width: 100vw;
    }
}
</style>
