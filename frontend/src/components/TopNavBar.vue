<script setup>
import { ref, computed, onMounted  } from 'vue';

</script>

<template>
	<v-app-bar id="topNavBar" app  elevated>
		<v-row align="center" no-gutters>
			<v-col cols="auto">
				<v-btn class="ml-2" variant="flat" color="red">
					Click Me 
				
				</v-btn>
			</v-col>
			<v-spacer></v-spacer>
	
			<v-col cols="auto" style="padding-right: 20px;">
				<!-- <v-btn v-if="!isAuth" :to="{ name: 'login' }" class="mr-2" variant="text" :color="buttonColor">Sign in</v-btn>
				<v-btn v-if="isAuth" :to="{ name: 'AddApplication' }" class="mr-2" variant="text" :color="buttonColor">Add App</v-btn>
				<v-btn v-if="isAuth" :to="{ name: 'kcApps' }" class="mr-2" variant="text" :color="buttonColor">Knox County Apps</v-btn> -->
				
				<!-- <v-btn v-if="isAuth" :to="{ name: 'addApp' }">Add App</v-btn>  -->


			</v-col>
		</v-row>
	</v-app-bar>
</template>

<style>
/* !important means dont overwrite */
.router-link-active {
	color: #007bff !important;
}

.button {
	margin-right: 10px;
}

#topNavBar {
	background-color: rgb(62, 81, 121);
}

</style>