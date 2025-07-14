import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

export const useLoadingView = defineStore('loadingView', () => {
    const loadingView = ref(false)


    return { loadingView }
})