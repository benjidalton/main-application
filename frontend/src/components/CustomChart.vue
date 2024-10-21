<script setup>
import { ref, onMounted, watch, computed, inject } from 'vue';
import ChartDataLabels from 'chartjs-plugin-datalabels';
import { Bar, Pie, Doughnut, Line } from 'vue-chartjs';
import {  Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale, ArcElement, LineElement, PointElement, Filler } from 'chart.js';

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale, ArcElement, LineElement, PointElement, Filler, ChartDataLabels)
import { createChartData, createChartOptions } from '@/services/ChartService';

const props = defineProps({
	data: Object
})

const chartData = ref(null);
const chartOptions = ref(null);
const displayValues = ref(false);

watch(() => props.data, (newData) => {
	if (newData) {
		createChart(newData);
	}
    
}, { immediate: true });

watch(displayValues, () => {
	createChart()
})

async function createChart(newSearch) {
	if (newSearch && chartData.value == null) {
		chartData.value = createChartData(newSearch)
	}
	
	chartOptions.value = createChartOptions(chartData.value.yMax, chartData.value.length, displayValues.value); // pass length of data to generate second x axis
}

</script>


<template>
	<v-container>
		<v-checkbox v-model="displayValues" label="Show Values" />
		<Line v-if="chartData" :data="chartData" :options="chartOptions"/>
	</v-container>
	

</template>

<style scoped>
.container {
	height: 700px;
	aspect-ratio: 2 / 1;
	overflow: hidden;
}

/* .chart-container canvas {
	width: 50% !important;
	height: 50% !important;
} */
</style>