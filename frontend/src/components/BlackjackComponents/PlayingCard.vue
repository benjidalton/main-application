<script setup>
import { PlayingCard } from '@/models/PlayingCard';
import { ref, computed } from 'vue';

const props = defineProps({
	card: {
		type: PlayingCard,
		required: true
	},
	startingX: {
		type: Number
	},
	showCardValues: {
		type: Boolean
	}

})

const image = ref(null)
const startX = ref(0);
const startY = ref(0);

const posX = ref(0);
const posY = ref(380);
const isDragging = ref(false);
const cardStyle = computed(() => {
	return {
        transform: `translate(${posX.value}px, ${posY.value}px) rotate(${props.card.rotation}deg)`, // Combine translation and rotation
        cursor: isDragging.value ? 'grabbing' : 'grab',
        position: 'absolute', // Ensure the card is absolutely positioned
        left: `${props.startingX + posX.value}px`, // Adjust left position based on drag
        top: `${posY.value}px`, // Set top position as needed (you can also use another ref for vertical position)
    };
})

function startDrag(event) {
	isDragging.value = true;
	startX.value = event.clientX - posX.value;
	startY.value = event.clientY - posY.value;
	window.addEventListener('mousemove', drag);
	window.addEventListener('mouseup', stopDrag);
}

function drag(event) {
	if (isDragging.value) {
		posX.value = event.clientX - startX.value;
		posY.value = event.clientY - startY.value;
	}
}
function stopDrag() {
	isDragging.value = false;
	window.removeEventListener('mousemove', drag);
	window.removeEventListener('mouseup', stopDrag);
}

</script>

<template>

	<div 
		class="draggable-card" 
		@mousedown="startDrag" 
		:style="cardStyle"
	>
		<v-card class="playing-card">
			<div>
				<div id="top-left-suit">
					<v-icon icon="mdi-cards-spade" />
					<span v-if="showCardValues" id="top-left-card-value"> {{ card.value }}</span>
				</div>
				<div id="bottom-right-suit">
					<v-icon icon="mdi-cards-spade" />
					<span v-if="showCardValues" id="bottom-right-card-value"> {{ card.value }}</span>
				</div>
			</div>
			
			<!-- <div class="card-content"> -->
				
		</v-card>
	</div>

	
</template>

<style scoped>

@import url('https://fonts.cdnfonts.com/css/casino');
.draggable-card {
  width: 200px; 
  height: 600px;
  bottom: 0;
  user-select: none;
  position: absolute;
}


.playing-card {
    width: 300px;
    height: 400px; 
    border: 3px solid #e6fbff; 
    border-radius: 10px; 
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
    background-color: #292929; 
    position: relative;           
    overflow: hidden;
	font-family: 'Casino';
	color: #FFD700;
	font-size: 35px;
}

.playing-card::before,
.playing-card::after {
    content: '';
    position: absolute;
    width: 0;
    height: 0;
    border-style: solid;
	
}

/* Top-right triangle */
.playing-card::before {
    border-width: 0 50px 50px 0; 
    border-color: transparent transparent #f7ffe3 transparent; /* Color for the triangle */
    top: 0px;
    right: 0;
	transform: rotate(180deg);	
}

/* Bottom-left triangle */
.playing-card::after {
    border-width: 50px 0 0 50px; /* Adjust size as needed */
    border-color: transparent transparent transparent #f7ffe3; /* Color for the triangle */
    bottom: 0;
    left: 0;
}

#top-left-suit {
    color: #f7ffe3;
    position: absolute; 
    top: 10px;
    left: 20px; 
}

#top-left-card-value {
    padding-left: 10px;
    font-size: 50px;
}

#bottom-right-suit {
    color: #f7ffe3;
    position: absolute;
    bottom: 10px;
    right: 20px;
    transform: rotate(180deg);
}

#bottom-right-card-value {
    padding-right: 20px; /* Adjust as needed */
    font-size: 50px; /* Adjust as needed */
}
.card-title {
    font-size: 36px; /* Bigger font for the value */
    font-weight: bold; /* Bold for emphasis */
}

.card-suit {
    font-size: 24px; /* Slightly smaller font for suit */
}
</style>
