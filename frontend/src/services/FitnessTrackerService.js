import axios from "axios";
import { MuscleGroup } from "@/models/FitnessTrackerModels/MuscleGroup";
import { Exercise } from "@/models/FitnessTrackerModels/Exercise";
const baseUrl = import.meta.env.VITE_BASE_URL;


export async function getExercisesByMuscleGroup() {
	let appConnectorUrl = baseUrl + import.meta.env.VITE_GET_EXERCISES_BY_MUSCLE_GROUP;
	let muscleGroups = [];
	await axios
		.get(appConnectorUrl, {
			params: {
				maxTimeToWaitSeconds: 30,
				maxResultsToReturn: 500,
			},
		})
		.then((response) => {
			response.data.forEach(muscleGroup => {
				// response is an array of muscle groups from db
				const id = muscleGroup.id;
				const muscleGroupName = muscleGroup.muscleGroupName;
				const listExercises = muscleGroup.exerciseIds ? muscleGroup.exerciseIds.split(',') : [];
				
				// create a new instance of Exercise.js for each exercise for each muscle group
				let muscleGroupExercises = []
				listExercises.forEach((exerciseId, index) => {
					let exerciseName = muscleGroup.exerciseNames.split(',')[index];
					let defaultWeight = muscleGroup.defaultWeights.split(',')[index];
					muscleGroupExercises.push(new Exercise(
						exerciseId,
						exerciseName,
						null,
						id,
						muscleGroupName,
						4,
						["", "", "", ""],
						null,
						null,
						defaultWeight
					));

				})
				muscleGroups.push(new MuscleGroup(id, muscleGroupName, muscleGroupExercises));
			})
		})
		.catch((error) => {
			console.log(error);
		});
	return muscleGroups
}

// export async function insertNewExercise(name, muscleGroupId) {
// 	let appConnectorUrl = baseUrl + import.meta.env.VITE_INSERT_NEW_EXERCISE;
// 	await axios
// 		.post(appConnectorUrl, {
// 			params: {
// 				name: name,
// 				muscleGroupId: muscleGroupId,
// 				maxTimeToWaitSeconds: 30,
// 				maxResultsToReturn: 500,
// 			},
// 		})
// 		.then((response) => {
// 			console.log('post response: ', response)
// 		})
// 		.catch((error) => {
// 			console.log(error);
// 		});
// }
 
export async function insertNewWorkout(workout) {
	let appConnectorUrl = baseUrl + import.meta.env.VITE_INSERT_NEW_WORKOUT;
	await axios
		.post(appConnectorUrl, {
			params: {
				workout: workout,
				maxTimeToWaitSeconds: 30,
				maxResultsToReturn: 500,
			},
		})
		.then((response) => {
			console.log('post response: ', response)
		})
		.catch((error) => {
			console.log(error);
		});
}

export async function selectWorkoutByDate(date) {
	let appConnectorUrl = baseUrl + import.meta.env.VITE_SELECT_WORKOUT_BY_DATE;
	let exercises = [];
	await axios
		.get(appConnectorUrl, {
			params: {
				date: date,
				maxTimeToWaitSeconds: 30,
				maxResultsToReturn: 500,
			},
		})
		.then((response) => {
			response.data.forEach(item => {
				let date = new Date(item.workoutDate).toISOString().split('T')[0];
				let repsArray = item.reps.split(',').map(Number); 
				let exercise = new Exercise(
					item.id, 
					item.name, 
					date, 
					item.muscleGroupId, 
					item.muscleGroup, 
					item.sets, 
					repsArray, 
					item.totalReps, 
					item.weight
				);
				exercises.push(exercise);
			})
		})
		.catch((error) => {
			console.log(error);
		});
	return exercises;
}

export async function selectWorkoutByDateRange(minDate, maxDate) {
	let appConnectorUrl = baseUrl + import.meta.env.VITE_SELECT_WORKOUT_BY_DATE_RANGE;
	let exercises = [];
	await axios
		.get(appConnectorUrl, {
			params: {
				minDate: minDate,
				maxDate: maxDate,
				maxTimeToWaitSeconds: 30,
				maxResultsToReturn: 500,
			},
		})
		.then((response) => {
			console.log(response)
			response.data.forEach(item => {
				let date = new Date(item.workoutDate).toISOString().split('T')[0];
				let repsArray = item.reps.split(',').map(Number); 
				let exercise = new Exercise(
					item.id, 
					item.name, 
					date, 
					item.muscleGroupId, 
					item.muscleGroup, 
					item.sets, 
					repsArray, 
					item.totalReps, 
					item.weight
				);
				exercises.push(exercise);
			})
		})
		.catch((error) => {
			console.log(error);
		});
	return exercises;
}

export async function getWorkouts(searchMuscleGroups, searchExercises, searchDates) {
	let appConnectorUrl = baseUrl + import.meta.env.VITE_GET_WORKOUTS;
	let exercises = [];
	await axios
		.get(appConnectorUrl, {
			params: {
				muscleGroups: Array.isArray(searchMuscleGroups) ? searchMuscleGroups.join(',') : searchMuscleGroups,
				exercises: Array.isArray(searchExercises) ? searchExercises.join(',') : searchExercises,
				dates: Array.isArray(searchDates) ? searchDates.join(',') : searchDates,
				maxTimeToWaitSeconds: 30,
				maxResultsToReturn: 500,
			},
		})
		.then((response) => {
			response.data.forEach(item => {
				let date = new Date(item.workoutDate).toISOString().split('T')[0];
				let repsArray = item.reps.split(',').map(Number); 
				let exercise = new Exercise(
					item.id, 
					item.name, 
					date, 
					item.muscleGroupId, 
					item.muscleGroup, 
					item.sets, 
					repsArray, 
					item.totalReps, 
					item.weight
				);
				exercises.push(exercise);

			})
		})
		.catch((error) => {
			console.log(error);
		});
	return exercises;

}
