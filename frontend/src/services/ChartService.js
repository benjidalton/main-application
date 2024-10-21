import { Legend } from "chart.js";
const colorMap = new Map();
class ChartDataSet {
	constructor(type, label, data, xAxidID = 'x', yAxisID = 'y') {
		this.type = type;
		this.label = label;
		this.data = data;
		this.color = this.getColor(label);
		this.borderColor = this.color;
		this.backgroundColor = this.getBackgroundColor();
		this.fill = false
		this.tension = 0.1;
		this.xAxidID = xAxidID;
		this.yAxisID = yAxisID;
		if (this.type === 'line') {
			this.pointRadius = 6; // Default point size
			this.pointHoverRadius = 10; // Bigger when hovered
			this.pointBorderColor = this.borderColor; // Border color around points
			this.pointBackgroundColor = this.color; // Fill color for points
			this.pointBorderWidth = 2; // Thickness of the point border
		}
		this.borderWidth = this.type === 'bar' ? 3 : 2; 
	}

	getColor(label) {
		// Select a color based on the current instance index
		if (colorMap.has(label)) {
			return colorMap.get(label); // Return the existing color
		} else {
			// Select a new color and store it in the map
			const index = ChartDataSet.counter % chartColors.length;
			const newColor = chartColors[index];
			colorMap.set(label, newColor); // Map the exercise name to the color
			ChartDataSet.counter++;
			return newColor;
		}
	}
	getBackgroundColor() {
		// If it's a bar chart, make the background color semi-transparent (alpha = 0.2)
		if (this.type === 'bar') {
			const rgbaColor = this.hexToRgba(this.color, 0.2); // Convert hex to rgba with alpha = 0.2
			return rgbaColor;
		}
		return this.color; // For non-bar charts, use the full color as background
	}

	hexToRgba(hex, alpha) {
		// Convert hex color to RGBA format
		let r = parseInt(hex.slice(1, 3), 16);
		let g = parseInt(hex.slice(3, 5), 16);
		let b = parseInt(hex.slice(5, 7), 16);
		return `rgba(${r}, ${g}, ${b}, ${alpha})`;
	}
}
// The ChartDataSet.counter variable keeps track of how many ChartDataSet instances have been created, 
// ensuring that each new instance gets a different color from the predefined list.
ChartDataSet.counter = 0;

const chartColors = [
	'#d1c7c7', // gray
	'#FF6384', // red
	'#36A2EB', // blue
	'#FFCE56', // yellow
	'#4BC0C0', // teal
	'#9966FF', // purple
	'#FF9F40', // orange
	'#FF5733', // coral
	'#C70039', // crimson
	'#900C3F', // dark red
	'#581845'  // dark purple
];


export function createChartData(newData) {
	const labels = [];
	const dataSets = []; 

	let maxReps = 0; 
	if (Array.isArray(newData)) {
		newData.forEach((item, index) => {
			let exerciseName = item.name;
			// Create labels for each set if not already done
			item.reps.forEach((repCount, setIndex) => {
				if (repCount > maxReps) {
					maxReps = repCount;
				}
				if (!labels.includes(`Set ${setIndex + 1}`)) {
					labels.push(`Set ${setIndex + 1}`);
				}
			});

			// Line dataset for reps
			let repsDataSet = new ChartDataSet('line', capitalizeWords(exerciseName), item.reps);
			// Bar dataset for weight, using the right-hand Y-axis
			let weightDataSet = new ChartDataSet('bar', capitalizeWords(exerciseName), [item.weight], 'x2', 'y2');
			dataSets.push(repsDataSet);
			dataSets.push(weightDataSet);
		});
	} else {
		// If it's a single object, use it directly
		newData.reps.forEach((repCount, index) => {
			if (repCount > maxReps) {
				maxReps = repCount;
			}
			labels.push(`Set ${index + 1}`);
		});
		let dataSet = new ChartDataSet('line', capitalizeWords(newData.name), newData.reps);

		dataSets.push(dataSet);
	}
	// Calculate the new max for the y-axis (20% greater than maxWeight)
	const yMax = Math.ceil(maxReps * 1.2);
	return {
		labels,
		datasets: dataSets,
		yMax
	};
}

export function createChartOptions(yMax, dataLength, displayValues = false) {
	return {
		responsive: true,
		plugins: {
			legend: {
				display: false,
				position: 'top',
			},
			datalabels: {
				align: 'end', // Align the labels below the points
				anchor: 'end',
				formatter: (value) => displayValues ? value : "", // Display the value itself
				color: 'black',
				font: {
					size: 12
				},
			},
			datalabels: {
				align: 'top',
 // Anchor them near the center of the line
				formatter: (value, context) => displayValues ? value : (() => {
					const datasetIndex = context.datasetIndex;
					const dataset = context.chart.data.datasets[datasetIndex];

					const totalPoints = dataset.data.length;
					const currentIndex = context.dataIndex;
					const labelPosition = Math.floor(totalPoints / (datasetIndex + 2));
					// Show label around the midpoint of the dataset
  					return currentIndex === labelPosition ? dataset.label : ''
				})(),
				color: (context) => {
					// Customize label color based on dataset
					return context.dataset.borderColor || 'black';
				},
				font: {
					size: 14,
					weight: 'bold'
				},
				clip: false, // Ensure labels don't get clipped if they go outside the chart area
				offset: 30
			}
		},
		scales: {
			x: {
				grid: {
					display: false
				},
				ticks: {
					font: {
						size: 14,
						weight: 'bold' 
					},
					color: 'black'
				}
			},
			x2: {
				type: 'linear',
				position: 'bottom',
				display: false, // Hide the secondary x-axis labels
				grid: {
					display: false
				},
				beginAtZero: true,
				min: 0, // Start at 0
				max: dataLength, // Max should be the length of newData
				ticks: {
					stepSize: 1 // Increment by 1
				}
			},
			y: {
				beginAtZero: true,
				max: yMax,
				grid: {
					display: false
				},
				title: { 
					display: true,
					text: 'Reps',
					font: {
						size: 16,
						weight: 'bold'
					}
				},
				ticks: {
					font: {
						size: 14,
						weight: 'bold' 
					},
					color: 'black'
				}
			},
			y2: { // Right Y-axis for weight
				type: 'linear',
				position: 'right',
				grid: {
					display: false
				},
				title: { 
					display: true,
					text: 'Weight (lb)',
					font: {
						size: 16,
						weight: 'bold'
					}
				},
				ticks: {
					font: {
						size: 14,
						weight: 'bold' 
					},
					color: 'black'
				}
			}
		}
	};
};


function capitalizeWords(string) {
	return string
		.split(' ') // Split the string into words
		.map(word => word.charAt(0).toUpperCase() + word.slice(1)) // Capitalize the first letter of each word
		.join(' '); // Join the words back into a single string
}

function getRandomColor() {
	const letters = '0123456789ABCDEF';
	let color = '#';
	for (let i = 0; i < 6; i++) {
		color += letters[Math.floor(Math.random() * 16)];
	}
	return color;
}
