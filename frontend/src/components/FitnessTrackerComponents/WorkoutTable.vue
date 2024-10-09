<script setup>
import { ref, watch } from 'vue';
import TableSearchBar from '../TableSearchBar.vue';
const props = defineProps({
	items: Array
});

watch((props.items), newValues => {
	console.log('new values: ', newValues)
})

const search = ref('');

const headers = ref([
	{ text: 'Date', value: 'date' },
	{ text: 'Muscle Group', value: 'muscleGroup' },
	{ text: 'Exercise', value: 'name' },
	{ text: 'Sets', value: 'sets' },
	{ 
		text: 'Reps',
		children: [
            { text: 'Set 1', value: 'reps.0' },
            { text: 'Set 2', value: 'reps.1' },
			{ text: 'Set 3', value: 'reps.2' },
			{ text: 'Set 4', value: 'reps.3' },
		]
	},
	{ text: 'Weight (lb)', value: 'weight' }
])

function capitalizeWords(string) {
	return string
		.split(' ') // Split the string into words
		.map(word => word.charAt(0).toUpperCase() + word.slice(1)) // Capitalize the first letter of each word
		.join(' '); // Join the words back into a single string
	}

function handleSearch(newSearch) {
	search.value = newSearch;
}

</script>

<template>
	<TableSearchBar @seachText="handleSearch" />
	<v-data-table
		:headers="headers"
		:items="items"
		class="elevation-1"
		:search="search"
		@click="console.log('items', items)"
	>
		<template v-slot:headers="{ columns }" >
			<tr id="header-row" >
				<template v-for="column in columns" :key="column.key">
				<td>
					<span class=" cursor-pointer">{{ column.text }}</span>
				</td>
				</template>
			</tr>
		</template>	
		<template v-slot:item.date="{ item }">
			{{ item.date[0] }}
		</template>
		<template v-slot:item.muscleGroup="{ item }">
			{{ capitalizeWords(item.muscleGroup) }}
		</template>
		<template v-slot:item.name="{ item }">
			{{ capitalizeWords(item.name) }}
		</template>
		<template v-slot:item.reps="{ item }">
			<td>
				<template v-for="(rep, index) in item.reps" :key="index">
					<v-text-field 
						v-model="item.reps[index]" 
						type="number" 
						placeholder="Reps" 
						style="width: 100px;" 
						:label="`Set ${index + 1}`" 
					/>
				</template>
			</td>
		</template>
	</v-data-table>

</template>

<style scoped>
#header-row {
	background-color: rgb(110 126 141);
	font-weight: bold;
	font-size: 24px;
	color: #f0f0f0;
	font-family: 'Poppins';
}

</style>