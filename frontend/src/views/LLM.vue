<script setup>
import { ref } from 'vue';
import { fetchLLMResponse } from '@/services/LLMService';
import BaseViewContainer from '@/components/BaseComponents/BaseViewContainer.vue';
import PromptInput from '@/components/PromptInput.vue';
import QueryContainer from '@/components/QueryContainer.vue';
import ExamplePromptsPanel from '@/components/ExamplePromptsPanel.vue';
import TypingIndicator from '@/components/TypingIndicator.vue';

import { LLMQuery } from '@/models/LLMQuery';

const llmQueries = ref([]);
const customPromptEntered = ref(false);
const showExamplePrompts = ref(true);
const currentPromptType = ref('DB Query');
const loading = ref(false);

async function sendPrompt(prompt) {
	loading.value = true;
	let query = await fetchLLMResponse(prompt, currentPromptType.value);
	llmQueries.value.push(query);
	loading.value = false;
	
}

function onUserPrompt(prompt, promptType) {
	customPromptEntered.value = true;
	currentPromptType.value = promptType;
	sendPrompt(prompt);
	
}

function onPromptClicked(prompt) {
	console.log('This prompt was clicked: ', prompt)
	sendPrompt(prompt);

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
	<BaseViewContainer>
		<ExamplePromptsPanel v-if="showExamplePrompts"  @promptClicked="onPromptClicked" :customPromptEntered="customPromptEntered"/>
		<div class="scrollable-wrapper">
			<template v-if="llmQueries.length > 0" v-for="(query, index) in llmQueries" :key="index">
				<QueryContainer :query="query"/>
			</template>
			<template v-if="loading">
				<TypingIndicator />
			</template>
		</div>


		<v-container class="prompt-wrapper">
			<PromptInput @userPrompt="onUserPrompt" @promptTypeChanged="onPromptTypeChanged"/>
		</v-container>
	</BaseViewContainer>
	
</template>


<style scoped>


.scrollable-wrapper {
	position: relative;
	display: flex;
	height: 80vh;
	overflow-y: auto; 
	overflow-x: hidden;
	padding: 10px; 
	width: 80vw;
	/* border: 5px solid blue; */
	margin-bottom: 40px;
	margin-top: 20px;
	flex-direction: column
	/* justify-content: center;
	align-content: center;
	align-items: center; */
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