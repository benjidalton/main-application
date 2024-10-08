<script setup>
import { ref, computed } from 'vue';
import PlayingCardComponent from '@/components/BlackjackComponents/PlayingCardComponent.vue'
import BaseViewContainer from '@/components/BaseComponents/BaseViewContainer.vue';
import { deck, dealCard, initialDeal, createDeck } from '@/services/BlackjackService';
import { Hand } from '@/models/CardGameModels/Hand.js';
import MoneyAnimation from '@/components/BlackjackComponents/MoneyAnimation.vue';
import Scoreboard from '@/components/BlackjackComponents/Scoreboard.vue';
import RulesContainer from '@/components/BlackjackComponents/RulesContainer.vue';

import slapSound from '@/assets/slap.mp3'
import coinSound from '@/assets/coins.mp3'



const cardShift = 120;
const initialPlayerOffset = 110;
const initialDealerOffset = 1500;

const blackjackRules = [
	"The goal is to beat the dealer by having a hand value as close to 21 as possible without going over.",
	"Each player is dealt two cards. The dealer also gets two cards, one face up and one face down.",
	"Cards 2 through 10 are worth their face value. Face cards (Jack, Queen, King) are worth 10. Aces are worth 1 or 11.",
	"Players can choose to 'Hit' to take an additional card or 'Stand' to keep their current hand.",
	"If your hand exceeds 21, you bust and lose the round.",
	"The dealer must hit until their cards total 17 or higher.",
	"If the dealer busts, the player automatically wins.",
	"If your hand value is higher than the dealer's without exceeding 21, you win.",
	"In the event of a tie (both player and dealer have the same value), it is a push, and no one wins."
];

const gameStarted = ref(false);
const playerHand = ref(new Hand());
const dealerHand = ref(new Hand());
const currentDeck = ref(deck);
const bet = ref(100);
const money = ref(1000); 
const playerWin = ref(false);
const newGameMessage = ref('');
const snackbar = ref(false);
const showHandValues = ref(false)
const showDealerHand = ref(false);
const showMoneyAnimation = ref(false);

const playSounds = ref(false);

const chosenCardBack = ref('/src/assets/card-images/black_gold_back.png');

const moneyAnimationAngles = ref([0, 30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330, 360])

const split = computed(() => {
	if (playerHand.value.length === 2) { 
		const [firstCard, secondCard] = playerHand.value;
		return firstCard.value === secondCard.value;
	}
	return false;
})

function startGame() {
	
	if (playerHand.value.length > 0 || dealerHand.value.length > 0) {
		currentDeck.value = createDeck();
		playerHand.value = new Hand();
		dealerHand.value = new Hand();
		
	}

	[playerHand.value, dealerHand.value] = initialDeal(currentDeck.value);

	showHandValues.value = true;
	showDealerHand.value = false;
	showMoneyAnimation.value = false;
	gameStarted.value = true;

	if (playerHand.value.getTotalValue() == 21) {
		playerWin.value = true;
		handleNewGame();
	}

}

function hit() {
	playerHand.value.push(dealCard(currentDeck.value))
	if (playerHand.value.getTotalValue() == 21) {
		playerWin.value = true;
		handleNewGame();
	}
	if (playerHand.value.getTotalValue() > 21) {
		playerWin.value = false;
		handleNewGame();
	}
}

function stand() {
	while (dealerHand.value.getTotalValue() < 17) {
		// break early user stands a low hand value and dealer hand > than player hand but still lower than 17
		if (dealerHand.value.getTotalValue() > playerHand.value.getTotalValue()) {
			playerWin.value = false;
			handleNewGame();
			break
		}
		dealerHand.value.push(dealCard(currentDeck.value));
	}

	const dealerTotal = dealerHand.value.getTotalValue();
	const playerTotal = playerHand.value.getTotalValue();

	if (dealerTotal > 21) {
		playerWin.value = true;
	} else if (playerTotal > dealerTotal) {
		playerWin.value = true;
	} else if (playerTotal < dealerTotal) {
		playerWin.value = false;
	} else {
		playerWin.value = false;
	}

	handleNewGame();
}

function handleNewGame() {
	let message;
	if (playerWin.value) {
		if (dealerHand.value.getTotalValue() > 21) {
			message = `The dealer busted with a hand value of ${dealerHand.value.getTotalValue()}. You won $${bet.value}!`;
		} else {
			message = `You won with a hand value of ${playerHand.value.getTotalValue()} to the dealer's ${dealerHand.value.getTotalValue()}. You won $${bet.value}!`;
		}
	} else {
		if (playerHand.value.getTotalValue() > 21) {
			message = `You busted with a hand value of ${playerHand.value.getTotalValue()}. You lost $${bet.value}.`;
		} else {
			message = `The dealer beat you with a hand value of ${dealerHand.value.getTotalValue()} to your ${playerHand.value.getTotalValue()}. You lost $${bet.value}.`;
		}
	}
	handleMoney()
	showMoneyAnimation.value = true;
	showDealerHand.value = true;
	newGameMessage.value = message;
	snackbar.value = true
	gameStarted.value = false;
	setTimeout(() => {
		snackbar.value = false
		showMoneyAnimation.value = false;
		
	}, 2500);
	
}

