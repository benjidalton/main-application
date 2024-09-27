<script setup>
import { ref, onBeforeMount } from 'vue';
import Table from '@/components/Table.vue';
import { teams } from '@/api/getData';

const displayTeamNames = ref(null);
const displayTeamLogos = ref(null);
const currentTeam = ref(null);

onBeforeMount(() => {
	// console.log('team names: ', teamNames)
	console.log('teams in default view', teams)
	displayTeamNames.value = teams.map(team => team.name);
	displayTeamLogos.value = teams.map(team => team.logoPath);
	console.log('display team names: ', displayTeamNames.value)
	console.log('team logo paths: ', displayTeamLogos.value)
});


</script>

<template>
	<v-sheet>
		<v-textarea v-model="displayTeamNames">


		</v-textarea>
		<v-row>
			<v-sheet class="container">
				<v-select 
					label="Choose Team"
					:v-model="currentTeam" 
					:items="displayTeamNames"
				>
				<template v-slot:item="{ item, index }">
						<v-row align="center">
							<v-img :src="displayTeamLogos[index]" :alt="item" max-width="50" class="mr-2" />
							<span>{{ displayTeamNames[index] }}</span>
						</v-row>
					</template>
				</v-select>
		</v-sheet>
<v-row>
			<v-col
				v-for="(logoPath, index) in displayTeamLogos"
				:key="index"
				cols="12" sm="6" md="4" lg="3"
			>
				<v-img :src="logoPath" :alt="displayTeamNames[index]" class="team-logo"/>
			</v-col>
		</v-row>

		</v-row>
		<!-- <Table /> -->
		



	</v-sheet>
		<!-- <Table /> -->

</template>


<style scoped>
.container {
	width: 50vw;
}
</style>