<script setup>
import userInfoComp from "../components/UserInfoNav.vue"
import { useUserStore } from "../stores/modules/auth"
const stateUser = useUserStore();
</script>

<template>
    <header>
        <div class="wrapper">
            <nav class="navbar navbar-expand-lg bg-light">
                <div class="container-fluid">
                    <RouterLink class="nav-link" to="/">
                        <img id="logo-nav" class="navbar-brand" src="../../public/logo.jpg" alt="logo del club">
                    </RouterLink>
                    <button class="navbar-toggler" type="button" data-bs-toggle="collapse"
                        data-bs-target="#navbarNavAltMarkup" aria-controls="navbarNavAltMarkup" aria-expanded="false"
                        aria-label="Toggle navigation">
                        <span class="navbar-toggler-icon"></span>
                    </button>
                    <div class="collapse navbar-collapse" id="navbarNavAltMarkup">
                        <div class="navbar-nav">
                            <RouterLink class="nav-link" to="/">Home</RouterLink>
                            <RouterLink class="nav-link" to="/disciplinas">Disciplinas</RouterLink>
                            <RouterLink class="nav-link" to="/usuario/disciplinas"
                                v-if="stateUser.state.isLoggedIn && !stateUser.state.loading">
                                Inscripciones
                            </RouterLink>
                            <RouterLink class="nav-link" to="/estadisticas">Estadísticas</RouterLink>
                            <RouterLink class="nav-link" to="/usuario/pagos"
                                v-if="stateUser.state.isLoggedIn && !stateUser.state.loading">
                                Mis Pagos
                            </RouterLink>
                            <button type="button" class="btn btn-outline-primary mx-2 nav991" data-bs-toggle="modal"
                                data-bs-target="#login" v-if="!stateUser.state.isLoggedIn">
                                Iniciar Sesion
                            </button>
                            <div class="div-user-info nav991">
                                <userInfoComp />
                            </div>
                        </div>
                    </div>
                    <button type="button" class="btn btn-outline-primary mx-2 nav1200" data-bs-toggle="modal"
                        data-bs-target="#login" v-if="!stateUser.state.isLoggedIn">
                        Iniciar Sesion
                    </button>
                    <div class="div-user-info nav1200">
                        <userInfoComp />
                    </div>
                </div>
            </nav>
        </div>
    </header>
</template>

<style scoped>
nav {
    padding: 2px;
}

#logo-nav {
    width: 60px;
    padding: 0;
}

.div-user-info {
    display: flex;
    align-items: center;
}

@media screen and (max-width: 991px) {
    .nav1200 {
        display: none;
    }
}

@media screen and (min-width: 992px) {
    .nav991 {
        display: none;
    }
}
</style>
