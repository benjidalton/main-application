import axios from "axios";
import { Team } from "@/models/Team";
import { Player } from "@/models/Player";

const baseUrl = import.meta.env.VITE_BASE_URL;

console.log('baseurl ', baseUrl)

export async function getTeamsData() {
	let appConnectorUrl = baseUrl + import.meta.env.VITE_GET_TEAMS_DATA;
	console.log('app connector url: ', appConnectorUrl)
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
			console.log('players response: ', response)
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
	let responsePlayers = []
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

export const teams = await getTeamsData();
export const players = await getPlayersData();
