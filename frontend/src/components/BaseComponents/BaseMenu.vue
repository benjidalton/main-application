<script setup>
import { onMounted, ref, computed } from 'vue';

const props = defineProps({
	baseLabel: String,
	menuItems: Array,
	addExercise: {
		type: Boolean,
		default: false
	},
	datePicker: {
		type: Boolean,
		default: false
	},
	minDate: String,
	maxDate: String,
	icon: String,
	multiple: Boolean
})

const chosenItem = ref('');
const allChosen = ref(true);
const chosenDate = ref(null); 

const emit = defineEmits(['itemChosen', 'openDialog', 'dateUpdated', 'allItemsChosen'])
defineExpose({ resetLabel, chosenItem })

function resetLabel() {
	chosenItem.value = '';
	allChosen.value = false;
}

function onItemChosen(item) {
	chosenItem.value = item;
	allChosen.value = false; // reset allChosen so the new chosen item will be displayed in card
	console.log('item chosen: ', chosenItem.value)
	emit('itemChosen', item);
}

function openDialog() {
	emit('openDialog');
}

function capitalizeWords(string) {
	return string
		.split(' ') // Split the string into words
		.map(word => word.charAt(0).toUpperCase() + word.slice(1)) // Capitalize the first letter of each word
		.join(' '); // Join the words back into a single string
}

const dateFormat = computed(() => {
	if (chosenDate.value) {
		let newDate;
		if (chosenDate.value.length > 1) {
			// chosenDate.value is an array
			newDate = handleDateArray(chosenDate.value);
		} else {
			// chosenDate.value is not an array (handle single date case)
			newDate = handleSingleDate(chosenDate.value);
		}
		return newDate;
	} 
})

function chooseAll() {
	allChosen.value = true;
	emit('allItemsChosen')
}


function handleDateArray(dates) {
	// Emit the formatted dates immediately for database queries
	let formattedDates = dates.map(date => date.toISOString().split('T')[0]);
	emit('dateUpdated', formattedDates);

	// Prettier label
	// idk why using first index of formattedDates is one day earlier than the user pressed??? 
	// have to take first index instead
	// the correct dates are in 'formattedDates' so they can be emitted to backend without issue so idk why this breaks
	const firstDate = new Date(formattedDates[1]);
	const lastDate = new Date(formattedDates[formattedDates.length - 1]);

	// Format dates as (MM/DD)
	const options = { month: 'numeric', day: 'numeric' };
	const formattedFirstDate = firstDate.toLocaleDateString(undefined, options);
	console.log('formatted first date', formattedFirstDate)
	const formattedLastDate = lastDate.toLocaleDateString(undefined, options);
	
	// Display in the format: "First Date - Last Date"
	return `${formattedFirstDate} - ${formattedLastDate}`;
}

function handleSingleDate(date) {
    // Process the single date
    const formattedDate = new Date(date).toISOString().split('T')[0]; // Ensure it's treated as a date object
    emit('dateUpdated', [formattedDate]);
	return formattedDate 
}

</script>


<template>

		<v-menu :return-value.sync="chosenDate" :close-on-content-click="datePicker && multiple? false : true">

		<template v-slot:activator="{ props }">
			<v-card class="custom-card" v-bind="props">
				<v-card-title>
					<template v-if="icon && (!chosenItem || !chosenDate)">
						<v-icon :icon="icon" size="small" style="position: relative; right: 10%;"/>
					</template>
					<span class=""> <!-- Add some margin for spacing -->
						{{ datePicker ? (chosenDate ? dateFormat : baseLabel) : (allChosen ? baseLabel : chosenItem ? capitalizeWords(chosenItem) : baseLabel) }}
					</span>
				</v-card-title>

			</v-card>
		</template>

		<v-list>
			<v-list-item 
				v-if="addExercise"
				@click="openDialog">
				Add Exercise
				<v-icon icon="mdi-plus"/>
				
			</v-list-item>

			<v-list-item 
				v-if="multiple && !datePicker"
				@click="chooseAll">
					All
				<v-icon icon="mdi-plus"/>
				
			</v-list-item>
			<v-list-item 
				v-for="(item, index) in menuItems" 
				:key="index" 
				@click="onItemChosen(item.toLowerCase())"
			>
			{{ capitalizeWords(item) }}
			</v-list-item>
		</v-list>


		<template v-if="datePicker">
			<v-date-picker
				v-model="chosenDate"
				no-title
				hide-actions
				style="font-size: 10px;"
				:min="minDate ? minDate : null"
				:max="maxDate ? maxDate : null"
				:multiple="multiple ? 'range' : null"
			/>
		</template>
	</v-menu>
</template>

<style scoped>
.custom-card {
	cursor: pointer;
	background-color: var(--custom-card-bg);
	color: rgb(75, 75, 75);
	padding: 5px;
}
.custom-card:hover {
	transform: scale(110%);
}
</style>