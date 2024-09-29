<script setup>
import { LLMQuery } from '@/models/LLMQuery';
import { ref, onBeforeMount } from 'vue';

const props = defineProps({
	query: {
		type: LLMQuery,
		required: true
	}
});

const formattedQuery = ref(null);

onBeforeMount(() => {
	if (props.query) {
		formattedQuery.value = formatAnswerWithContext(props.query)
	}
})

function formatAnswerWithContext(query) {
	let updatedText = query.answerWithContext;
	query.itemUrls.forEach(item => {
		const nameRegex = new RegExp(item.name, 'g'); 
		const itemLink = `<a href="${item.baseballReferenceUrl}" target="_blank">${item.name} </a><i class="mdi mdi-open-in-new"></i>` ;
		updatedText = updatedText.replace(nameRegex, itemLink);
		return updatedText;
	})
	query.formattedResponse = updatedText;
	
	return query
}

function copyQueryToClipboard(copyText) {
	navigator.clipboard.writeText(copyText)
}

</script>

<template>
	<v-col cols="12" md="6" class="text-center">
		<v-tooltip activator="parent" location="top" class="formatted-sql" :text="formattedQuery.rawSqlQuery">
			<template v-slot:activator="{ props }">
				<v-card v-bind="props" class="pa-3 d-flex align-center justify-space-between" outlined>
					<v-card-text>
						<v-row class="message-row" justify="end">
							{{ formattedQuery.originalPrompt }}
						</v-row>
						<v-row class="message-row" justify="start">
							<span class="formatted-response" v-html="formattedQuery.formattedResponse"></span>
						</v-row>
						 
					</v-card-text>
					<v-btn icon @click="copyQueryToClipboard(formattedQuery.rawSqlQuery)" class="ml-2">
						<v-icon>mdi-content-copy</v-icon>
					</v-btn>
					</v-card>
			</template>
		</v-tooltip>
	</v-col>
</template>

<style>

.formatted-sql {
	white-space: pre; /* Preserve the newlines and spaces */
	font-family: monospace; /* Optional: for a code-like appearance */
}

.message-row {
	padding: 10px;
	color: black;
}
.formatted-response {
	color: black;
}

.formatted-response a {
	color: black;
	text-decoration: none; 
}

.formatted-response a:hover {
	text-decoration: underline;
}

.formatted-response i.mdi {
  font-size: 16px;
}

</style>