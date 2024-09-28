<script setup>
import { ref, onBeforeMount } from 'vue';
import { teams, getPlayersOnTeam } from '@/api/getData';
// import LLMConversation from '@/components/LLMConversation.vue';
// import LLMConversation from '@/components/LLMConversation.vue';
import { fetchLLMResponse } from '@/api/llmAPI';
import PromptInput from '@/components/PromptInput.vue';

const displayTeamNames = ref(null);
const displayTeamLogos = ref(null);
const playersOnTeam = ref(null)
const currentTeam = ref(null);
const playerHeaders = ref([
	{ title: 'Player Name', key: 'name', width: '100px', align: 'center' },
	{ title: 'Team Name', key: 'teamName', width: '100px', align: 'center'  },
	{ title: 'Team Logo', key: 'teamLogoPath', sortable: false, width: '100px', align: 'center'  },
]);

const llmQueries = ref([])
const userPrompt = ref(null);
onBeforeMount(() => {
	displayTeamNames.value = teams.map(team => team.name);
	displayTeamLogos.value = teams.map(team => team.logoPath);
});

async function onTeamChosen(team) {
	currentTeam.value = team;
	playersOnTeam.value = await getPlayersOnTeam(currentTeam.value.id);
	console.log('players on team: ', playersOnTeam.value)
}


async function onUserPrompt(prompt) {
	console.log('propmpt in handle user prompt:', prompt)
	llmQueries.value.push(await fetchLLMResponse(prompt))
	// console.log('llmMessage: ', llmQuery.value.answerWithContext)
}

</script>

<template>
	<PromptInput @userPrompt="onUserPrompt" /> 
	<v-sheet>
		<template v-if="llmQueries.length > 0">
			<v-row v-for="(query, index) in llmQueries" :key="index"  justify="center" align="center" class="mt-4">
				<v-col cols="12" md="6" class="text-center">
					<v-textarea 
						 
						v-model="query.rawSqlQuery" 
						full-width
						label="Raw SQL Query"
					></v-textarea>
				</v-col>
				<v-col cols="12" md="6" class="text-center">
					<v-textarea 
						v-model="query.answerWithContext" 
						full-width
						label="Answer with Context"
					></v-textarea>
				</v-col>
			</v-row>

		</template>
		
		
		<!-- <v-row>
			<v-sheet class="container">
				<v-menu location="end">
					<template v-slot:activator="{ props }">
						<v-btn
							color="primary"
							v-bind="props"
						>
						Activator slot
						</v-btn>
					</template>

					<v-list>
						<v-list-item
							v-for="(team, index) in teams"
							:key="index"
							@click="onTeamChosen(team)"
							width="300"
							>
							<v-list-item-title>{{ team.name }}</v-list-item-title>

							<template v-slot:prepend>
								<v-avatar >
									<v-img :src="team.logoPath" max-width="25" max-height="25" class="mr-2"/>
								</v-avatar>
							</template>

						</v-list-item>
					</v-list>

				</v-menu>


			</v-sheet>

		</v-row> -->
		
		<!-- <LLMConversation /> -->

		<v-data-table 
			v-if="playersOnTeam"			
			:items="playersOnTeam"
			:headers="playerHeaders"
			style="width: 50vw;"
		>
			<template v-slot:item.teamLogoPath="{ item }">
				<v-avatar>
					<v-img :src="item.teamLogoPath" max-width="25" max-height="25" />
				</v-avatar>
			</template>
			<template v-slot:item.name="{ item }" >
				<a :href="item.baseballReferenceUrl" target="_blank" style="text-decoration: none; color: inherit;">
					{{ item.name }} 
				</a>
			</template>
		<!-- <template v-slot:item="{ item }">
					<tr>
						<td>
							<v-text-field
								v-model="item.name"
								type="text"
							/>
						</td>
						<td>
							<v-text-field
								v-model="item.teamName"
								type="text"
							/>
						</td>
						<td>
							<v-text-field
								v-model="item.name"
								type="text"
							/>
						</td>
						<td>
							<v-text-field
								v-model="item.teamLogoPath"
								type="text"
							/>
						</td>
					</tr>

				</template> -->
		</v-data-table> 



	</v-sheet>
		<!-- <Table /> -->

</template>


<style scoped>
.container {
	width: 50vw;
}

#logo-container {
	border: 2px solid gray;
	background-color: aliceblue;
}
</style>