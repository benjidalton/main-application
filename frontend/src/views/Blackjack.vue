<script setup>
import { ref, computed } from 'vue';
import PlayingCardComponent from '@/components/BlackjackComponents/PlayingCardComponent.vue'
import BaseViewContainer from '@/components/BaseComponents/BaseViewContainer.vue';
import { deck, dealCard, initialDeal, createDeck } from '@/services/BlackjackService';
import { Hand } from '@/models/Hand.js';
import MoneyAnimation from '@/components/BlackjackComponents/MoneyAnimation.vue';
import Scoreboard from '@/components/BlackjackComponents/Scoreboard.vue';
import RulesContainer from '@/components/BlackjackComponents/RulesContainer.vue';

const cardShift = 120;
const initialPlayerOffset = 110;
const initialDealerOffset = 1700;

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

const split = computed(() => {
	if (playerHand.value.length === 2) { 
		const [firstCard, secondCard] = playerHand.value;
		return firstCard.value === secondCard.value;
	}
	return false;
})

const dealerCardsStyle = computed(() => {
	return {
        color: showDealerHand.value ? '#f7ffe3' : 'transparent'
      };
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
	setTimeout(() => {
		snackbar.value = false
		showMoneyAnimation.value = false;
	}, 2500);
	gameStarted.value = false;
}

function handleMoney() {
	money.value += playerWin.value ? bet.value : -bet.value;
}

function updateBet(newBet) {
	bet.value = newBet;
}

</script>

<template>
	<BaseViewContainer style="background-color: rgb(100, 0 , 0);">
		<Scoreboard 
			:gameStarted="gameStarted" 
			:money="money" 
			@betChanged="updateBet"
		/>

		<MoneyAnimation 
			:isVisible="showMoneyAnimation" 
			:amount="50" 
			:duration="2"
			:win="playerWin"
		/>
		
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
				:style="{ transform: `rotate(${card.rotation}deg)`, paddingTop: '350px' }"
			/>
		</template>

		<span v-if="showDealerHand" id="dealers-hand-score">Dealer's Hand Value: {{ dealerHand.getTotalValue() }}</span>
		<template v-for="(card, index) in dealerHand" :key="index">
			<audio ref="handSlapSound" src="@/assets/hand-slap.mp3" preload="auto"></audio>
			<PlayingCardComponent 
				:card="card" 
				:startingX="initialDealerOffset - index * cardShift"  
				:startingY="380"
				:showCardValues="showDealerHand"
				:style="{ transform: `rotate(${card.rotation}deg)`, paddingTop: '350px' }"
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
	display: flex; /* Enable flexbox */
	justify-content: center; /* Center the text */
	align-items: center; /* Center vertically */
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