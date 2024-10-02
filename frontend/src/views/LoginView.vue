<script setup>
//imports
import { ref, computed } from 'vue';
import { useAuthStore } from '@/store';
import useVuelidate from '@vuelidate/core';
import { required, helpers } from '@vuelidate/validators';
import { useRouter } from 'vue-router';

//computed vars
const emailRules = computed(() => [
	v => !!v || 'Email is required',
	v => /.+@.+\..+/.test(v) || 'Email must be valid',
]);
const passwordRules = computed(() => [
	v => !!v || 'Password is required',
]);
const emailErrors = computed(() => {
	return v$.value.username.$errors.map(e => e.$message);
});
const passwordErrors = computed(() => {
	return v$.value.password.$errors.map(e => e.$message);
});

//reactive vars
const username = ref('');
const password = ref('');
const servererror = ref(false);
const router = useRouter();
const authStore = useAuthStore();
const v$ = useVuelidate({
	username: { required },
	password: { required },
	}, { username, password }
);

//functions
const authenticate = async () => {
	v$.value.$touch();
	await v$.value.$validate();
	if (v$.value.$error) {
		return; // validation failed
	}

	const formData = {
		username: username.value,
		password: password.value,
	};
	try {
		await authStore.login(formData);
		// Redirect on success
		router.push('/dashboard');
	} catch (error) {
		servererror.value = true;
		console.error(error);
	}
};


</script>

<template>
	<v-container fluid style="padding-top: 100px;">
		<v-form @submit.prevent="authenticate">
			<v-card>
				<v-card-title>
				<h3>Sign In</h3>
				</v-card-title>

				<v-card-subtitle style="padding: 20px;">
					<v-text-field
						v-model="username"
						label="Username"
						outlined
						dense
						:error-messages="emailErrors"
						autocomplete="username"
						required
					></v-text-field>

					<v-text-field
						v-model="password"
						type="password"
						label="Password"
						outlined
						dense
						:error-messages="passwordErrors"
						@keyup.enter="authenticate"
						autocomplete="current-password"
						required
					></v-text-field>

					<v-row>
						<v-col cols=6>
							<v-btn
								@click="console.log('register button clicked')"
								color="blue"
							>
								<v-icon icon="mdi-account-plus" style="padding-right: 10px;"/>
								Register
							</v-btn>
						</v-col>
						<v-col cols=6>
							<v-btn
								@click="console.log('sign-in button clicked')"
								color="blue"
							>
							<v-icon icon="mdi-login" style="padding-right: 10px;"/>
								Sign In
							</v-btn>
						</v-col>
					</v-row>
				</v-card-subtitle>
			</v-card>
		</v-form>
	</v-container>
</template>
  
<style scoped>
.v-card {
	max-width: 500px;
	margin: auto;
}
</style>
  