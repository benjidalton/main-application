export class Team {
	constructor(id, name, league, division, logoPath, baseballReferenceUrl, pitchingStats) {
		this.id = id;
		this.name = name;
		this.league = league;
		this.division  = division;
		this.logoPath = logoPath;
		this.baseballReferenceUrl = baseballReferenceUrl;
		this.pitchingStats = pitchingStats;
	}
}