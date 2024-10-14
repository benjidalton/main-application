class ChartDataSet {
	constructor(label, data) {
		this.label = label;
		this.data = data;
		this.color = this.getColor();
		this.borderColor = this.color;
		this.backgroundColor = this.color;
		this.fill = false
		this.tension = 0.1;
	}

	getColor() {
        // Select a color based on the current instance index
        const index = ChartDataSet.counter % chartColors.length;
        ChartDataSet.counter++;
        return chartColors[index];
    }
}
// The ChartDataSet.counter variable keeps track of how many ChartDataSet instances have been created, 
// ensuring that each new instance gets a different color from the predefined list.
ChartDataSet.counter = 0;

const chartColors = [
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
		newData.forEach(item => {
			let exerciseName = item.name;

			let dataSet = new ChartDataSet(capitalizeWords(exerciseName), item.reps)
			console.log('item ', item)
			// Create labels for each set if not already done
			item.reps.forEach((repCount, index) => {
				if (repCount > maxReps) {
					maxReps = repCount;
				}
				if (!labels.includes(`Set ${index + 1}`)) {
					labels.push(`Set ${index + 1}`);
				}
			});

			console.log('iotem weight: ', item.weight)

			dataSets.push(dataSet);
		});
	} else {
		// If it's a single object, use it directly
		newData.reps.forEach((repCount, index) => {
			if (repCount > maxReps) {
				maxReps = repCount;
			}
			labels.push(`Set ${index + 1}`);
		});
		let dataSet = new ChartDataSet(capitalizeWords(newData.name), newData.reps);

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

export function createChartOptions(yMax) {
	return {
		responsive: true,
		plugins: {
			legend: {
				display: true,
				position: 'top',
			},
			datalabels: {
				align: 'end', // Align the labels below the points
				anchor: 'end',
				formatter: (value) => value, // Display the value itself
				color: 'black',
				font: {
					size: 12
				},
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
					color: 'black', 
					callback: function(value) {
						return value; // Custom formatting for tick labels
					}
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
					color: 'black', 
					// callback: function(value) {
					// 	return value + ' lb'; // Add ' lb' to each tick label
					// }
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
