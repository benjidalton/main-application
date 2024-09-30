import axios from "axios";
import { LLMQuery } from "@/models/LLMQuery";
const baseUrl = import.meta.env.VITE_BASE_URL;

export async function fetchLLMResponse(prompt, promptType) {
	let appConnectorUrl = baseUrl + import.meta.env.VITE_FETCH_LLM_RESPONSE;
	console.log('url for fetching llm: ', appConnectorUrl)
	return await axios
		.get(appConnectorUrl, {
			params: {
				prompt: prompt,
				promptType: promptType,
				maxTimeToWaitSeconds: 30,
				maxResultsToReturn: 500,
			},
		})
		.then((response) => {
			let toolTipString = response.data[0];
			let formattedSqlQuery = response.data[1];
			let answerWithContext = response.data[2];
			let itemUrls = response.data[3];
			return new LLMQuery(prompt, toolTipString, formattedSqlQuery, answerWithContext, itemUrls);
		})
		.catch((error) => {
			console.log(error);
		});

	
	}

// await submitUserPrompt('hello from inside the api file')