<script setup>
import { ref } from 'vue';
import PlayingCard from '@/components/BlackjackComponents/PlayingCard.vue'
import BaseViewContainer from '@/components/BaseComponents/BaseViewContainer.vue';
import { deck, dealCard, initialDeal } from '@/services/BlackjackService';
import { Hand } from '@/models/Hand.js';

const gameStarted = ref(false);
const activeCards = ref([]);
const cardShift = 120;
const initialPlayerOffset = 110;
const initialDealerOffset = 1700;
const playerHand = ref(new Hand());
const dealerHand = ref(new Hand());

const bet = ref(0);
const money = ref(1000);

function startGame() {
	initialDeal(playerHand.value, dealerHand.value);
	console.log('player hand: ', playerHand.value)
	gameStarted.value = true;
}

function hit() {
	playerHand.value.push(dealCard())

}


function drawCard() {
	console.log('deck length', deck.length)
	let dealtCard = dealCard();
	activeCards.value.push(dealtCard)
	console.log('deck length', deck.length)
}


</script>

<template>
	<BaseViewContainer >
		<v-card id="money-container">
			<v-card-title style="text-align: left;">
				<span style="font-size: 40px;">Money: </span>
				<div id="money-counter">
					<span style="font-size: 40px;">${{ money }}</span>
				</div>
			</v-card-title>


		</v-card>
		<v-btn class="custom_btn" v-if="!gameStarted" @click="startGame">Deal</v-btn>
		<v-btn class="custom_btn" v-if="gameStarted" @click="hit">Hit</v-btn>
		<v-btn class="custom_btn" v-if="gameStarted" @click="drawCard">Stand</v-btn>
		<v-container class="hands">
			<v-container class="player-hand">
				<template v-for="(card, index) in playerHand" :key="index">
					<PlayingCard :card="card" :startingX="initialPlayerOffset + index * cardShift" />
				</template>
			</v-container>

			<v-container class="dealer-hand">
				<template v-for="(card, index) in dealerHand" :key="index">
					<PlayingCard :card="card" :startingX="initialDealerOffset - index * cardShift" />
				</template>
			</v-container>

		</v-container>

	</BaseViewContainer>
	

</template>


<style scoped>
.custom_btn {
	width: auto; /* Allow the button to size based on content */
	padding: 10px;
	margin: 10px;
	font-size: 40px;
	display: flex; /* Enable flexbox */
	justify-content: center; /* Center the text */
	align-items: center; /* Center vertically */
	height: 60px;
}

#money-container {
	position: absolute;
	top: 2vh;
	left: 3vw;
	width: 20vw;
	height: 15vh;
	border: 2px solid rgb(191, 184, 184);
	background-color: rgb(238, 238, 238);
}

#money-counter {
	position: absolute;
	display: flex;
	top: 0;
	border: 2px solid rgb(39, 37, 37);
	border-radius: 5px;
	width: 50%;
	height: 80px;
	margin-top: 10px;
	margin-right: 20px;
	right: 0;
	background-color: rgb(243, 243, 243);
	justify-content: center;
	align-items: center;
}

</style>