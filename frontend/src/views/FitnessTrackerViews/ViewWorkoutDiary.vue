<script setup>
import { ref, computed, watch } from 'vue';
import BaseMenu from '@/components/BaseComponents/BaseMenu.vue';
import WorkoutTable from '@/components/FitnessTrackerComponents/WorkoutTable.vue';
import { selectWorkoutByDate, selectWorkoutByDateRange } from '@/services/FitnessTrackerService';
import { getExercisesByMuscleGroup, allMuscleGroups, insertNewExercise } from '@/services/FitnessTrackerService';
import LoadingIndicator from '@/components/LoadingIndicator.vue';

const loading = ref(false);
const diary = ref([]);
const exerciseMenuRef = ref(null);
const muscleGroupRef = ref(null);
const search = ref({'date': [], 'muscleGroups': [], 'exercises': []})
const currentMuscleGroup = ref('');
const muscleGroupLabels = computed(() => {
	return allMuscleGroups.map(muscleGroup =>  muscleGroup.name );
})

const muscleGroupExercises = computed(() => {
	if (currentMuscleGroup.value) {
		const index = allMuscleGroups.findIndex(muscleGroup => 
			
			muscleGroup.name.toLowerCase() === currentMuscleGroup.value.toLowerCase()
		);
		if (index !== -1) {
			// Return the exercises for the matching muscle group
			return allMuscleGroups[index].exercises;
		}
	} else {
		return allExercises.value
	}
	return [];
})

const allExercises = computed(() => {
    // Create an array to hold exercises for all muscle groups
    const exercises = [];
    // Loop through all muscle groups and gather their exercises
    allMuscleGroups.forEach(muscleGroup => {
        if (muscleGroup.exercises) {
            exercises.push(...muscleGroup.exercises);
        }
    });
    return exercises;
});

function handleMuscleGroupChosen(muscleGroup) {
	currentMuscleGroup.value = muscleGroup; // need this so the exercise list stays correctly populated
	search.value.muscleGroups = muscleGroup;
}

function handleExerciseChosen(exercise) {
	search.value.exercises = [exercise];
}

function handleAllExercisesChosen() {
	const index = allMuscleGroups.findIndex(muscleGroup => 
		muscleGroup.name.toLowerCase() === currentMuscleGroup.value.toLowerCase()
	);
	if (index !== -1) {
		// Return the exercises for the matching muscle group
		search.value.muscleGroups = allMuscleGroups[index].exercises;
	}
	console.log('search.value.exercises', search.value.exercises)
}

function handleAllMuscleGroupsChosen() {
	search.value.muscleGroups = muscleGroupLabels.value;
	currentMuscleGroup.value = null;
}

function handleDateChange(date) {
	search.value.date = date; 
	
}

async function commitSearch() {
	loading.value = true;
	exerciseMenuRef.value.resetLabel();
	muscleGroupRef.value.resetLabel();
	let muscleGroups = search.value.muscleGroups; // Assume this is an array of muscle groups
	let exercises = search.value.exercises; // Assume this is an array of exercises
	let dates = search.value.date; // Assume this is either a date array or a single date
	console.log('muscle groups', muscleGroups)
	console.log('exercises', exercises)
	
	let selectedMuscleGroups = Array.isArray(muscleGroups) && muscleGroups.length > 0 
		? muscleGroups 
		: [muscleGroups]; // Ensure it is an array

	let selectedExercises = Array.isArray(exercises) && exercises.length > 0 
		? exercises 
		: [exercises]; // Ensure it is an array

	console.log('selected muscle groups: ', selectedMuscleGroups)
	console.log('selected selectedExercisess: ', selectedExercises)

	let minDate, maxDate;
	if (Array.isArray(dates)) {
		// Handle date range
		minDate = dates[0];
		maxDate = dates[dates.length - 1];
	} else {
		// Handle single date
		minDate = maxDate = dates; 
	}

	// // Fetch workouts based on the filters
	// try {
	//     if (selectedMuscleGroups.length > 0 && selectedExercises.length > 0) {
	//         // Both muscle groups and exercises selected
	//         diary.value = await selectWorkoutByMuscleAndExercise(selectedMuscleGroups, selectedExercises, minDate, maxDate);
	//     } else if (selectedMuscleGroups.length > 0) {
	//         // Only muscle groups selected
	//         diary.value = await selectWorkoutByMuscleGroup(selectedMuscleGroups, minDate, maxDate);
	//     } else if (selectedExercises.length > 0) {
	//         // Only exercises selected
	//         diary.value = await selectWorkoutByExercise(selectedExercises, minDate, maxDate);
	//     } else {
	//         // No filters, fetch all workouts
	//         diary.value = await selectAllWorkouts(minDate, maxDate);
	//     }
	// } catch (error) {
	//     console.error("Error fetching workouts:", error);
	// }

	// reset search params
	search.value = {'date': [], 'muscleGroups': allMuscleGroups, 'exercises': allExercises}
	loading.value = false;
}

</script>

<template>
	<v-container id="diary-container">
		<v-container class="container">
			<v-row justify="center">

				<v-col cols="3">
					<BaseMenu 
						@dateUpdated="handleDateChange" 
						baseLabel="Choose Date" 
						:datePicker="true"
						icon="mdi-calendar"
						:multiple="true"
					/>
				</v-col>

				<v-col cols="3">
					<BaseMenu 
						ref="muscleGroupRef"
						@itemChosen="handleMuscleGroupChosen" 
						baseLabel="All Muscle Groups" 
						:menuItems="muscleGroupLabels"
						icon="mdi-format-list-numbered-rtl"
						:multiple="true"
						@allItemsChosen="handleAllMuscleGroupsChosen"
					/>
				</v-col>

				<v-col cols="3">
					<BaseMenu 
						ref="exerciseMenuRef"
						@itemChosen="handleExerciseChosen" 
						baseLabel="All Exercises" 
						:menuItems="currentMuscleGroup ? muscleGroupExercises : allExercises" 
						icon="mdi-format-list-numbered-rtl"
						:multiple="true"
						@allItemsChosen="handleAllExercisesChosen"
					/>
				</v-col>

				<v-col cols="2">
					<v-btn @click="commitSearch">
						Search
					</v-btn>

				</v-col>

			</v-row>
		</v-container>
		<LoadingIndicator v-if="loading" />
		<WorkoutTable v-if="diary.length > 0" :items="diary"/>
	</v-container>
</template>


<style scoped>

#diary-container {
	width: 80vw;
	margin-top: 100px; 
}

.container {
	width: 1600px;
	background-color: rgb(243, 243, 243);
	border-radius: 10px;
	margin-bottom: 50px;
	box-shadow: 0px 5px 5px rgb(62, 57, 94);
}

.custom-number-input {
	height: 110px;
	width: 130px;
	margin-right: 20px;
	
}

</style>