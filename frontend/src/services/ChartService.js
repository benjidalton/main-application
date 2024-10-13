class ChartDataSet {
	constructor(label, data) {
		this.label = label;
		this.data = data;
		this.color = getRandomColor();
		this.borderColor = this.color;
        this.backgroundColor = this.color;
        this.fill = false
        this.tension = 0.1;
	}
}

export function createChartData(newData) {
	const labels = [];
    const dataSets = []; 

    if (Array.isArray(newData)) {
		newData.forEach(item => {
            let exerciseName = item.name;

			let dataSet = new ChartDataSet(capitalizeWords(exerciseName), item.reps)

            // Create labels for each set if not already done
            item.reps.forEach((_, index) => {
                if (!labels.includes(`Set ${index + 1}`)) {
                    labels.push(`Set ${index + 1}`);
				}
			});

			dataSets.push(dataSet);
		});
	} else {
		// If it's a single object, use it directly
		newData.reps.forEach((_, index) => {
			labels.push(`Set ${index + 1}`);
		});
		let dataSet = new ChartDataSet(capitalizeWords(newData.name), newData.reps)
		dataSets.push(dataSet);
	}
	return {
        labels,
        datasets: dataSets
    };
}

export function createChartOptions() {
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
            },
            scales: {
                x: {
                    grid: {
                        display: false // Hide grid lines
                    }
                },
                y: {
                    grid: {
                        display: false // Hide grid lines
                    }
                }
            }
        },
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
