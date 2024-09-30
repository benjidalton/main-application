<script setup>
import { ref, computed, onMounted  } from 'vue';

const showTechBox = ref(false); // State to control the visibility of the tech box
const toggleTechBox = () => {
	showTechBox.value = !showTechBox.value; // Toggle the visibility
};

</script>

<template>
	<v-app-bar id="topNavBar" app  elevated>
		<v-row align="center" no-gutters style="padding-right: 40px; position: relative; overflow: visible;">
			<!-- <v-col cols="auto">
				<v-btn class="ml-2" variant="flat" color="red">
					Click Me 
				
				</v-btn>
			</v-col> -->
			<v-spacer></v-spacer>
	
			<v-col cols="auto" style="padding-right: 40px; position: relative; overflow: visible;">
				<v-btn
					href="https://github.com/kcbdalton" 
					target="_blank"  
					icon
				>
					<v-icon size="40px">
						mdi-github  <!-- Material Design Icons GitHub icon -->
					</v-icon>
				</v-btn>
				<v-btn icon @click="toggleTechBox">
					<v-icon size="30px">
						mdi-information-slab-circle-outline  <!-- Material Design Icons GitHub icon -->
					</v-icon>
				</v-btn>
				<v-expand-transition>
					<div v-if="showTechBox" class="tech-box" style="">
						<strong>Technologies used:</strong>
						<div style="display: flex; gap: 10px; margin-top: 5px;">
							<v-icon>mdi-vuejs</v-icon>
							<v-icon>mdi-vuetify</v-icon>
							<v-icon>mdi-language-python</v-icon>
							<v-icon>mdi-microsoft-visual-studio-code</v-icon>
							<v-icon>mdi-nodejs</v-icon>
						</div>
					</div>
				</v-expand-transition>
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
	overflow: visible; 
	z-index: 100;
}

.tech-box {
	box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
	border-radius: 4px;
	position: absolute; 
	background: white; 
	border: 1px solid #ccc; 
	padding: 10px; 
	z-index: 1000 !important;
	right: 200px;
	top: -2px;
}

</style>