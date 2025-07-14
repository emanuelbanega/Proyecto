<script setup>
import { useUserStore } from "../stores/modules/auth"
const stateUser = useUserStore();
</script>

<template>
    <RouterLink class="nav-link-perfil" to="/perfil" v-if="stateUser.state.isLoggedIn && !stateUser.state.loading">
        <!-- <div id="user_info" v-if="!stateUser.state.log"> -->
        <img id="ItemPreview" alt="foto de usuario" v-bind:src="stateUser.state.user.photo">
    </RouterLink>
    <div v-if="stateUser.state.isLoggedIn && stateUser.state.loading" class="spinner-border" role="status">
        <span class="sr-only">Cargando...</span>
    </div>
    <div id="div-user-name">
        <RouterLink class="nav-link nav-link-perfil" to="/perfil" v-if="stateUser.state.isLoggedIn">
            <label>{{ stateUser.state.user.user }}</label>
        </RouterLink>
        <!-- </div> -->
        <button class="btn btn-outline-danger me-2" id="btn-LogOut" v-if="stateUser.state.isLoggedIn"
            @click="stateUser.logoutUser()">
            Cerrar sesion
        </button>
    </div>
</template>

<style scoped>
img {
    object-fit: cover;
    width: 50px;
    height: 50px;
    border-radius: 50%;
}

.nav-link-perfil {
    padding: 0;
    margin-right: 5px;
}

#btn-LogOut {
    padding: 1px 5px;
}

.user_info {
    cursor: pointer;
    width: 200px;
    display: flex;
    align-items: center;
    justify-content: end;
    color: white;
    font-family: Arial, Helvetica, sans-serif;
}

label {
    text-decoration: none;
    background: none;
    border: 0;
    font-size: 17px;
    cursor: pointer;
    user-select: none;
}
</style>