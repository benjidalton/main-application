<script setup>
import { ref, watch, toRefs } from 'vue';
import ChooseCardBack from '@/components/BlackjackComponents/ChooseCardBack.vue';

const props = defineProps({
	gameStarted : Boolean,
	money: Number
})

const { money } = toRefs(props);

watch(money, (newVal) => {
	console.log('money amount passed to scoreboard: ', newVal);
});

const emit = defineEmits(['betChanged', 'cardBackChanged', 'soundToggled']);

const bet = ref(100);
const betOptions = ref([10, 20, 50, 100, 200]);

const chosenCardBack = ref('');
const playSound = ref(false);

function selectBet(value) {
	bet.value = value;
	emit('betChanged', bet.value);
}

function onCardBackChanged(newCardBackFilePath) {
	chosenCardBack.value = newCardBackFilePath;
	emit('cardBackChanged', chosenCardBack.value)
}

function toggleSound() {
	playSound.value = !playSound.value;
	emit('soundToggled', playSound.value)
}

</script>

<template>

	<v-card id="scoreboard" >
		<v-card-title style="text-align: left; padding-top: 20px;">
			<span style="font-size: 40px; padding-top: 5px;">Money: </span>
			<div class="money-container" id="money-counter" >
				<span style="font-size: 40px;">{{ money }}</span>
			</div>
		</v-card-title>
		<v-row style="padding-top: 40px; padding-left: 50px; align-items: center">
			<v-icon icon="mdi-lock" v-if="gameStarted" style="padding-right: 20px; font-size: 40px;"/>
			<v-icon 
				icon="mdi-lock" 
				v-else 
				style="padding-right: 20px;  visibility: hidden;" 
				/>
			<span style="font-size: 40px;">Bet: </span>
			<div class="money-container" id="bet-counter">
				
				<v-menu transition="scale-transition" :disabled="gameStarted" offset-y attach="body">
					<template v-slot:activator="{ props }">
						<!-- <div id="bet-counter"> -->
							<span style="font-size: 40px;" v-bind="props" :style="'cursor: pointer'">{{ bet }}</span>
						<!-- </div> -->
					</template>
					<v-list id="prompts-list" style="right: 18px;">
						<v-list-item
							v-for="(option, index) in betOptions"
							:key="index"
							style="cursor: pointer;"
							@click="selectBet(option)"
						>
						<v-list-item-title v-text="option" style="font-family: Casino;"></v-list-item-title>
						</v-list-item>
					</v-list>
				</v-menu>
				
			</div>
		</v-row>

		<ChooseCardBack @cardBackChanged="onCardBackChanged"/>
		<template v-if="playSound">
			<v-btn id="sound-button" @click="toggleSound" >
			<v-icon icon="mdi-volume-high" />
		</v-btn>
		</template>
		<template v-else="!playSound">
			<v-btn id="sound-button" @click="toggleSound" style="outline: 2px solid gray;">
				<v-icon  icon="mdi-volume-variant-off" style="color: gray; "/>
			</v-btn>
		</template>
		
		
	</v-card>
</template>

<style scoped>


#scoreboard {
	position: absolute;
	top: 2vh;
	left: 38vw;
	width: 24vw;
	height: 20vh;  /* Increased height to fit the input */
	border: 5px dotted red;
	background-color: rgb(0, 0, 0);
	font-family: 'Casino';
	color: #FFD700;
	outline: 5px dotted #C0C0C0;
	overflow: visible;
}

.money-container {
	position: absolute;
	display: flex;
	border: 2px solid rgb(39, 37, 37);
	border-radius: 5px;
	width: 30%;
	height: 80px;
	margin-right: 200px;
	background-color: black; 
	justify-content: center;
	align-items: center;
}

#money-counter {
	position: absolute;
	top: 10px;
	left: 50%;
}

#bet-counter {                    
	position: absolute;
	top: 55%;
	left: 50%;
}

#bet-input {
	font-size: 20px;
	text-align: center;
	justify-content: center;
	z-index:20;
}

#prompts-list {
	width: 100px;
	justify-content: center;
	text-align: center;
	background-color: #f7ffe3;
}

.v-list-item-title {
	padding: 5px;
	font-size: 30px;
}


#sound-button {
	position: absolute;
	top: 110px;
	right: 15px;
	z-index: 1000;
	height: 60px;
	width: fit-content;
	outline: 2px solid #FFD700;
	border-radius: 5px;
	background-color: rgb(0, 0, 0);
	font-weight: bold;
	font-family: 'Casino';
	color: #FFD700;
	font-size: 24px;
}

</style>