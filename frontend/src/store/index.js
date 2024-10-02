import { defineStore } from 'pinia';
import axios from 'axios';
import router from '@/router';

export const useAuthStore = defineStore('auth', {
	state: () => ({
		username: null,
		token: null,
	}),
	actions: {
		async login(authData) {
			console.log("Login URL: {" + import.meta.env.VITE_APP_LOGIN_URL + "}");

			try {
				const response = await axios.post(
					import.meta.env.VITE_APP_LOGIN_URL,
					{
						username: authData.username,
						password: authData.password,
					}
				)
				console.log("Received Success")
				this.username = authData.username
				this.token = response.data.token
				localStorage.setItem("token", response.data.token)
				localStorage.setItem("email", authData.username)
				return response
			} catch (error) {
				throw error.response
			}
		},

		autoLogin() {
			const token = localStorage.getItem("token")
			const username = localStorage.getItem("username")

			if (token && email) {
				this.username = username
				this.token = token
			}
		},

		logout() {
			this.username = null
			this.token = null
			localStorage.removeItem("username")
			localStorage.removeItem("token")
			router.replace("login")
		},

		getEmail() {
			return localStorage.getItem("username")
		},
	},
	getters: {
		isAuthenticated: (state) => !!state.token,
	},
})
