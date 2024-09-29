<script setup>
import { ref } from 'vue';
import { fetchLLMResponse } from '@/api/llmAPI';
import PromptInput from '@/components/PromptInput.vue';
import QueryContainer from '@/components/QueryContainer.vue';

const llmQueries = ref([]);

async function onUserPrompt(prompt, promptType) {
	let query = await fetchLLMResponse(prompt, promptType);
	llmQueries.value.push(query);
}

</script>

<template>
	<v-container class="container fill-height">
		<template v-if="llmQueries.length > 0">
			<v-row v-for="(query, index) in llmQueries" :key="index"  justify="center" align="center" class="mt-4">
				<QueryContainer :query="query"/>
			</v-row>
		</template>
		<PromptInput @userPrompt="onUserPrompt" /> 
	</v-container>
</template>


<style scoped>
.container {
	height: 90vh; 
	width: 100vw;
	padding: 0;
	border: 2px solid red;
	overflow: hidden;
}

.fill-height {
	display: flex;
	flex-direction: column;
	justify-content: space-between; /* To ensure the input stays at the bottom */
}

#logo-container {
	border: 2px solid gray;
	background-color: aliceblue;
}

</style>