<script setup>
import { ref, computed, watch, inject } from 'vue';
import { insertNewWorkout } from '@/services/FitnessTrackerService';
import { Exercise } from '@/models/FitnessTrackerModels/Exercise';
import BaseMenu from '../BaseComponents/BaseMenu.vue';
import BaseNumberInput from '../BaseComponents/BaseNumberInput.vue';
import { capitalizeWords } from '@/services/UtilService';

const emit = defineEmits(['successMessage'])
const dialog = ref(false);
const successMessage = ref('')
const allMuscleGroups = inject('allMuscleGroups')

const muscleGroupLabels = computed(() => {
	return allMuscleGroups.value.map(muscleGroup =>  muscleGroup.name );
})

const currentMuscleGroup = ref(null);
const currentMuscleGroupId = ref(null);
const tempExerciseName = ref(null);
const newExerciseName = ref(null)
const exerciseDate = ref(new Date().toISOString().split('T')[0])

const exercises = computed(() => {
	if (currentMuscleGroup.value) {
		const index = allMuscleGroups.value.findIndex(muscleGroup => 
			
			muscleGroup.name.toLowerCase() === currentMuscleGroup.value.toLowerCase()
		);
		if (index !== -1) {
			// Return the exercises for the matching muscle group
			// Return the name of each Exercise obj in exercises array
			currentMuscleGroupId.value = allMuscleGroups.value[index].id;
			return allMuscleGroups.value[index].exercises;
		}
	}
	return [];
})

watch(newExerciseName, (newExercise) => {
	// push new exercise instance to exercises
	exercises.value.push(
		new Exercise(
			null, 
			newExercise,
			new Date().toISOString().split('T')[0],
			currentMuscleGroupId.value,
			currentMuscleGroup.value
		)
	)
})


function updateReps(exercise) {
	// Update the reps array based on the new number of sets
	exercise.reps = Array.from({ length: exercise.sets }, () => 0);
}

async function addWorkoutEntry() {

	exercises.value.forEach(exercise => {
		exercise.calculateTotalReps()
		if (exercise.weight == null) {
			exercise.weight = exercise.defaultWeight;
		}
		if (exercise.date == null) {
			// default to current date if not specified
			exercise.date = exerciseDate.value;
		}
	})

	try {
		await insertNewWorkout(exercises.value);
		emit('successMessage');
	} catch (error) {
		console.error('Error saving workout:', error);
	}
	console.log('exercise at save:', exercises.value)
	currentMuscleGroup.value = null;
	return
}


function handleMuscleGroupChosen(muscleGroup) {
	currentMuscleGroup.value = muscleGroup;
}

function handleDateChange(date) {
	exerciseDate.value = date;
}

function openDialog() {
	console.log('open dialog')
	dialog.value = true;
}

function saveExercise() {
	newExerciseName.value = tempExerciseName.value;
	dialog.value = false;
}

</script>

<template>
	<v-container class="container">
		<v-row align="center" style="justify-content: center;">
			<v-col cols="3">
				<BaseMenu 
					@dateUpdated="handleDateChange" 
					baseLabel="Choose Date" 
					:datePicker="true"
					icon="mdi-calendar"
					:multiple="false"
				/>
			</v-col>
			

			<v-col cols="4">
				<BaseMenu 
					@itemChosen="handleMuscleGroupChosen" 
					baseLabel="Choose Muscle Group" 
					:menuItems="muscleGroupLabels"
					icon="mdi-format-list-numbered-rtl"
				/>
			</v-col>
			<v-col cols="4">
				<v-btn 
					v-if="currentMuscleGroup" 
					@click="openDialog"
				> 
					Add New Exercise
				</v-btn>
			</v-col>
		</v-row>

		<v-expansion-panels style="margin-top: 40px; margin-bottom: 60px;" multiple>
			<v-expansion-panel
				v-for="(exercise, index) in exercises"
				:title=capitalizeWords(exercise.name)
			>
				<v-expansion-panel-text class="panel-content">
					<v-row align="center">
						<v-col cols="2">
							<v-card class="custom-number-input" id="sets-input">
								<v-card-title>
									Sets
								</v-card-title>
								<v-text-field 
									v-model="exercise.sets"
									type="number"
									placeholder="Sets"
									bg-color="inherit"
									style="padding: 0px 10px 0px 10px; "
									variant="solo"
									:disabled="exercise.muscleGroup || exercise.name ? false: true"
									@change="updateReps(exercise, index)"
								/>
							</v-card>

						</v-col>

						<template v-for="(set, index) in exercise.reps" :key="index">
							<v-card class="custom-number-input">
								<v-card-title>
									Set {{ index + 1 }}
								</v-card-title>
								<v-text-field 
									v-model="exercise.reps[index]"
									type="number"
									bg-color="inherit"
									placeholder="Reps"
									style="padding: 0px 10px 0px 10px; "
									variant="solo"
									:disabled="exercise.muscleGroup || exercise.name ? false: true"
								/>
							</v-card>

						</template>
						<v-col>
							<v-card class="custom-number-input" id="weight-input">
								<v-card-title>
									Weight
								</v-card-title>
								<v-text-field 
								v-model="exercise.weight"
								type="number"
								bg-color="inherit"
								style="padding: 0px 10px 0px 10px; "
								variant="solo"
								:disabled="exercise.muscleGroup || exercise.name ? false: true"
								:placeholder="exercise.defaultWeight"
								/>
								<!-- <v-text-field 
									type="number"
									bg-color="inherit"
									style="padding: 0px 10px 0px 10px; "
									variant="solo"
									:disabled="exercise.muscleGroup || exercise.name ? false: true"
									:placeholder="exercise.defaultWeight"
								/> -->
							</v-card>

						</v-col>
					</v-row>
				</v-expansion-panel-text>
			</v-expansion-panel>
		</v-expansion-panels>