function handleMoney() {
	console.log('playerwin: ',playerWin.value,'\nmoney before adding bet: ', money.value,  '\ncurrent bet: ', bet.value)
	let val = money.value += playerWin.value ? bet.value : -bet.value;
	money.value = val;
	handleMoneySound();
	console.log('money after bet added:', money.value)
}

function updateBet(newBet) {
	bet.value = newBet;
}

function onCardBackChanged(newCardBackFilePath) {
	chosenCardBack.value = newCardBackFilePath;
}

function onSoundToggled(sound) {
	playSounds.value = sound;
}

function handleMoneySound() {
	if (playSounds.value) {
		let audio = new Audio(coinSound);
			audio.volume = 0.25;
			audio.currentTime = 2.5;
			audio.addEventListener('timeupdate', () => {
				if (audio.currentTime >= 4) {
					audio.pause(); 
					audio.currentTime = 2.5;
			}
		});
		audio.play();
	}
}

function handleDealerHandTouch() {
	if (playSounds.value) {
		let activeSound = new Audio(slapSound)
		activeSound.volume = 0.1;
		activeSound.play()
	}
}

</script>

<template>
	<BaseViewContainer style="background-color: rgb(100, 0 , 0);">
		<Scoreboard 
			:gameStarted="gameStarted" 
			:money="money" 
			@betChanged="updateBet"
			@cardBackChanged="onCardBackChanged"
			@soundToggled="onSoundToggled"
		/>

		<template v-for="(angle, index) in moneyAnimationAngles" :key="index">
			<MoneyAnimation 
				:isVisible="showMoneyAnimation" 
				:amount="50" 
				:duration="2"
				:win="playerWin"

				:style="`transform: rotate(${angle}deg); position: absolute; top: 6vh; left: 53vw;`"
			/>

		</template>
		

		<v-btn class="custom_btn" v-if="!gameStarted" @click="startGame">Deal</v-btn>
		<v-btn class="custom_btn" v-if="gameStarted" @click="hit">Hit</v-btn>
		<v-btn class="custom_btn" v-if="gameStarted" @click="stand">Stand</v-btn>
		<v-btn class="custom_btn" v-if="gameStarted && split">Split</v-btn>
		
		<span v-if="showHandValues" id="players-hand-score">Player's Hand Value: {{ playerHand.getTotalValue() }}</span>
		<template v-for="(card, index) in playerHand" :key="index">
			<PlayingCardComponent 
				:card="card" 
				:startingX="initialPlayerOffset + index * cardShift" 
				:showCardValues="true"
				:style="{ transform: `rotate(${card.rotation}deg)`, marginTop: '350px' }"
			/>
		</template>

		<span v-if="showDealerHand" id="dealers-hand-score">Dealer's Hand Value: {{ dealerHand.getTotalValue() }}</span>
		<template v-for="(card, index) in dealerHand" :key="index">
			
			<PlayingCardComponent 
				:card="card" 
				:startingX="initialDealerOffset - index * cardShift"  
				:startingY="380"
				:showCardValues="showDealerHand"
				:style="{ transform: `rotate(${card.rotation}deg)`, marginTop: '350px' }"
				:cardBack="chosenCardBack"
				@click="handleDealerHandTouch"
				:draggable="false"
			/>
		</template>

		<v-snackbar
			v-model="snackbar"
			multi-line
			style="text-align: center; justify-content: center; font-family: 'Casino'; font-size: 50px;"
			
			color="#FFD700"
		>
			{{ newGameMessage }}
		</v-snackbar>

		<RulesContainer :rules="blackjackRules" />
		
	</BaseViewContainer>
</template>


<style scoped>
@import url('https://fonts.cdnfonts.com/css/casino');
.custom_btn {
	width: auto; /* Allow the button to size based on content */
	padding: 10px;
	margin: 10px;
	font-size: 40px;
	display: flex; 
	justify-content: center;
	align-items: center;
	height: 60px;
	font-family: 'Casino';
	background-color: rgb(0, 0, 0);
	font-family: 'Casino';
	color: #FFD700;
}

.snackbar {
	background-color: rgb(0, 0, 0);
	font-family: 'Casino';
	color: #FFD700;
}

#players-hand-score {
	position: absolute;
	left: 8vw;
	top: 18vh;
	font-size: 40px;
	font-weight: bold;
	font-family: 'Casino';
	color: #f7ffe3;
}

#dealers-hand-score {
	position: absolute;
	right: 8vw;
	top: 18vh;
	font-size: 40px;
	font-weight: bold;
	font-family: 'Casino';
	color: #f7ffe3;
}



@keyframes fadeOutBorder {
	0% {
	border-color: green;
	}
	100% {
	border-color: rgb(39, 37, 37); /* Original border color */
	}
}


</style>