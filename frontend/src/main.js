import { createApp, ref, provide, watch } from 'vue';

import router from './router';
import vuetify from './plugins/vuetify';
import { createPinia } from 'pinia';
import App from './App.vue';
import './assets/main.css';

import { getExercisesByMuscleGroup, getWorkouts } from './services/FitnessTrackerService';

const app = createApp(App);
const pinia = createPinia();
// Create and configure Pini
const allMuscleGroups = ref(null);
const searchResults = ref('');


async function fetchMuscleGroups() {
	allMuscleGroups.value = await getExercisesByMuscleGroup();
}

await fetchMuscleGroups();

app.provide('allMuscleGroups', allMuscleGroups);
app.provide('searchResults', searchResults);

app.use(pinia).use(router).use(vuetify);
app.mount('#app')