<script defer >
import { apiService } from '@/api'
import { useUserStore } from "../../stores/modules/auth";

const expresiones = {
    usuario: /^[a-zA-Z0-9\_\-]{4,16}$/, // Letras, numeros, guion y guion_bajo
    nombre: /^[a-zA-ZÀ-ÿ\s]{1,40}$/, // Letras y espacios, pueden llevar acentos.
    address: /^[a-zA-ZÀ-ÿ0-9\°\s]{1,30}$/, // Letras y espacios, pueden llevar acentos.
    correo: /^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$/,
    phone: /^\d{7,14}$/, // 7 a 14 numeros.
    description: /^[a-zA-Z0-9\.\_\-\s]{0,150}$/,
}

const campos = {
    user: false,
    name: false,
    last_name: false,
    description: false,
    address: false,
    phone: false,
}

const validateCampo = (expresion, input, campo) => {
    if (expresion.test(input.value)) {
        document.getElementById(`grupo__${campo}`).classList.remove('form__grupo-incorrecto');
        document.getElementById(`grupo__${campo}`).classList.add('form__grupo-correcto');
        document.querySelector(`#grupo__${campo} i`).classList.add('fa-circle-check');
        document.querySelector(`#grupo__${campo} i`).classList.remove('fa-circle-xmark');
        document.querySelector(`#grupo__${campo} .form__input-error`).classList.remove('form__input-error-activo')
        campos[campo] = true
    } else {
        document.getElementById(`grupo__${campo}`).classList.add('form__grupo-incorrecto');
        document.getElementById(`grupo__${campo}`).classList.remove('form__grupo-correcto');
        document.querySelector(`#grupo__${campo} i`).classList.add('fa-circle-xmark');
        document.querySelector(`#grupo__${campo} i`).classList.remove('fa-circle-check');
        document.querySelector(`#grupo__${campo} .form__input-error`).classList.add('form__input-error-activo')
        campos[campo] = false
    }
}

const checkValidation = () => {
    if (!campos.user) {
        const input = document.getElementById('user')
        validateCampo(expresiones.usuario, input, 'user');
    }
    if (!campos.name) {
        const input = document.getElementById('name')
        validateCampo(expresiones.nombre, input, 'name');
    }
    if (!campos.last_name) {
        const input = document.getElementById('surname')
        validateCampo(expresiones.nombre, input, 'last_name');
    }
    if (!campos.address) {
        const input = document.getElementById('address')
        validateCampo(expresiones.address, input, 'address');
    }
    if (!campos.phone) {
        const input = document.getElementById('phone')
        if (input.value != "") {
            validateCampo(expresiones.phone, input, 'phone');
        } else {
            campos['phone'] = true
        }
    }
    if (!campos.description) {
        const input = document.getElementById('texDes')
        validateCampo(expresiones.description, input, 'description');
    }
}

