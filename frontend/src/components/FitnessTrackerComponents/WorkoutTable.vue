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
const mousePosition = ref({x: 0, y: 0});
const displayChart = ref(false);
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
	{ text: 'Actions', value: 'actions', sortable: false }
])

const chartStyle = computed(() => ({
	display: displayChart.value,
	position: 'absolute',
	left: `${mousePosition.value.x}px`,
	top: `${mousePosition.value.y}px`,
	zIndex: 1000,
}));


function handleSearch(newSearch) {
	search.value = newSearch;
}

function createGraph(newData, event) {
	mousePosition.value.x = event.clientX + 10;
	mousePosition.value.y = event.clientY - 100;
	chartData.value = newData;
	displayChart.value = 'block';

}
function hideChart() {
	chartData.value = null;
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
		<template v-slot:item.exercise="{ item }">
			{{ capitalizeWords(item.exercise) }}
		</template>
		<template v-slot:item.actions="{ item }">
			<v-card id="graph-icon" @mouseover="(event) => createGraph(item, event)" @mouseleave="hideChart" >
					<v-icon icon="mdi-chart-areaspline-variant" />
			</v-card>
			
		</template> 
		<template v-slot:footer>
			<v-row>
				<v-col class="d-flex justify-end">
					<v-btn color="primary">Custom Button</v-btn>
				</v-col>
			</v-row>
		</template>
	</v-data-table>

	<div v-if="chartData" class="chart-popup" :style="chartStyle">
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