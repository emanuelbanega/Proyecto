import axios from 'axios';

// http://127.0.0.1:5000
// https://admin-grupo17.proyecto2022.linti.unlp.edu.ar
const apiService = axios.create({
    baseURL: 'https://admin-grupo17.proyecto2022.linti.unlp.edu.ar/api/',
    withCredentials: true,
    xsrfCookieName: 'csrf_access_token',
});

apiService.defaults.xsrfCookieName = 'csrf_access_token';
apiService.defaults.xsrfHeaderName = 'X-CSRF-TOKEN';

export { apiService };
