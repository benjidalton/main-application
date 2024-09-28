import axios from "axios";
import { LLMQuery } from "@/models/LLMQuery";
const baseUrl = import.meta.env.VITE_BASE_URL;

export async function fetchLLMResponse(prompt) {
	let appConnectorUrl = baseUrl + import.meta.env.VITE_FETCH_LLM_RESPONSE;
	console.log('url: ', appConnectorUrl)
	// console.log(prompt)
	return await axios
		.get(appConnectorUrl, {
			params: {
				prompt: prompt,
				maxTimeToWaitSeconds: 30,
				maxResultsToReturn: 500,
			},
		})
		.then((response) => {
			let rawSqlQuery = response.data[0];
			let formattedSqlQuery = response.data[1];
			let answerWithContext = response.data[2];
			return new LLMQuery(rawSqlQuery, formattedSqlQuery, answerWithContext) ;
		})
		.catch((error) => {
			console.log(error);
		});

	
	}

// await submitUserPrompt('hello from inside the api file')