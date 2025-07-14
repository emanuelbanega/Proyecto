<script setup>
import { useLoadingView } from "../stores/loadingView";
const loadingView = useLoadingView();
</script>

<template>
    <div v-if="loadingView.loadingView" class="content-loading text-info">
        <div class="text-center">
            <div class="spinner-border text-info" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
            <h5>cargando</h5>
        </div>
    </div>
</template>

<style scoped>
.content-loading {
    height: 80vh;
    width: 100vw;
    display: flex;
    justify-content: center;
    align-items: center;
}
</style>