
<script setup>
import { ref } from 'vue';

const showPanel = ref(false);

const prop = defineProps({
	customPromptEntered: {
		type: Boolean
	}
})
const emit = defineEmits(['promptClicked']);

const promptSelected = ref(false);
const prompts = [
	'Who hit the most home runs?', 
	'Which team had the most wins?', 
	'Which pitcher allowed the most walks?', 
	'Which American League team hit the most doubles?', 
	"Can you give me a summary of Shohei Ohtani's season?"
];

function handleClick(promptLabel) {
	emit('promptClicked', promptLabel);
	promptSelected.value = true;
};

</script>

<template>
	<v-menu transition="scale-transition" >
		<template v-slot:activator="{ props }">
			<v-btn
				class="open-panel-button"
				v-bind="props"
			>
			<v-icon size="30px">mdi-menu</v-icon>
			Example Prompts
		</v-btn>
		</template>
		<v-list id="prompts-list">
			<v-list-item
				v-for="(prompt, index) in prompts"
				:key="index"
				style="cursor: pointer;"
			>
			<v-list-item-title v-text="prompt" @click="handleClick(prompt)"></v-list-item-title>
			</v-list-item>
		</v-list>
	</v-menu>

</template>


<style scoped>
.open-panel-button {
	position: absolute;
	bottom: 0;
	right: 0;
	z-index: 1000;
	transition: transform 0.3s ease;
	height: 50px;
	width: fit-content;
	color: rgb(50, 62, 73);
}

#prompts-list {
	background-color: rgb(255, 255, 255);
}

.v-list-item:hover {
  background-color: rgba(100, 150, 200, 0.3); /* Change to your desired color */
}
</style>