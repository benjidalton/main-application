<script setup>
import { ref } from 'vue';
import AddExercise from '@/components/FitnessTrackerComponents/AddExercise.vue';

const successMessage = ref('Workout saved successfully!');
const snackbarVisible = ref(false);

function handleSuccessMessage() {
	snackbarVisible.value = true;
}

</script>

<template>
  	<v-container id="exercise-entry-container">
		<AddExercise  @successMessage="handleSuccessMessage"/>

		<v-snackbar v-model="snackbarVisible" color="success" timeout="3000">
			{{ successMessage }}
		</v-snackbar>
		
	</v-container>

</template>

<style scoped>

#exercise-entry-container {
	width: 60vw;
	margin-top: 100px; 
}
</style>