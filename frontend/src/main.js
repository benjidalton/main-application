import { createApp } from 'vue';

import router from './router';
import vuetify from './plugins/vuetify';

import App from './App.vue';
import './assets/main.css';
const app = createApp(App);

// Create and configure Pini
app.use(router).use(vuetify);


app.mount('#app')