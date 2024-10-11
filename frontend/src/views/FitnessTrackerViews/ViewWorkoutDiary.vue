<script setup>
import { ref, computed, watch } from 'vue';
import BaseMenu from '@/components/BaseComponents/BaseMenu.vue';
import WorkoutTable from '@/components/FitnessTrackerComponents/WorkoutTable.vue';
import { 
	getExercisesByMuscleGroup, 
	allMuscleGroups, 
	insertNewExercise, 
	selectWorkoutByDate, 
	selectWorkoutByDateRange,
	getWorkouts
} from '@/services/FitnessTrackerService';
import LoadingIndicator from '@/components/LoadingIndicator.vue';

const loading = ref(false);
const workoutDiary = ref([]);
const exerciseMenuRef = ref(null);
const muscleGroupRef = ref(null);
const search = ref({'dates': null, 'muscleGroups': null, 'exercises': null})
const currentMuscleGroup = ref('');
const searchComplete = ref(false);
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

const isDiaryEmpty = computed(() => {
	if (searchComplete.value) {
		return workoutDiary.value.length === 0;
	}
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
		search.value.exercises = allMuscleGroups[index].exercises;
	}
}

function handleAllMuscleGroupsChosen() {
	search.value.muscleGroups = muscleGroupLabels.value;
	currentMuscleGroup.value = null;
}

function handleDateChange(date) {
	search.value.date = date; 
}

async function commitSearch() {
	searchComplete.value = false;
	loading.value = true;
	exerciseMenuRef.value.resetLabel();
	muscleGroupRef.value.resetLabel();
	let muscleGroups = search.value.muscleGroups; // Assume this is an array of muscle groups
	let exercises = search.value.exercises; // Assume this is an array of exercises
	let searchDates = search.value.dates; // Assume this is either a date array or a single date

	
	let searchMuscleGroups = Array.isArray(muscleGroups) && muscleGroups.length > 0 
		? muscleGroups 
		: muscleGroups == null ? null : muscleGroups; // Ensure it is an array

	let searchExercises = Array.isArray(exercises) && exercises.length > 0 
		? exercises 
		: exercises == null ? null : exercises; // Ensure it is an array

	console.log('selected muscle groups at search: ', searchMuscleGroups)
	console.log('selected exercises at search: ', searchExercises)
	console.log('dates in search ', searchDates)

	currentMuscleGroup.value = '';
	
		// No date entered so search for all muscles
	workoutDiary.value = await getWorkouts(searchMuscleGroups, searchExercises, searchDates);

	searchComplete.value = true;
	search.value = {'dates': null, 'muscleGroups': allMuscleGroups, 'exercises': allExercises}
	loading.value = false;
	return
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
					<v-btn 
						id="search-btn"
						@click="commitSearch" >
						Search
					</v-btn>

				</v-col>

			</v-row>
		</v-container>
		<LoadingIndicator v-if="loading" />
		<WorkoutTable v-if="workoutDiary.length > 0" :items="workoutDiary"/>
		
		<v-empty-state
	 		v-if="isDiaryEmpty"
			icon="mdi-magnify"
			text="Try adjusting your search terms or filters. Sometimes less specific terms or broader queries can help you find what you're looking for."
			title="We couldn't find a match."
		></v-empty-state>
	
	
	</v-container>


</template>


<style scoped>

#diary-container {
	width: 80vw;
	margin-top: 100px; 
	
}

.container {
	width: 1600px;
	border-radius: 10px;
	margin-bottom: 50px;
	box-shadow: 0px 5px 5px rgb(62, 57, 94);
	background-color: var(--custom-card-bg-opacity);
}

.custom-number-input {
	height: 110px;
	width: 130px;
	margin-right: 20px;
	
}

#search-btn {
	background-color: rgb(var(--custom-card-bg));
	color: rgb(255, 255, 255);
}

</style>