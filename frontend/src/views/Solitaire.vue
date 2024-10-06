<script setup>
import { ref, computed, onMounted } from 'vue';
import { PlayingCard }from '@/models/PlayingCard.js'
import PlayingCardComponent from '@/components/BlackjackComponents/PlayingCardComponent.vue';
import BaseViewContainer from '@/components/BaseComponents/BaseViewContainer.vue';
import {  createDeck, shuffle } from '@/services/BlackjackService';
import { Hand } from '@/models/Hand.js';


const fakeCard = ref(new PlayingCard('Hearts', 'A', ''));
const cardShift = 70;
const initialOffset = 110;
const aces = ref([]);
const acesContainer = ref('');
const columnsContainer = ref('');
const currentDeck = ref(shuffle(createDeck()));
const visibleCardCount = computed(() => {
	return currentDeck.value.length >= 3 ? 3 : currentDeck.value.length;
})

const newCardOptions = computed(() => {

	return currentDeck.value.slice(0, visibleCardCount.value);
})

onMounted(() => {
	getAcesContainerCoordinates(); // Call this function when component is mounted
});


function getAcesContainerCoordinates() {
	// if (acesContainer.value) {
		const rect = document.getElementById('aces-container').getBoundingClientRect();
		console.log('Aces Container Coordinates:', rect);
		console.log('Top:', rect.top, 'Left:', rect.left);
		console.log('Width:', rect.width, 'Height:', rect.height);
	// }
}

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
	console.log('aces container', acesContainer.value)
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

function onAceDrop(event, index) {
	console.log('event', event)
    const cardData = JSON.parse(event.dataTransfer.getData('text/plain'));
    if (cardData.value === 'Ace') {
        aces.value[index] = cardData; // Place the Ace in the appropriate slot
        console.log('Ace dropped in slot:', index);
    }
}


</script>

<template>
	<BaseViewContainer style="background-color: rgb(100, 0 , 0);">

			<v-container id="deck-container">
				<PlayingCardComponent
					:card="fakeCard"
					:startingX="10"  
					:startingY="-500"
					style="transform: scale(50%); "
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
					style="transform: scale(50%);"
					:draggable="index === newCardOptions.length - 1"
					@dragstart="onDragStart"
					@dragend="onDragEnd"
				/>
			</template>
		</v-container>

		<v-container 
			ref="acesContainer"
			id="aces-container" 
			@dragover.prevent 
			@drop="event => onDrop(event)"  
		>
			<div 
				v-for="slot in 4" 
				:key="slot" 
				class="ace-slot" 
				@drop="event => onAceDrop(event, slot - 1)" 
				@dragover.prevent
				>
				<!-- Display the ace if it exists -->
				<div v-if="aces[slot - 1]" class="ace-card">
					<PlayingCardComponent :card="aces[slot - 1]" style="transform: scale(20%);" />
				</div>
			</div>
			<!-- Aces display logic -->
		</v-container>
		
		<v-container 
			ref="columnsContainer"
			id="columns-container" 
			@dragover.prevent 
			@drop="event => onDrop(event)"  
			style="position: relative;"
		>
			<div 
				v-for="slot in 7" 
				:key="slot" 
				class="column" 
				@dragover.prevent
				>
				<!-- Display the ace if it exists -->
				<!-- <div v-if="aces[slot - 1]" class="ace-card">
					<PlayingCardComponent :card="aces[slot - 1]" style="transform: scale(60%);" />
				</div> -->
			</div>
		</v-container>
	</BaseViewContainer>
</template>


<style scoped>
@import url('https://fonts.cdnfonts.com/css/casino');

#aces-container {
	position: absolute;
	display: flex;
	flex-direction: row;
	width: 45vw;
	height: 35vh;
	top: 0;
	right: 0;
	/* background-color: rgb(194, 194, 194);
	border: 5px solid gray; */
	border-radius: 10px;
	z-index: 0;
	align-items: center;
}

.ace-slot {
	width: 250px; 
	height: 275px; 
	/* background-color: rgb(211, 211, 211); 	 */
	border: 2px solid gray; 
	border-radius: 10px; 
	display: flex; 
	align-items: center;
}

#columns-container {
	position: absolute;
	display: flex;
	flex-direction: row;
	top: 10vh;
	width: 90vw;
	height: 55vh;
	background-color: rgb(194, 194, 194);
	border: 5px solid gray;
	border-radius: 10px;
	z-index: 0;
	align-items: center;
}

.column {
	width: 250px; 
	height: 100%; 
	/* background-color: rgb(211, 211, 211); 	 */
	border: 2px solid gray; 
	border-radius: 10px; 
	display: flex; 
	align-items: center;
}

</style>