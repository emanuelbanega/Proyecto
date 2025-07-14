import { apiService } from '@/api'
import { defineStore } from 'pinia';
import { ref, computed, watch } from 'vue';
import router from '../../router'

export const useUserStore = defineStore('userStore', () => {
    const state = ref({
        user: {},
        isLoggedIn: false,
        loading: false,
    });

    if (localStorage.getItem("user")) {
        const data = JSON.parse(localStorage.getItem("user"))
        if (Object.entries(data).length !== 0) {
            state.value.user.user = data["user"]
            state.value.user.photo = data["photo"]
            state.value.isLoggedIn = true
        }
    }

    watch(
        state,
        (userVal) => {
            const json = {
                user: userVal.user.user,
                photo: userVal.user.photo,
            }
            localStorage.setItem("user", JSON.stringify(json));
        },
        { deep: true }
    )

    const loginUser = async (user) => {
        await apiService.post('/auth', user)
        await fetchUser()
    }

    const fetchUser = async () => {
        await apiService.get('/me/profile')
            .then(({ data }) => { setUser(data) })
    }

    const logoutUser = async () => {
        await apiService.get('/logout').catch((err) => {
            console.log(err);
        });
        logoutUserState();
        router.push('/')
    }

    const setUser = (user) => {
        state.value.isLoggedIn = true;
        const data = {
            user: user.user,
            photo: user.photo,
        }
        state.value.user = data;
    }

    const logoutUserState = () => {
        state.value.isLoggedIn = false;
        state.value.user = {};
    }

    return {
        state,
        loginUser,
        logoutUser,
    }
})