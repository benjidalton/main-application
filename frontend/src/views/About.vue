<script setup>
import { ref } from 'vue';
import BaseViewContainer from '@/components/BaseComponents/BaseViewContainer.vue';
const window = ref(null);
const length = ref(3);

const windowTitles = [
	'Education',
	'Experience',
	'Technologies'
]

const windowContents = [
	[
		'Masters in Neuromuscular Physiology'
	],
	[

	],
	[
		'Python', 'Github', 'Vue JS', 'Vuetify'
	]
	
]

</script>

<template>
	<BaseViewContainer>
		<v-card class="card">
			<v-toolbar>
				<v-toolbar-title style="text-align: left; padding-left: 40px;">
					<span style="padding-top: 20px; font-size: 30px; border-bottom: 2px solid black;">Ben Dalton</span>
				</v-toolbar-title>
				<v-btn @click="window=0">
					Education
				</v-btn>
				<v-btn @click="window=1">
					Experience
				</v-btn>
				<v-btn @click="window=2">
					Technologies
				</v-btn>
				<v-btn @click="window=3">
					Fun Facts
				</v-btn>

				<v-spacer></v-spacer>
				<v-btn>
					Resume
					<v-icon icon="mdi-file-download-outline" />
				</v-btn>
			</v-toolbar>
			<v-window
				v-model="window"
				show-arrows
				>
				<v-window-item :key="0" class="window-item">
					<v-row>
						<v-col cols="6">
							<v-card width="40vw" style="background-color: aqua;">
								<v-card-title>
									<span style="padding-top: 20px; font-size: 24px; border-bottom: 2px solid black;">Education</span>
								</v-card-title>
								<v-btn>clickem</v-btn>
							</v-card>
						</v-col>
						<v-col cols="6">
							<v-card width="40vw" style="background-color: azure;">
								<v-card-title>
									<span style="padding-top: 20px; font-size: 24px; border-bottom: 2px solid black;">Experience</span>
								</v-card-title>

							</v-card>
						</v-col>
					</v-row>	
				</v-window-item>
				<v-window-item v-for="(windowTitle, index) in windowTitles" :key="index" class="window-item">
					<v-card  height="500px">
						<v-card-title>
							{{ windowTitle }}
						</v-card-title>
						<template v-for="(windowContent, index2) in windowContents[index]" :key="index2">
							<p>
								> {{ windowContent }}
							</p>
						</template>
					</v-card>
				</v-window-item>

			</v-window>

		</v-card>
	</BaseViewContainer>
</template>

<style scoped>
.card {
	position: fixed;
	min-width: 700px;
	height: fit-content;
	width: 80vw;
}

.window-item {
	height: 600px;
}

</style>