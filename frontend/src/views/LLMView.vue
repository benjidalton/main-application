<script setup>
import { ref } from 'vue';
import { fetchLLMResponse } from '@/services/LLMService';
import PromptInput from '@/components/PromptInput.vue';
import QueryContainer from '@/components/QueryContainer.vue';
import ExamplePromptsPanel from '@/components/ExamplePromptsPanel.vue';

const llmQueries = ref([]);
const customPromptEntered = ref(false);
const showExamplePrompts = ref(true);

async function onUserPrompt(prompt, promptType) {
	customPromptEntered.value = true;
	let query = await fetchLLMResponse(prompt, promptType);
	llmQueries.value.push(query);
}

function onPromptClicked(prompt) {
	console.log('This prompt was clicked: ', prompt)
}

function onPromptTypeChanged(promptType) {
	if (promptType == 'DB Query') {
		showExamplePrompts.value = true;
	} else {
		showExamplePrompts.value = false;
	}
}

</script>

<template>
	<v-container class="container" fluid>
		<ExamplePromptsPanel v-if="showExamplePrompts"  @promptClicked="onPromptClicked" :customPromptEntered="customPromptEntered"/>
		<div class="scrollable-wrapper">
			<template v-if="llmQueries.length > 0" v-for="(query, index) in llmQueries" :key="index">
				<QueryContainer :query="query"/>
			</template>
		</div>


		<v-container class="prompt-wrapper">
			<PromptInput @userPrompt="onUserPrompt" @promptTypeChanged="onPromptTypeChanged"/>
		</v-container>
	</v-container>
</template>


<style scoped>
.container {
	position: relative;
	display: flex;
	flex-direction: column;
	padding: 0;
	margin-top: 70px;
	box-sizing: border-box;
	justify-content: center;
	align-content: center;
	align-items: center;
	overflow-y: hidden;
	
	height: calc(100vh - 70px);

	background-color: rgb(247, 247, 247);
	
}

.scrollable-wrapper {
	position: relative;
	display: flex;
	height: 80vh;
	overflow-y: auto; 
	overflow-x: hidden;
	padding: 10px; 
	width: 80vw;
	border: 5px solid blue;
	margin-bottom: 40px;
	margin-top: 20px;
	justify-content: center;
	align-content: center;
	align-items: center;
}

.prompt-wrapper {
	position: relative;
	width: 100%;
	justify-content: center;
	/* margin-top: 10px; */
	bottom: 5%;
}

#logo-container {
	border: 2px solid gray;
	background-color: aliceblue;
}

</style>