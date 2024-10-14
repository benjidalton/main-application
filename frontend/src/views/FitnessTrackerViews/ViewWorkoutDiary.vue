<script setup>
import { ref, computed, inject } from 'vue';
import BaseMenu from '@/components/BaseComponents/BaseMenu.vue';
import { getWorkouts } from '@/services/FitnessTrackerService';
import LoadingIndicator from '@/components/LoadingIndicator.vue';
import { capitalizeWords } from '@/services/UtilService';
import WorkoutTable from '@/components/FitnessTrackerComponents/WorkoutTable.vue';
import CustomChart from '@/components/CustomChart.vue';

const allMuscleGroups = inject('allMuscleGroups');
const searchResults = inject('searchResults');

const loading = ref(false);
const workoutDiary = ref([]);
const exerciseMenuRef = ref(null);
const muscleGroupRef = ref(null);
const search = ref({'dates': null, 'muscleGroups': null, 'exercises': null});
const rawSearchResults = ref(null);
const formattedSearchResults = ref(null);
const currentMuscleGroup = ref('');
const searchComplete = ref(false);


const muscleGroupLabels = computed(() => {
	return allMuscleGroups.value.map(muscleGroup =>  muscleGroup.name );
})

const muscleGroupExercises = computed(() => {
	if (currentMuscleGroup.value) {
		const index = allMuscleGroups.value.findIndex(muscleGroup => 
			
			muscleGroup.name.toLowerCase() === currentMuscleGroup.value.toLowerCase()
		);
		if (index !== -1) {
			// Return the exercises for the matching muscle group
			return allMuscleGroups.value[index].exercises;
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
	allMuscleGroups.value.forEach(muscleGroup => {
		if (muscleGroup.exercises) {
			exercises.push(...muscleGroup.exercises);
		}
	});
	return exercises;
});

const isDiaryEmpty = computed(() => {
	if (searchComplete.value) {
		return formattedSearchResults.value.length === 0;
	}
});

function handleMuscleGroupChosen(muscleGroup) {
	currentMuscleGroup.value = muscleGroup; // need this so the exercise list stays correctly populated
	search.value.muscleGroups = muscleGroup;
}

function handleExerciseChosen(exercise) {
	console.log('exercise in handle exercise chosen:', exercise)
	search.value.exercises = [exercise];
}

function handleAllExercisesChosen() {
	const index = allMuscleGroups.value.findIndex(muscleGroup => 
		muscleGroup.name.toLowerCase() === currentMuscleGroup.value.toLowerCase()
	);
	if (index !== -1) {
		// Return the exercises for the matching muscle group
		search.value.exercises = allMuscleGroups.value[index].exercises;
	}
}

function handleAllMuscleGroupsChosen() {
	search.value.muscleGroups = muscleGroupLabels.value;
	currentMuscleGroup.value = null;
}

function handleDateChange(date) {
	search.value.dates = date; 
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
	
	rawSearchResults.value = await getWorkouts(searchMuscleGroups, searchExercises, searchDates);

	
	// Group exercises by date
	let groupedExercisesByDate = [];
	rawSearchResults.value.forEach(exercise => {
		const date = exercise.date;

		// Find if this date already exists in the groupedExercisesByDate array
		const dateGroup = groupedExercisesByDate.find(group => group.date === date);

		if (dateGroup) {
			// If the date group exists, push the exercise into its exercises array
			dateGroup.exercises.push(exercise);
		} else {
			// If the date group does not exist, create a new one
			groupedExercisesByDate.push({
				date: date,
				exercises: [exercise]
			});
		}
	});

	formattedSearchResults.value = groupedExercisesByDate;

	searchComplete.value = true;
	search.value = {'dates': null, 'muscleGroups': null, 'exercises': null}
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

		<v-expansion-panels style="margin-top: 40px; margin-bottom: 60px;" multiple>
			<v-expansion-panel
				v-for="(workout, index) in formattedSearchResults"
				:title=workout.date
			>
				<v-expansion-panel-text class="panel-content">
					<!-- <v-row align="center" v-for="(exercise, index2) in workout.exercises" style="justify-content: space-around; ">
						<v-card width="100%" height="200px">
							<v-card-title>
								{{ capitalizeWords(exercise.name) }}: {{ exercise.weight }}
								
							</v-card-title>
							<v-row justify="space-around">
								<template  v-for="(repCount, index) in exercise.reps">
									<v-card class="custom-number-input">
										<v-card-title style="font">
											Set {{ index + 1 }}
										</v-card-title>
										{{ exercise.reps[index] }}
									</v-card>
								</template>
								<v-card class="custom-number-input">
									<v-card-title>
										Total Reps
									</v-card-title>
									{{ exercise.totalReps }}
								</v-card>
							</v-row>

						</v-card>
						
						
					</v-row> -->
					<WorkoutTable v-if="formattedSearchResults" :items="workout.exercises"/>
					<CustomChart :data="workout.exercises"/>
				</v-expansion-panel-text>
			</v-expansion-panel>
		</v-expansion-panels>


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
	height: 70px;
	width: 130px;
	margin-right: 20px;
	
}

#search-btn {
	background-color: var(--top-bar-btn);
	color: var(--top-nav-bar-btn-font);
}

</style>