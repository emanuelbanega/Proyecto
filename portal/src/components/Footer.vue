<script>
import { apiService } from '@/api'

export default {
    data() {
        return {
            phone: "Sin-dato",
            email: "Sin-dato",
        };
    },
    async created() {
        await apiService.get("/club/data/info_and_contact").then((response) => {
            if (response.data) {
                this.phone = response.data["celContact"]
                this.email = response.data["emailContact"]
            }
        });
    }
}
</script>
<template>
    <footer>
        <div class="contacto">
            <b>Contacto:</b><br>
            {{ phone }}<br>
            Email: {{ email }}
        </div>
        Club socios - Facultad de Informática - UNLP
    </footer>
</template>

<style scoped>
footer {
    position: absolute;
    height: 90px;
    bottom: 0;
    width: 100%;
    background-color: black;
    color: aliceblue;
    display: flex;
    align-items: center;
    padding: 10px;
    justify-content: space-between;
}

.contacto {
    font-size: 14px;
    margin-right: 10px;
}
</style>