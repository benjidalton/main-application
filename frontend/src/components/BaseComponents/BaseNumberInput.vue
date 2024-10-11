<script setup>
import { ref } from 'vue';

const model = ref('')

function  handleClick(direction) {
	// Handle the click event for the icons
	console.log(`${direction} icon clicked`);
}

</script>

<template>
	<v-container style="align-items: center; justify-content: center;">
		<v-row align="center" justify="center">
			<v-text-field 
				v-model="model"
				bg-color="inherit"
				
				variant="solo"
				class="custom-field"
			>
			<template v-slot:append-inner>
				<v-col class="d-flex flex-column align-center">
					<v-icon
						@click="handleClick('up')" 
						icon="mdi-arrow-up-drop-circle-outline" 
						size="large" 
						class="input-btn"
					/>

					<v-icon 
						@click="handleClick('down')" 
						icon="mdi-arrow-down-drop-circle-outline" 
						size="large" 
						class="input-btn"
					/>
			</v-col>

   			</template>
			</v-text-field>
			

		</v-row>
	</v-container>
	
</template>

<style>
.input-btn {
	cursor: pointer;
}

.input-btn:hover	 {
	transform: scale(120%);
}

.custom-field {
	margin-top: 20px;
}
</style>