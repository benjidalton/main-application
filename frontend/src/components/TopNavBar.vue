<script setup>
import { ref, computed, onMounted  } from 'vue';
import { useRouter } from 'vue-router';
const frontEndIcons = ['mdi-vuejs', 'mdi-vuetify', 'mdi-nodejs' ]
const frontEndLabels = ['Vue JS', 'Vuetify', 'Node JS',]

const backEndIcons = ['mdi-language-python', 'mdi-database']
const backEndLabels = ['Python', 'MariaDB']

const generalIcons = ['mdi-github', 'mdi-microsoft-visual-studio-code']
const generalLabels = ['Github', 'VS Code']
const router = useRouter();

onMounted(()=> {
	console.log('router', router.currentRoute.value.fullPath)
})
const navBarStyle = computed(() => {
	let backgroundColor;
	switch(router.currentRoute.value.fullPath) {
		case '/blackjack':
		case '/solitaire':
			backgroundColor = 'black'
			break;
		default:
			backgroundColor = 'rgb(62, 81, 121)'
	}
	return { backgroundColor};

})

const elevationClass = computed(() => {
    switch(router.currentRoute.value.fullPath) {
        case '/blackjack':
		case '/solitaire':
            return 'custom-elevation'; // Apply custom elevation for this route
        default:
            return ''; // Default to no custom elevation
    }
});
</script>

<template>
	<v-app-bar id="topNavBar" app  elevated :style="navBarStyle">
		<v-row align="center" no-gutters style="padding-right: 40px; position: relative; overflow: visible;">
			
			<v-btn 
				text="Baseball LLM" 
				:to="{ name: 'baseball' }" 
				color="rgb(224, 224, 224)" 
				style="margin-left: 50px;"
			/>

			<v-menu>
				<template v-slot:activator="{ props }">
					<v-btn text="Card Games"  v-bind="props" color="rgb(224, 224, 224)"/>
				</template>
				<v-list>
					<v-list-item
						v-for="(link, index) in [{ name: 'Blackjack', href: '/blackjack' }, { name: 'Solitaire', href: '/solitaire' }]"
						:key="index"
						:to="link.href"
					>
						<v-list-item-title>
							{{ link.name.toUpperCase() }}
						</v-list-item-title>
					</v-list-item>
				</v-list>
			</v-menu>
			
			<v-btn 
				text="Fitness Tracker" 
				:to="{ name: 'fitness-tracker' }" 
				color="rgb(224, 224, 224)" 
			/>

			<v-spacer></v-spacer>
			
			<v-col cols="auto" style="padding-right: 40px; position: relative; overflow: visible;">
				<v-btn text="About The Dev" :to="{ name: 'about' }" color="rgb(224, 224, 224)"></v-btn>
				<v-menu transition="scale-transition">
					<template v-slot:activator="{ props }">
						<v-btn v-bind="props" text="" color="rgb(224, 224, 224)">
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

				<v-btn href="https://github.com/kcbdalton" target="_blank" icon color="rgb(224, 224, 224)">
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
	background-color: rgb(62, 81, 121);
	overflow: visible; 
	z-index: 999;
}

</style>