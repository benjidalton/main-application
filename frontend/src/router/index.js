import { createRouter, createWebHistory } from "vue-router";

const routes = [
	{
		path: '/',
		name: '/',
		component: () => import('../views/Login.vue')
	},

	{
		path: '/baseball',
		name: 'baseball',
		redirect: {
			name: 'baseball-LLM'
		},
		component: () => import('../views/BaseballStats.vue')
	},
	{
		path: '/baseball/LLM',
		name: 'baseball-LLM',
		component: () => import('../views/LLM.vue')
	},
	{
		path: '/blackjack',
		name: 'blackjack',
		component: () => import('../views/CardGameViews/Blackjack.vue')
	},
	{
		path: '/solitaire',
		name: 'solitaire',
		component: () => import('../views/CardGameViews/Solitaire.vue')
	},
	{
		path: '/fitness-tracker',
		name: 'fitness-tracker',
		component: () => import('../views/FitnessTrackerViews/WorkoutDiaryEntry.vue'),
	},
	{
		path: '/fitness-tracker/new-workout-diary',
		name: 'new-workout-diary',
		component: () => import('../views/FitnessTrackerViews/WorkoutDiaryEntry.vue')
	},
	{
		path: '/fitness-tracker/view-diary',
		name: 'view-diary',
		component: () => import('../views/FitnessTrackerViews/ViewWorkoutDiary.vue')
	},
	{
		path: '/about',
		name: 'about',
		component: () => import('../views/About.vue')
	}
]

const router = createRouter({
	history: createWebHistory(),
	routes
})

export default router;