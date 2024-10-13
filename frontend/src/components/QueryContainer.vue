<script setup>
import { LLMQuery } from '@/models/LLMQuery';
import { ref, onBeforeMount } from 'vue';

const props = defineProps({
	query: {
		type: LLMQuery,
		required: true
	},
	loading: {
		type: Boolean
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
	if ( query.itemUrls )
		// if its a response that actually got data from db, it will hopefully have urls
		// else it wil be a response thats just explaining that it couldn't create a good 
		// query with the database schema provided
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
	<v-container class="query-container"> 
		<v-tooltip activator="parent" location="top" class="formatted-sql text-center" :text="formattedQuery.toolTipString">
			<template v-slot:activator="{ props }">
				<v-card v-bind="props" class="card" outlined>
					<v-card-text>
						<v-row class="message-row" justify="end">
							{{ formattedQuery.originalPrompt }}
						</v-row>
						<v-row class="message-row" justify="start">
							<span class="formatted-response" v-html="formattedQuery.formattedResponse"></span>
						</v-row>
						 
					</v-card-text>
					<v-btn icon @click="copyQueryToClipboard(formattedQuery.toolTipString)" class="ml-2">
						<v-icon>mdi-content-copy</v-icon>
					</v-btn>
					
				</v-card>
			</template>
		</v-tooltip>
		<p class="hover-text">Hover me to see SQL query used</p>
	</v-container>
	
</template>

<style>
.query-container {
	width: 70%;
}

.query-container .card {
	padding: 16px; 
	display: flex;
	align-items: center;
	justify-content: space-between;
	background-color: var(--custom-card-bg-opacity);
}

.formatted-sql {
	white-space: pre; /* Preserve the newlines and spaces */
	font-family: monospace; /* Optional: for a code-like appearance */
}

.message-row {
	padding: 10px;
	color: black;
	font-size: 20px;
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

.hover-text {
	color: rgba(0, 0, 0, 0.5);
	font-size: 12px;
	text-align: center;
	margin-top: 8px;
}

</style>