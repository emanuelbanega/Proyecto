<template>
    <section class="error-message">
        <section class="error-message__container">
            <h1 class="animated bounce text-danger">Error 404 Not found</h1>
            <p class="zoom-area"><b>Error!</b> La url a la que quieres acceder no existe</p>
        </section>
        <div class="link-container">
            <router-link to="/">Ir a la pagina principal</router-link>
            <!-- <a href="{{ url_for('home') }}" class="more-link"> Ir a la pagina principal</a> -->
        </div>
    </section>
</template>

<style scoped>
h1 {
    margin: 0px;
    font-size: 60px;
}

.error-message {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: calc(100vh - 100px);
    width: 100%;
    font-family: Verdana, Geneva, Tahoma, sans-serif;
    background-image: linear-gradient(120deg, #6ad190 0%, #8fd3f4 100%);
}

.error-message__container {
    text-align: center;
    color: white;
}

p {
    font-size: 18px;
}

.animated {
    animation-duration: 2.5s;
    animation-fill-mode: both;
    animation-iteration-count: infinite;
}

@keyframes bounce {

    0%,
    20%,
    50%,
    80%,
    100% {
        transform: translateY(0)
    }

    40% {
        transform: translateY(-30px)
    }

    60% {
        transform: translateY(-15px)
    }
}

.bounce {
    animation-name: bounce;
}
</style>