import { createApp } from 'vue';

import router from './router';
import vuetify from './plugins/vuetify';
import { createPinia } from 'pinia';
import App from './App.vue';
import './assets/main.css';
const app = createApp(App);
const pinia = createPinia();
// Create and configure Pini
app.use(pinia).use(router).use(vuetify);


app.mount('#app')