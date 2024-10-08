<script setup>
import { ref } from 'vue';
import WorkoutTable from '@/components/FitnessTrackerComponents/WorkoutTable.vue';
import AddExercise from '@/components/FitnessTrackerComponents/AddExercise.vue';
import { insertNewWorkout } from '@/services/FitnessTrackerService';

const exercises = ref([]);

function handleNewExercise(exercise) {
	exercises.value.push(exercise);
}

function handleWorkoutSubmit() {
	console.log('workout submitted', exercises.value)
	exercises.value.forEach(exercise => {
		exercise.calculateTotalReps()
	})
	insertNewWorkout(exercises.value)

	exercises.value = [];
}

</script>

<template>
  	<v-container id="exercise-entry-container">
		<AddExercise @newExercise="handleNewExercise"/>

		<template v-if="exercises.length > 0">
			<WorkoutTable :items="exercises"/>
			<v-btn @click="handleWorkoutSubmit">
				Save Workout
			</v-btn>
		</template>
		
		
		
	</v-container>

</template>

<style scoped>

#exercise-entry-container {
	width: 60vw;
	margin-top: 100px; 
}
</style>