<script setup>
import { ref, computed, onMounted, watch  } from 'vue';
import { useRouter } from 'vue-router';
const frontEndIcons = ['mdi-vuejs', 'mdi-vuetify', 'mdi-nodejs' ]
const frontEndLabels = ['Vue JS', 'Vuetify', 'Node JS',]

const backEndIcons = ['mdi-language-python', 'mdi-database']
const backEndLabels = ['Python', 'MariaDB']

const generalIcons = ['mdi-github', 'mdi-microsoft-visual-studio-code']
const generalLabels = ['Github', 'VS Code']
const router = useRouter();
const chosenColor = ref('')
const fitnessRoutes = ref([
	{ name: 'New Workout', href: '/fitness-tracker/new-workout-diary' }, 
	{ name: 'View Log', href: '/fitness-tracker/view-diary' }
])

const gameRoutes = ref([
	{ name: 'Blackjack', href: '/blackjack' }, 
	{ name: 'Solitaire', href: '/solitaire' }
])

onMounted(()=> {
	console.log('current path: ', router.currentRoute.value.fullPath)
})
const navBarStyle = computed(() => {
	let backgroundColor;
	switch(router.currentRoute.value.fullPath) {
		case '/blackjack':
		case '/solitaire':
			backgroundColor = 'black'
			break;
		default:
			backgroundColor = 'var(--top-bar-bg)'
	}
	return { backgroundColor};

})

watch(chosenColor , (color) => {
	document.documentElement.style.setProperty('--custom-card-bg', color);
})

</script>

<template>
	<v-app-bar id="topNavBar" app  elevated :style="navBarStyle">
		<v-row align="center" no-gutters style="padding-right: 40px; position: relative; overflow: visible;">
			
			<v-btn 
				class="navbar-btn"
				text="Baseball LLM" 
				:to="{ name: 'baseball' }" 
				style="margin-left: 50px;"
			/>

			<v-menu>
				<template v-slot:activator="{ props }">
					<v-btn class="navbar-btn" text="Card Games"  v-bind="props"/>
				</template>
				<v-list>
					<v-list-item
						v-for="(link, index) in gameRoutes"
						:key="index"
						:to="link.href"
					>
						<v-list-item-title>
							{{ link.name.toUpperCase() }}
						</v-list-item-title>
					</v-list-item>
				</v-list>
			</v-menu>

			<v-menu>
				<template v-slot:activator="{ props }">
					<v-btn 
						class="navbar-btn"
						text="Fitness Tracker" 
						v-bind="props"	
					/>
				</template>
				<v-list>
					<v-list-item
						v-for="(link, index) in fitnessRoutes"
						:key="index"
						:to="link.href"
					>
						<v-list-item-title>
							{{ link.name.toUpperCase() }}
						</v-list-item-title>
					</v-list-item>
				</v-list>
			</v-menu>
			

			<v-spacer></v-spacer>
			<v-col cols="auto">
				<v-menu offset-y>
					<template v-slot:activator="{ props }">
						<v-btn
							class="navbar-btn"
							variant="tonal"
							v-bind="props"
						>
						Choose Color
						</v-btn>
					</template>
						<v-color-picker
							value="#7417BE"
							v-model="chosenColor"
							hide-inputs 
							show-swatches
							class="mx-auto"
							@input="updateGlobalColor(color)"
						></v-color-picker>
					</v-menu>
			</v-col>


			<v-col cols="auto" style="padding-right: 40px; position: relative; overflow: visible;">
				<v-btn  class="navbar-btn" text="About The Dev" :to="{ name: 'about' }"></v-btn>
				<v-menu transition="scale-transition">
					<template v-slot:activator="{ props }">
						<v-btn class="navbar-btn" v-bind="props" text="">
							Tech Stack
							<v-icon size="20px" style="padding-left: 5px;">
								mdi-information-slab-circle-outline  
							</v-icon>
						</v-btn>
					</template>
					<v-container>
						<v-row>
							
							<v-card style="border-right: 2px solid gray;" v-if="router.currentRoute.value.fullPath != '/blackjack'"> 
								<v-card-title style="text-align: center;">
									<span style="border-bottom: 1px solid black;" >Back End</span>
								</v-card-title>
								<v-card-item>
									<v-list-item
										v-for="(icon, index) in backEndIcons"
										:key="index"
									>
									<v-icon :icon="icon" />
										{{ backEndLabels[index] }}
									</v-list-item>
								</v-card-item>
							</v-card>

							<v-card style="border-right: 2px solid gray;" > 
								<v-card-title style="text-align: center;">
									<span style="border-bottom: 1px solid black;">Front End</span>
								</v-card-title>
								<v-card-item>
									<v-list-item
										v-for="(icon, index) in frontEndIcons"
										:key="index"
									>
									<v-icon :icon="icon" />
										{{ frontEndLabels[index] }}
									</v-list-item>
								</v-card-item>
							</v-card>

							<v-card> 
								<v-card-title style="text-align: center;">
									<span style="border-bottom: 1px solid black;">General</span>
								</v-card-title>
								<v-card-item>
									<v-list-item
										v-for="(icon, index) in generalIcons"
										:key="index"
									>
									<v-icon :icon="icon" />
										{{ generalLabels[index] }}
									</v-list-item>
								</v-card-item>
							</v-card>

						</v-row>
					</v-container>
				</v-menu>

				<v-btn href="https://github.com/kcbdalton" target="_blank" icon color="var(--top-nav-bar-btn-font)">
					<v-icon size="40px">
						mdi-github 
					</v-icon>
				</v-btn>

			</v-col>
		</v-row>
	</v-app-bar>
</template>

<style scoped>
/* !important means dont overwrite */
.router-link-active {
	color: #007bff !important;
}

.button {
	margin-right: 10px;
}

#topNavBar {
	background-color: var(--top-bar-bg);
	overflow: visible; 
	z-index: 999;
}
.navbar-btn {
	margin: 5px;
	background-color: var(--top-bar-btn);
	color: var(--top-nav-bar-btn-font);
}

</style>