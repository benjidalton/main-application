export class LLMQuery {
	constructor(originalPrompt, toolTipString, formattedSqlQuery, answerWithContext, itemUrls) {
		this.originalPrompt = originalPrompt;
		this.toolTipString = toolTipString;
		this.formattedSqlQuery = formattedSqlQuery;
		this.answerWithContext = answerWithContext;
		this.itemUrls = itemUrls;
		this.formattedResponse = '';
	}
}