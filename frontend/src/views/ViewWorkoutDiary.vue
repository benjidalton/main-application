<script setup>
import { ref } from 'vue';
import BaseMenu from '@/components/BaseComponents/BaseMenu.vue';
import WorkoutTable from '@/components/FitnessTrackerComponents/WorkoutTable.vue';
import { selectWorkoutByDate, selectWorkoutByDateRange } from '@/services/FitnessTrackerService';

const date = ref(new Date());
const diary = ref([]);
const minDate = ref(null);
const maxDate = ref(null);
const dateRange = ref(false);

function handleMinDate(newDate) {
	minDate.value = newDate;
}

function handleMaxDate(newDate) {
	maxDate.value = newDate;
}

async function selectWorkout() {
	if (!dateRange.value) {
		diary.value = await selectWorkoutByDate(minDate.value)
	} else {
		if (minDate.value && maxDate.value) {
			diary.value = await selectWorkoutByDateRange(minDate.value, maxDate.value);
			console.log('diary', diary.value)
		}
		
	}
	
}

function toggleDateRange() {
	dateRange.value = !dateRange.value;
}

</script>

<template>
	<v-container id="diary-container">
		<v-container class="container">
			<v-row align="center" style="justify-content: center;">
				<v-btn @click="toggleDateRange">Date Range</v-btn>
				<v-col cols="3">
					<BaseMenu 
						@dateUpdated="handleMinDate" 
						baseLabel="Choose Date" 
						:datePicker="true"
						icon="mdi-calendar"
						:maxDate="maxDate"
					/>
				</v-col>

				<template v-if="dateRange">
					--

				<v-col cols="3">
					<BaseMenu 
						@dateUpdated="handleMaxDate" 
						baseLabel="Choose Date" 
						:datePicker="true"
						icon="mdi-calendar"
						:minDate="minDate"
					/>
				</v-col>
					
				</template>
				
				<v-col cols="3">
					<v-btn @click="selectWorkout">
						Get Workout From Date
					</v-btn>
				</v-col>
			</v-row>
				
		</v-container>
		<WorkoutTable v-if="diary.length > 0" :items="diary"/>
	</v-container>
</template>


<style scoped>

#diary-container {
	width: 60vw;
	margin-top: 100px; 
}

.container {
	width: 1200px;
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