<script setup>
import { ref, computed } from 'vue';
import { PlayingCard }from '@/models/PlayingCard.js'
import PlayingCardComponent from '@/components/BlackjackComponents/PlayingCardComponent.vue';
import BaseViewContainer from '@/components/BaseComponents/BaseViewContainer.vue';
import {  createDeck, shuffle } from '@/services/BlackjackService';
import { Hand } from '@/models/Hand.js';

const fakeCard = ref(new PlayingCard('Hearts', 'A', ''));
const cardShift = 70;
const initialOffset = 110;
const aces = ref([]);
const currentDeck = ref(shuffle(createDeck()));
const visibleCardCount = computed(() => {
	return currentDeck.value.length >= 3 ? 3 : currentDeck.value.length;
})

const newCardOptions = computed(() => {

	return currentDeck.value.slice(0, visibleCardCount.value);
})

const cardPositions = ref(newCardOptions.value.map((_, index) => ({
	index,
	startingX: 200 + index * cardShift,
	startingY: 0
})));

function displayNewCards() {
	// console.log('slice', currentDeck.value.slice(0, visibleCardCount.value))
	console.log('active cards', newCardOptions.value)
}

function onDragStart(card) {
    console.log('Dragging card:', card);
}

function onDragEnd(card) {
    console.log('Dropped card:', card);
}
function onDrop(event) {
	console.log('event', event)
	const cardData = JSON.parse(event.dataTransfer.getData('text/plain'));
    
    // Check if the card is an Ace
    if (cardData.value === 'Ace') {
        aces.value.push(cardData); // Add to aces
        console.log('Aces:', aces.value);
    } else {
		console.log('hello')
        // Reset the position of the card if not an Ace
        const cardIndex = newCardOptions.value.findIndex(c => c.value === cardData.value && c.suit === cardData.suit);
        if (cardIndex !== -1) {
            const originalPos = cardPositions.value[cardIndex];
            // Reset position logic can be implemented here
            // Here we would need to trigger a re-render to reflect the original positions
            cardPositions.value[cardIndex].startingX = originalPos.startingX;
            cardPositions.value[cardIndex].startingY = originalPos.startingY;
            console.log('Card returned to its original position:', originalPos);
        }
    }
}


</script>

<template>
	<BaseViewContainer style="background-color: rgb(100, 0 , 0);">
		<v-container id="deck-container">
			<PlayingCardComponent
				:card="fakeCard"
				:startingX="10"  
				style="transform: scale(60%); padding-bottom: 50px;"
				:draggable="false"
				@click="displayNewCards"
			/>
		</v-container>
		<v-container id="visible-cards">
			<template v-for="(card, index) in newCardOptions" :key="index">
				<PlayingCardComponent 
					:card="card"
					:startingX="200 + index * cardShift"  
					:startingY="0"
					:showCardValues="true"
					style="transform: scale(60%);"
					:draggable="index === newCardOptions.length - 1"
					@dragstart="onDragStart"
					@dragend="onDragEnd"
				/>
			</template>
		</v-container>

		<v-container 
            id="aces-container" 
            @dragover.prevent 
            @drop="event => onDrop(event)"  
            style="position: relative;"
        >
            <!-- Aces display logic -->
        </v-container>
	</BaseViewContainer>
</template>


<style scoped>
@import url('https://fonts.cdnfonts.com/css/casino');

#aces-container {
	position: relative;
	top: 5vh;
	right: 10vw;
	width: 30vw;
	height: 30vh;
	background-color: rgb(194, 194, 194);
	border: 5px solid gray;
	border-radius: 10px;
	z-index: 0;
}


</style>