export default {
    props: {
        profile: {}
    },
    created() {
        this.editUser.user = this.profile.user;
        this.editUser.first_name = this.profile.first_name;
        this.editUser.last_name = this.profile.last_name;
        this.editUser.description = this.profile.description;
        this.editUser.address = this.profile.address;
        this.editUser.phone = this.profile.phone;
    },

    data() {
        return {
            editUser: {
                user: " ",
                first_name: "",
                last_name: "",
                description: "",
                address: "",
                phone: "",
            },
            loadingEditDes: false,
        }
    },
    methods: {
        validateForm: (e) => {
            switch (e.target.name) {
                case "user":
                    validateCampo(expresiones.usuario, e.target, 'user');
                    break;
                case "name":
                    validateCampo(expresiones.nombre, e.target, 'name');
                    break;
                case "surname":
                    validateCampo(expresiones.nombre, e.target, 'last_name');
                    break;
                case "address":
                    validateCampo(expresiones.address, e.target, 'address');
                    break;
                case "phone":
                    if (e.target.value != "") {
                        validateCampo(expresiones.phone, e.target, 'phone');
                    } else {
                        document.getElementById(`grupo__phone`).classList.remove('form__grupo-incorrecto');
                        document.querySelector(`#grupo__phone i`).classList.remove('fa-circle-xmark');
                        document.getElementById(`grupo__phone`).classList.remove('form__grupo-correcto');
                        document.querySelector(`#grupo__phone i`).classList.remove('fa-circle-check');
                    }
                    break;
                case "texDes":
                    if (e.target.value != "") {
                        validateCampo(expresiones.description, e.target, 'description');
                    } else {
                        document.getElementById(`grupo__description`).classList.remove('form__grupo-incorrecto');
                        document.querySelector(`#grupo__description i`).classList.remove('fa-circle-xmark');
                        document.getElementById(`grupo__description`).classList.remove('form__grupo-correcto');
                        document.querySelector(`#grupo__description i`).classList.remove('fa-circle-check');
                    }
                    break;
            }
        },
        async actDes() {
            this.loadingEditDes = true;
            checkValidation()
            if (campos.user && campos.name && campos.last_name && campos.description && campos.address && campos.phone) {
                document.getElementById('formularioPerfil').reset();

                document.querySelectorAll('.form__grupo-correcto').forEach((icono) => {
                    icono.classList.remove('form__grupo-correcto')
                })
                let json = {
                    "user": this.editUser.user,
                    "first_name": this.editUser.first_name,
                    "last_name": this.editUser.last_name,
                    "description": this.editUser.description,
                    "address": this.editUser.address,
                    "phone": this.editUser.phone,
                }
                await apiService.post(`/me/profile`, json)
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
                            }
                            useUserStore().logoutUser();
                        } else {
                            alert("Se perdió la conexión con el servidor")
                        }

                    });
            } else {
                document.getElementById('form__msg').classList.add('form__msg-activo')

                setTimeout(() => {
                    document.getElementById('form__msg').classList.remove('form__msg-activo');
                }, 15000)
            }
            this.loadingEditDes = false;
        }
    }

}
</script>

