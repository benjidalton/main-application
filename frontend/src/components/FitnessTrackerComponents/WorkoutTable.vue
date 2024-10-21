<script setup>
import { ref, watch, computed } from 'vue';
import TableSearchBar from '../TableSearchBar.vue';
import CustomChart from '@/components/CustomChart.vue';
import { capitalizeWords } from '@/services/UtilService';

const props = defineProps({
	items: Array
});

const emit = defineEmits(['newChartData'])

watch((props.items), newValues => {
	console.log('new values: ', newValues)
})

const search = ref('');
const chartData = ref([]);

const headers = ref([
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
	{ text: 'Weight (lb)', value: 'weight' },
])

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
		item-value="value"
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
		<template v-slot:item.name="{ item }">
			{{ capitalizeWords(item.name) }}
		</template>
		<template v-slot:footer>
			<v-row>
				<v-col class="d-flex justify-end">
					<v-btn color="primary">Custom Button</v-btn>
				</v-col>
			</v-row>
		</template>
	</v-data-table>

	<div v-if="chartData" class="chart-popup" >
	    <!-- Your chart implementation goes here -->
	    <CustomChart :data="chartData" />
	  </div>

</template>

<style scoped>
#header-row {
	background-color: var(--custom-card-bg-opacity);
	font-weight: bold;
	font-size: 20px;
	color: #000000;
	font-family: 'Poppins';
}

#graph-icon {
	width: 50px;
	height: 50px;
	align-items: center;
	justify-content: center;
}
.chart-popup {
	display: none;
	border: 1px solid #ccc;
	background: white;
	padding: 10px;
	border-radius: 5px;
	width: 400px;
	aspect-ratio:  2 / 1;
}

#group-row {
	background-color:  rgb(239, 251, 255);
	border-radius: 10px;
}

</style>