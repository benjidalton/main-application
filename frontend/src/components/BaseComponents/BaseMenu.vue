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
	icon: String

})

const chosenItem = ref('');

const chosenDate = ref(new Date()); 
const emit = defineEmits(['itemChosen', 'openDialog', 'dateUpdated'])

function onItemChosen(item) {
	chosenItem.value = item;
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
		let newDate = chosenDate.value.toISOString().split('T')[0];
		emit('dateUpdated', newDate);
		return newDate;
	} 
})

</script>


<template>
	
	<v-menu 
	>
		<template v-slot:activator="{ props }">
			<v-card class="custom-card" v-bind="props">
				<v-card-title>
					<template v-if="icon && (!chosenItem || !chosenDate)">
						<v-icon :icon="icon" size="small" style="position: relative; right: 10%;"/>
					</template>
					<span class=""> <!-- Add some margin for spacing -->
						{{ datePicker ? (chosenDate ? dateFormat : baseLabel) : (chosenItem ? capitalizeWords(chosenItem) : baseLabel) }}
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
			/>
		</template>
	</v-menu>
</template>

<style scoped>
.custom-card {
	cursor: pointer;
	background-color: rgb(121, 119, 156);
	color: white;
	padding: 5px;
}
.custom-card:hover {
	transform: scale(110%);
}
</style>