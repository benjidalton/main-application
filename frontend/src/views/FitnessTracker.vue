<script setup>
import { ref, watch } from 'vue';

const headers = ref([
	{ text: 'Exercise', value: 'name' },
	{ text: 'Sets', value: 'sets' },
	{ 
		text: 'Reps',
		children: [
            { text: 'Set 1', value: 'height' },
            { text: 'Set 2', value: 'base' },
			{ text: 'Set 3', value: 'base' },
			{ text: 'Set 4', value: 'base' },
		]
	},
	{ text: 'Weight (lb)', value: 'weight' }
])

const exerciseOptions = ref(['Bicep Curls', 'Squats', 'Bench Press']);
const exerciseName = ref(null);
const exercises = ref([
	{ name: 'Bicep Curls', sets: 4, reps: 10, weight: 20 },
	{ name: 'Squats', sets: 4, reps: 10, weight: 50 },
	{ name: 'Bench Press', sets: 4, reps: 8, weight: 40 },
]);

const dialog = ref(false);
const newExercise = ref({ name: '', sets: 0, reps: [], weight: 0 });
const newExerciseName = ref('');
const newExerciseMuslceGroup = ref(null);
const muscleGroups = ref(['Biceps', 'Triceps', 'Shoulders', 'Chest', 'Back', 'Quads', 'Hamstrings'])

watch(() => newExercise.value.sets, (newValue) => {
	console.log('sets', newValue)
	newExercise.value.reps = Array.from({ length: newValue }, () => 0); // Initialize reps array
	console.log('newexercise', newExercise.value)
});

function addExercise() {
	exerciseOptions.value.push(newExerciseName.value)
	exerciseName.value = newExerciseName.value;

	console.log('new exercise', newExercise.value)

	newExerciseMuslceGroup.value = null;
	dialog.value = false;
	exercises.value.push({ ...newExercise.value });
	if (newExercise.value.name && !exercises.value.find(e => e.name === newExercise.value.name)) {
		exercises.value.push({ ...newExercise.value });
		
		newExercise.value = { name: '', sets: 0, reps: [], weight: 0 }; // Clear input fields after adding
	}
}

function chooseExercise(exercise) {
	newExercise.value.name = exercise;
}

function openDialog() {
	dialog.value = true;
}

</script>

<template>
  	<v-container id="exercise-entry-container">
		<v-data-table
			:headers="headers"
			:items="exercises"
			class="elevation-1"
		>
			<template v-slot:headers="{ columns }" >
				<tr id="header-row">
					<template v-for="column in columns" :key="column.key">
					<td>
						<span class=" cursor-pointer">{{ column.text }}</span>
					</td>
					</template>
				</tr>
			</template>	
	  		<template v-slot:top>
				<v-row>
					<v-col>
						<v-menu>
							<template v-slot:activator="{ props }">
								<v-btn v-bind="props">
									{{ exerciseName ? exerciseName : 'Choose Exercise' }}
								</v-btn>
							</template>
							<v-list>
								<v-list-item @click="openDialog">
									Add Exercise
									<v-icon icon="mdi-plus"/>
							
								</v-list-item>
								<v-list-item 
									v-for="(exercise, index) in exerciseOptions" 
									:key="index" 
									@click="chooseExercise(exercise)"
								>
									{{ exercise }}
								</v-list-item>
							</v-list>
						</v-menu>
					</v-col>
					<v-col>
						<v-text-field 
							v-model="newExercise.sets"
							label="Sets"
							type="number"
							placeholder="Sets"
							style="width: 100px;"
						/>
					</v-col>
					
					<template v-for="(set, index) in newExercise.reps" :key="index">
						<v-text-field 
							v-model="newExercise.reps[index]"
							:label="`Set ${ index + 1 }`"
							type="number"
							placeholder="Reps"
							max-width="100px"
							style="margin: 10px;"
						/>
					</template>
					<v-col>
						<v-text-field 
							v-model="newExercise.weight"
							label="Weight (lb)"
							type="number"
							placeholder="Weight"
						/>
					</v-col>
					<v-col>
						<v-btn @click="addExercise" color="primary">Add Exercise</v-btn>
					</v-col>
				</v-row>
				<v-row v-if="newExercise.sets > 0">
					
				</v-row>
			</template>
			<template v-slot:item.set1Reps="{ item }">

				10

				<v-text-field 
					v-model="item.set1Reps" 
					type="number" 
					placeholder="Reps" 
					style="width: 100px;" 
				/>
			</template>
			<template v-slot:item.set2Reps="{ item }">
				<v-text-field 
					v-model="item.set2Reps" 
					type="number" 
					placeholder="Reps" 
					style="width: 100px;" 
				/>
			</template>
			<template v-slot:item.set3Reps="{ item }">
				<v-text-field 
					v-model="item.set3Reps" 
					type="number" 
					placeholder="Reps" 
					style="width: 100px;" 
				/>
			</template>
			<template v-slot:item.set4Reps="{ item }">
				<v-text-field 
					v-model="item.set4Reps" 
					type="number" 
					placeholder="Reps" 
					style="width: 100px;" 
				/>
			</template>
		</v-data-table>

		<v-dialog v-model="dialog" max-width="500px">
			<v-card>
				<v-card-title>
					<span class="headline">Add New Exercise</span>
				</v-card-title>
				<v-card-text>
					<v-text-field 
						v-model="newExerciseName"
						label="Exercise Name"
						placeholder="Enter exercise name"
					/>
					<v-select
						v-model="newExerciseMuslceGroup"
						label="Muscle Group"
						:items="muscleGroups"
					/>
				</v-card-text>
				<v-card-actions>
					<v-btn @click="dialog = false">Cancel</v-btn>
					<v-btn color="primary" @click="addExercise">Save</v-btn>
				</v-card-actions>
			</v-card>
		</v-dialog>
	</v-container>

</template>

<style scoped>
#header-row {
	background-color: rgb(223, 223, 223);
	font-weight: bold;
	font-size: 24px;
	font-family: 'Poppins';
}

#exercise-entry-container {
	width: 60vw;
	margin-top: 100px; 
}
</style>