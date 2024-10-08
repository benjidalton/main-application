export class Exercise {
	constructor(id, name, date, muscleGroupId, muscleGroup, sets, reps, totalReps, weight) {
		this.id = id;
		this.name = name;
		this.date = date;
		this.muscleGroupId = muscleGroupId;
		this.muscleGroup = muscleGroup;
		this.sets = sets ? sets : 4;
		this.reps = reps ? reps : ["", "", "", ""];
		this.totalReps = totalReps;
		this.weight = weight;
		 // Initialize totalReps
    }

    // Method to calculate total reps
    calculateTotalReps() {
        this.totalReps = this.reps
            .map(rep => parseInt(rep, 10))
            .filter(num => !isNaN(num))
            .reduce((acc, curr) => acc + curr, 0);
    }
	
}