import { createRouter, createWebHistory } from "vue-router";

const routes = [
	{
		path: '/',
		name: '/',
		component: () => import('../views/LoginView.vue')
	},
	{
		path: '/baseball',
		name: 'baseball',
		component: () => import('../views/LLMView.vue')
	},

	{
		path: '/about',
		name: 'about',
		component: () => import('../views/AboutView.vue')
	}
]

const router = createRouter({
	history: createWebHistory(),
	routes
})

export default router;