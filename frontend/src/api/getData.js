import axios from "axios";
import { Team } from "@/models/Team";

export async function getTeamsData() {
	let appConnectorUrl = import.meta.env.VITE_APP_GET_TEAM_DATA;
	
	let teams = [];
	let allTeams = []
	await axios
		.get(appConnectorUrl, {
			params: {
				maxTimeToWaitSeconds: 30,
				maxResultsToReturn: 500,
			},
		})
		.then((response) => {
			allTeams = response.data.items;
			teams = allTeams.map(team => {
				const logoFileName = `${team.logoName}.svg`;
				let logoPath = new URL(`../assets/team-logos/${logoFileName}`, import.meta.url).href;
				return new Team(team.name, team.league, team.division, logoPath);
			});
			return teams;
		})
		.catch((error) => {
			console.log(error);
		});
	return teams
}


export const teams = await getTeamsData();

console.log('teams: ', teams)