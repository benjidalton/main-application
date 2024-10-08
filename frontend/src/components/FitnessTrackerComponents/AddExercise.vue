<script setup>
import { ref, computed, watch } from 'vue';
import { getExercisesByMuscleGroup, muscleGroups, insertNewExercise } from '@/services/FitnessTrackerService';
import { Exercise } from '@/models/FitnessTrackerModels/Exercise';
import BaseMenu from '../BaseComponents/BaseMenu.vue';

const emit = defineEmits(['newExercise'])
const dialog = ref(false);
const muscleGroupLabels = computed(() => {
	return muscleGroups.map(muscleGroup =>  muscleGroup.name );
})

const currentMuscleGroup = ref('');

const newExercise = ref(new Exercise());

const exercises = computed(() => {
    if (currentMuscleGroup.value) {
        const index = muscleGroups.findIndex(muscleGroup => 
            muscleGroup.name === currentMuscleGroup.value.toLowerCase()
        );
        if (index !== -1) {
            // Return the exercises for the matching muscle group
            return muscleGroups[index].exercises;
        }
    }
    return [];
})

watch(() => newExercise.value.sets, (newValue) => {
	newExercise.value.reps = Array.from({ length: newValue }, () => 0); // Initialize reps array
});

function addExercise() {
	console.log(' chosen muscle group:', newExercise.value.muscleGroup.toLowerCase())
	const index = muscleGroups.findIndex(muscleGroup => 
        muscleGroup.name === newExercise.value.muscleGroup.toLowerCase()
    );


 	if (index !== -1) {
        let currentExercises = muscleGroups[index].exercises;
        let exerciseName = newExercise.value.name.toLowerCase();
        let newExerciseAdded = currentExercises.includes(exerciseName);
		newExercise.value.muscleGroupId = muscleGroups[index].id;

        if (!newExerciseAdded) {
            // Insert new exercise
			if (exerciseName != '') {
				insertNewExercise(exerciseName, muscleGroups[index].id);
            	currentExercises.push(exerciseName);
			}
        }

        emit('newExercise', newExercise.value);
    }

    newExercise.value = new Exercise();
	newExercise.value.muscleGroup = currentMuscleGroup.value; // set default muscle group. same muscle group likely to be used repeatedly
}

function handleExerciseChosen(exercise) {
	newExercise.value.name = exercise;
	
}

function handleMuscleGroupChosen(muscleGroup) {
	newExercise.value.muscleGroup = muscleGroup;
	currentMuscleGroup.value = muscleGroup;
}

function handleDateChange(date) {
	newExercise.value.date = date; 
}

function openDialog() {
	dialog.value = true;
}

function closeDialog() {
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
				<BaseMenu 
					@itemChosen="handleExerciseChosen" 
					baseLabel="Choose Exercise" 
					:menuItems="exercises" 
					:addExercise="true"
					@openDialog="openDialog"
					icon="mdi-format-list-numbered-rtl"
				/>
			</v-col>
		</v-row>
		
		<v-row align="center">
			<v-col cols="2">
				<v-card class="custom-number-input" id="sets-input">
					<v-card-title>
						Sets
					</v-card-title>
					<v-text-field 
						v-model="newExercise.sets"
						type="number"
						placeholder="Sets"
						bg-color="inherit"
						style="padding: 0px 10px 0px 10px; "
					/>
				</v-card>
				
			</v-col>
			
			<template v-for="(set, index) in newExercise.reps" :key="index">
				<v-card class="custom-number-input">
					<v-card-title>
						Set {{ index + 1 }}
					</v-card-title>
					<v-text-field 
						v-model="newExercise.reps[index]"
						type="number"
						bg-color="inherit"
						placeholder="Reps"
						style="padding: 0px 10px 0px 10px; "
					/>
				</v-card>
				
			</template>
			<v-col>
				<v-card class="custom-number-input" id="weight-input">
					<v-card-title>
						Weight (lb)
					</v-card-title>
					<v-text-field 
						v-model="newExercise.weight"
						type="number"
						bg-color="inherit"
						style="padding: 0px 10px 0px 10px; "
					/>
				</v-card>

			</v-col>

		</v-row>
		<v-row justify="end">
			<v-btn id="submit-new-exercise" @click="addExercise" style="margin: 10px;">Add Exercise</v-btn>
		</v-row>

		<v-dialog v-model="dialog" width="500px">
			<v-card  >
				<v-card-title>
					<span class="headline" style="font-size: 30px;">Add New Exercise</span>
				</v-card-title>
				<v-card-text>
					<v-text-field 
						v-model="newExercise.name"
						label="Exercise Name"
						placeholder="Enter exercise name"
					/>
				</v-card-text>
				<v-card-actions>
					<v-btn @click="dialog = false" style="font-size: 26px;" color="red">Cancel</v-btn>
					<v-btn color="primary" @click="closeDialog" style="font-size: 26px;">Save</v-btn>
				</v-card-actions>
			</v-card>
		</v-dialog>

	</v-container>
	
</template>


<style scoped>

.container {
	width: 1200px;
	background-color: rgb(243, 243, 243);
	border-radius: 10px;
	margin-bottom: 50px;
	box-shadow: 0px 5px 5px var(--custom-card-bg);
}

.custom-number-input {
	height: 110px;
	width: 130px;
	margin-right: 20px;
	
}

#sets-input {
	left: 20%;
}

#weight-input {
	position: relative;
	width: 200px;
}


#submit-new-exercise {
	background-color: var(--custom-card-bg);
	color: rgb(75, 75, 75);
}

</style>