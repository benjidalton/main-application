export class LLMQuery {
	constructor(rawSqlQuery, formattedSqlQuery, answerWithContext) {
		this.rawSqlQuery = rawSqlQuery;
		this.formattedSqlQuery = formattedSqlQuery;
		this.answerWithContext = answerWithContext;
	}
}