<template>
    <form id="formularioPerfil" class="form-des" action @submit.prevent="actDes">
        <!-- Grupo: usuario -->
        <div class="form__grupo" id="grupo__user">
            <label for="user" class="form-label">Usuario:</label>
            <div class="form__grupo-input">
                <input v-on:keyup="validateForm" v-on:blur="validateForm" class="form-control form__input" type="text"
                    id="user" name="user" placeholder="Ingrese el nombre de usuario" v-model="editUser.user"
                    autocomplete="off" required>
                <i class="form__validation-state fa-solid fa-circle-xmark"></i>
            </div>
            <p class="form__input-error">El usuario tiene que ser de 4 a 16 dígitos y solo puede contener
                numeros, letras y guion bajo.</p>
        </div>

        <!-- Grupo: nombre -->
        <div class="form__grupo" id="grupo__name">
            <label for="name" class="form-label">Nombre:</label>
            <div class="form__grupo-input">
                <input v-on:keyup="validateForm" v-on:blur="validateForm" class="form-control form__input" type="text"
                    id="name" name="name" placeholder="Ingrese el nombre del asociado" v-model="editUser.first_name"
                    autocomplete="off" required>
                <i class="form__validation-state fa-solid fa-circle-xmark"></i>
            </div>
            <p class="form__input-error">El nombre solo puede tener letras y espacios. Puede tener hasta 40 caracteres.
            </p>
        </div>

        <!-- Grupo: apellido -->
        <div class="form__grupo" id="grupo__last_name">
            <label for="surname" class="form-label">Apellido:</label>
            <div class="form__grupo-input">
                <input v-on:keyup="validateForm" v-on:blur="validateForm" class="form-control form__input" type="text"
                    id="surname" name="surname" placeholder="Ingrese el apellido del asociado"
                    v-model="editUser.last_name" autocomplete="off" required>
                <i class="form__validation-state fa-solid fa-circle-xmark"></i>
            </div>
            <p class="form__input-error">El apellido solo puede tener letras y espacios. Puede tener hasta 40
                caracteres.</p>
        </div>

        <!-- Grupo: address -->
        <div class="form__grupo" id="grupo__address">
            <label for="address" class="form-label">Dirección:</label>
            <div class="form__grupo-input">
                <input v-on:keyup="validateForm" v-on:blur="validateForm" class="form-control form__input" type=" text"
                    id="address" name="address" placeholder="Ingrese la dirección del asociado"
                    v-model="editUser.address" autocomplete="off" required>
                <i class="form__validation-state fa-solid fa-circle-xmark"></i>
            </div>
            <p class="form__input-error">La dirección solo puede contener numeros, letras y °. Y hasta 40 caracteres.
            </p>
        </div>

        <!-- Grupo: phone -->
        <div class="form__grupo" id="grupo__phone">
            <label for="phone" class="form-label">Teléfono:</label>
            <div class="form__grupo-input">
                <input v-on:keyup="validateForm" v-on:blur="validateForm" class="form-control form__input" type="number"
                    id="phone" name="phone" placeholder="Ingrese el teléfono del asociado" v-model="editUser.phone"
                    autocomplete="off">
                <i class="form__validation-state fa-solid fa-circle-xmark"></i>
            </div>
            <p class="form__input-error">El telefono solo puede contener numeros y el maximo son 14 digitos.</p>
        </div>

        <!-- Grupo: description -->
        <div class="form__grupo" id="grupo__description">

            <label for="texDes" class="form-label">Acerca de mí </label>
            <div class="form__grupo-input">
                <textarea v-on:keyup="validateForm" v-on:blur="validateForm" class="form-control form__input"
                    id="texDes" name="texDes" rows="5" placeholder="Cuéntanos sobre ti"
                    v-model="editUser.description">{{ editUser.description }}</textarea>
                <i class="form__validation-state fa-solid fa-circle-xmark"></i>
            </div>
            <p class="form__input-error">La descripción solo puede tener letras, y un maximo de 150 caracteres</p>
        </div>

        <div class="form__msg" id="form__msg">
            <p><i class="fa-solid fa-triangle-exclamation"></i> <b>Error:</b> Rellene el formulario
                correctamente.</p>
        </div>
        <div class="form__grupo form__grupo-btn-act">
            <button v-if="loadingEditDes" class="btn btn-sm btn-info" type="button" disabled>
                <span class="spinner-grow spinner-grow-sm" role="status" aria-hidden="true"></span>
                Actualizando...
            </button>
            <input v-if="!loadingEditDes" type="submit" class="btn btn-sm btn-info" value="Actualizar">
        </div>
    </form>
</template>

<style scoped>
textarea {
    resize: none;
}

.form-label {
    color: burlywood;
    font-weight: 700;
    cursor: pointer;
}

.form__grupo-input {
    position: relative;
}

.form__input {
    width: 100%;
}

.form__input-error {
    font-size: 12px;
    margin-bottom: 0;
    display: none;
}

.form__input-error-activo {
    display: block;
}

.form__validation-state {
    position: absolute;
    right: 10px;
    bottom: 12px;
    z-index: 100;
    font-size: 16px;
    opacity: 0;
}

.form__msg {
    height: 45px;
    line-height: 45px;
    background: #F66060;
    padding: 0 15px;
    border-radius: 3px;
    display: none;
}

.form__msg-activo {
    display: block;
}

.form__msg p {
    margin: 0;
}

.form__grupo-btn-act {
    margin: 20px;
}

.form__grupo-correcto .form__validation-state {
    color: #1ed12d;
    opacity: 1;
}

.form__grupo-incorrecto .form-label {
    color: #bb2929;
}

.form__grupo-incorrecto .form__validation-state {
    color: #bb2929;
    opacity: 1;
}

.form__grupo-incorrecto .form__input {
    border: 3px solid #bb2929;
}
</style>