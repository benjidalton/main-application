export class LLMQuery {
	constructor(originalPrompt, rawSqlQuery, formattedSqlQuery, answerWithContext, itemUrls) {
		this.originalPrompt = originalPrompt;
		this.rawSqlQuery = rawSqlQuery;
		this.formattedSqlQuery = formattedSqlQuery;
		this.answerWithContext = answerWithContext;
		this.itemUrls = itemUrls;
		this.formattedResponse = '';
	}
}