<!-- 
		<v-row align="center" v-for="(exercise, index) in exercises" style="margin-bottom: 50px; border-bottom: 1px solid gray;">
			<v-col cols=3>
				<v-card >
					<v-card-title>
						{{ capitalizeWords(exercise.name) }}
					</v-card-title>
				</v-card>

			</v-col>
			<v-col cols="2">
				<v-card class="custom-number-input" id="sets-input">
					<v-card-title>
						Sets
					</v-card-title>
					<v-text-field 
						v-model="exercise.sets"
						type="number"
						placeholder="Sets"
						bg-color="inherit"
						style="padding: 0px 10px 0px 10px; "
						variant="solo"
						:disabled="exercise.muscleGroup || exercise.name ? false: true"
						 @change="updateReps(exercise, index)"
					/>
				</v-card>
				
			</v-col>
			
			<template v-for="(set, index) in exercise.reps" :key="index">
				<v-card class="custom-number-input">
					<v-card-title>
						Set {{ index + 1 }}
					</v-card-title>
					<v-text-field 
						v-model="exercise.reps[index]"
						type="number"
						bg-color="inherit"
						placeholder="Reps"
						style="padding: 0px 10px 0px 10px; "
						variant="solo"
						:disabled="exercise.muscleGroup || exercise.name ? false: true"
					/>
				</v-card>
				
			</template>
			<v-col>
				<v-card class="custom-number-input" id="weight-input">
					<v-card-title>
						Weight
					</v-card-title> -->
					<!-- <v-text-field 
						v-model="exercise.weight"
						type="number"
						bg-color="inherit"
						style="padding: 0px 10px 0px 10px; "
						variant="solo"
						:disabled="exercise.muscleGroup || exercise.name ? false: true"
						:placeholder="exercise.defaultWeight"
					/> -->
					<!-- <v-text-field 
						type="number"
						bg-color="inherit"
						style="padding: 0px 10px 0px 10px; "
						variant="solo"
						:disabled="exercise.muscleGroup || exercise.name ? false: true"
						:placeholder="exercise.defaultWeight"
					/>
				</v-card>

			</v-col>

		</v-row> -->
		<v-row justify="end">
			<v-btn 
				
				id="submit-new-exercise" 
				@click="addWorkoutEntry" style="margin: 10px;"
				:disabled="false"
				>
				Save Workout
			</v-btn>
		</v-row>

		<v-dialog v-model="dialog" width="500px">
			<v-card  >
				<v-card-title>
					<span class="headline" style="font-size: 30px;">Add New Exercise</span>
				</v-card-title>
				<v-card-text>
					<v-text-field 
						v-model="tempExerciseName"
						label="Exercise Name"
						placeholder="Enter exercise name"
					/>
				</v-card-text>
				<v-card-actions>
					<v-btn @click="dialog = false" style="font-size: 26px;" color="red">Cancel</v-btn>
					<v-btn color="primary" @click="saveExercise" style="font-size: 26px;">Save</v-btn>
				</v-card-actions>
			</v-card>
		</v-dialog>

		

	</v-container>
	
</template>


<style scoped>

.container {
	width: 1200px;
	
	background-color: var(--custom-card-bg-opacity);
	border-radius: 10px;
	margin-bottom: 50px;
	box-shadow: 0px 5px 5px var(--custom-card-bg);
}

.custom-number-input {
	height: 110px;
	width: 150px;
	margin-right: 20px;
	/* background-color: beige; */
}

#sets-input {
	left: 0%;
}

#weight-input {
	position: relative;
	width: 150px;
}


#submit-new-exercise {
	background-color: var(--custom-card-bg);
	color: rgb(255, 255, 255);
}

.panel-content {
	background-color: rgba(205, 223, 223, 0.32);
}

</style>