import axios from "axios";
import { Team } from "@/models/BaseballModels/Team";
import { Player } from "@/models/BaseballModels/Player";

const baseUrl = import.meta.env.VITE_BASE_URL;

console.log('baseurl ', baseUrl)

export async function getTeamsData() {
	let appConnectorUrl = baseUrl + import.meta.env.VITE_GET_TEAMS_DATA;
	let teams = [];
	let responseTeams = []
	await axios
		.get(appConnectorUrl, {
			params: {
				maxTimeToWaitSeconds: 30,
				maxResultsToReturn: 500,
			},
		})
		.then((response) => {
			responseTeams = response.data.items;
			teams = responseTeams.map(team => {
				const logoFileName = `${team.logoName}.svg`;
				let logoPath = new URL(`../assets/team-logos/${logoFileName}`, import.meta.url).href;
				return new Team(team.id, team.name, team.league, team.division, logoPath);
			});
			return teams;
		})
		.catch((error) => {
			console.log(error);
		});
	return teams
}

export async function getPlayersData() {
	let appConnectorUrl = baseUrl + import.meta.env.VITE_GET_PLAYERS_DATA;
	
	let players = [];
	let responsePlayers = []
	await axios
		.get(appConnectorUrl, {
			params: {
				maxTimeToWaitSeconds: 30,
				maxResultsToReturn: 500,
			},
		})
		.then((response) => {
			responsePlayers = response.data.items;
			players = responsePlayers.map(player => {
				const logoFileName = `${player.teamLogoName}.svg`;
				let teamLogoPath = new URL(`../assets/team-logos/${logoFileName}`, import.meta.url).href;
				return new Player(player.id, player.name, player.baseballReferenceUrl, player.teamName, teamLogoPath); 
			});
			return players;
		})
		.catch((error) => {
			console.log(error);
		});
	return players
}

export async function getPlayersOnTeam(teamId) {
	let appConnectorUrl = baseUrl + import.meta.env.VITE_GET_PLAYERS_ON_TEAM;
	let players = [];
	let responsePlayers = [];
	await axios
		.get(appConnectorUrl, {
			params: {
				teamId: teamId,
				maxTimeToWaitSeconds: 30,
				maxResultsToReturn: 500,
			},
		})
		.then((response) => {
			responsePlayers = response.data.items;
			players = responsePlayers.map(player => {
				const logoFileName = `${player.teamLogoName}.svg`;
				let teamLogoPath = new URL(`../assets/team-logos/${logoFileName}`, import.meta.url).href;
				return new Player(player.id, player.name, player.baseballReferenceUrl, player.teamName, teamLogoPath); 
			});
			return players;
		})
		.catch((error) => {
			console.log(error);
		});
	return players
}

export async function getAllTeamsPitchingStats() {
	let appConnectorUrl = baseUrl + import.meta.env.VITE_GET_ALL_TEAMS_PITCHING_STATS;
	let teams = [];

	await axios
		.get(appConnectorUrl, {
			params: {
				maxTimeToWaitSeconds: 30,
				maxResultsToReturn: 500,
			},
		})
		.then((response) => {
			teams = response.data.items.map(team => {

				const logoFileName = `${team.logoName}.svg`;
				let logoPath = new URL(`../assets/team-logos/${logoFileName}`, import.meta.url).href;
				const { id, name, league, division, logoName, ...otherProperties } = team;

				let pitchingStats = {};
				for (let [key, value] of Object.entries(otherProperties)) {
					let result = key.split(/(?=[A-Z])/);

					// capitalize the first letter of the column from db
					result[0] = result[0].charAt(0).toUpperCase() + result[0].slice(1);
					let statName = result.join(" ");
					pitchingStats[statName] = value;
				}

				return new Team(team.id, team.name, team.league, team.division, logoPath, team.baseballReferenceUrl, pitchingStats);
			});
			return teams;
		})
		.catch((error) => {
			console.log(error);
		});
	console.log('teams pitching stats obtained: ', teams)
	return teams
}

// export const teams = await getTeamsData();
export const players = await getPlayersData();
export const teamsPitchingStats = await getAllTeamsPitchingStats();