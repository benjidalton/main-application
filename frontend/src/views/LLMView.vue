<script setup>
import { ref } from 'vue';
import { fetchLLMResponse } from '@/api/llmAPI';
import PromptInput from '@/components/PromptInput.vue';
import QueryContainer from '@/components/QueryContainer.vue';

const llmQueries = ref([]);
const loading = ref(null);

async function onUserPrompt(prompt, promptType) {
	let query = await fetchLLMResponse(prompt, promptType);
	llmQueries.value.push(query);
}

</script>

<template>
	<v-container class="container">
		<div class="scrollable-wrapper">
			<template v-if="llmQueries.length > 0" v-for="(query, index) in llmQueries" :key="index">
				<QueryContainer :query="query"/>
			</template>
		</div>


		<v-container class="prompt-wrapper">
			<PromptInput @userPrompt="onUserPrompt" />
		</v-container>
	</v-container>
</template>


<style scoped>
.container {
	height: 100vh; /* Full viewport height */
	width: 100vw; /* Full viewport width */
	display: flex;
	flex-direction: column;
	padding: 0;
	margin: 0;
	box-sizing: border-box;
	justify-content: center;
	align-content: center;
	transform: translate(5%);
	overflow-y: hidden;
}

.scrollable-wrapper {
	height: 80vh;
	overflow-y: auto; 
	padding: 10px; 
}

.prompt-wrapper {
	position: relative;
	width: 100%;
	justify-content: center;
	margin-top: 10px;
	bottom: 5%;
}


#logo-container {
	border: 2px solid gray;
	background-color: aliceblue;
}

</style>