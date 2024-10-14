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

watch(() => props.data, (newData) => {
	if (newData) {
		createChart(newData);
	}
    
}, { immediate: true });


function createChart(newSearch) {
	chartData.value = createChartData(newSearch)
	chartOptions.value = createChartOptions(chartData.value.yMax);
	
}


</script>


<template>
	<Line v-if="chartData" :data="chartData" :options="chartOptions"/>

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