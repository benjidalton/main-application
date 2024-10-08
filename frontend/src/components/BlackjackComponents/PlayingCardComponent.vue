<script setup>
import { PlayingCard } from '@/models/CardGameModels/PlayingCard';
import { ref, computed } from 'vue';

const props = defineProps({
	card: {
		type: PlayingCard,
		required: true
	},
	cardBack: {
		type: String,
	},
	startingX: {
		type: Number
	},
	startingY: {
		type: Number
	},	
	showCardValues: {
		type: Boolean
	},
	draggable: {
		type: Boolean,
		default: true 
	}

})

const emit = defineEmits(['dragstart', 'dragend'])

const startX = ref(0);
const startY = ref(0);

const posX = ref(0);
const posY = ref(0);
const isDragging = ref(false);

const cardColor = computed(() => {
	return props.card.suit === 'Spades' || props.card.suit === 'Clubs' ? 'black' : 'red';
});

const valueColor = computed(() => {
	return props.card.suit === 'Spades' || props.card.suit === 'Clubs' ? 'black' : 'red';
});

const cardStyle = computed(() => {
	return {
		transform: `translate(${posX.value}px, ${posY.value}px) rotate(${props.card.rotation}deg)`, // Combine translation and rotation
		cursor: isDragging.value ? 'grabbing' : 'grab',
		position: 'absolute', 
		left: `${props.startingX + posX.value}px`,
		top: `${posY.value}px`,
		zIndex: isDragging.value ? 10 : 1
	};
})

const cardBackStyle = computed(() => {
	return {
		backgroundImage: `url(${props.cardBack})`
	}
})

function getIcon(suit) {
    switch (suit) {
        case 'Hearts':
            return 'mdi-cards-heart';
        case 'Diamonds':
            return 'mdi-cards-diamond';
        case 'Clubs':
            return 'mdi-cards-club';
        case 'Spades':
            return 'mdi-cards-spade';
        default:
            return 'mdi-cards';
    }
}

function startDrag(event) {
	if (!props.draggable) return; 
	isDragging.value = true;
	startX.value = event.clientX - posX.value;
	startY.value = event.clientY - posY.value;
	console.log('start x', startX.value, '\nstart y', startY.value)
	emit('dragstart', props.card);
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
	emit('dragend', props.card);
	console.log('start x at drop', startX.value, '\nstart y at drop', startY.value)
	console.log('x at drop:', posX.value, 'y at drop', posY.value)
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
			<div v-if="showCardValues" >
                <div id="top-left-suit" :style="{ color: cardColor }">
                    <v-icon :icon="getIcon(props.card.suit)" />
                    <span 
						id="top-left-card-value" 
						:style="{ color: valueColor }"
					> 
					{{ card.value.length > 0 ? card.value[0] : card.value }}
				</span>
                </div>
				<div id="bottom-right-suit" :style="{ color: cardColor }">
                    <v-icon :icon="getIcon(props.card.suit)" />
                    <span 
						id="bottom-right-card-value" 
						:style="{ color: valueColor }"
					>
					 {{ card.value.length > 0 ? card.value[0] : card.value }}</span>
                </div>
			</div>

			<div v-else="showCardValues" >
				<v-card class="card-back" :style="cardBackStyle">
				</v-card>
			</div>
			
			<!-- <div class="card-content"> -->
				
		</v-card>
	</div>

	
</template>

<style scoped>

@import url('https://fonts.cdnfonts.com/css/casino');
@font-face {
    font-family: 'JQKas Wild Font';
    src: url('@/assets/fonts/JqkasWild-w1YD6.ttf') format('truetype'); /* Adjust path as necessary */
    font-weight: normal;
    font-style: normal;
}

.draggable-card {
	width: 300px;
	height: 400px; 
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
	background-color: #e6fbff;
	position: relative;           
	overflow: hidden;
	font-family: 'JQKas Wild Font';
	color: #FFD700;
	font-size: 35px;
	z-index: 100;
}


/* Top-right triangle */

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
	padding-right: 20px; 
	font-size: 50px; 
}
.card-title {
	font-size: 36px;
	font-weight: bold; 
}

.card-suit {
	font-size: 24px;
}


.card-back {
    width: 300px;
    height: 400px;
    border: 5px solid #000000;
    border-radius: 10px;
    background-size: 110%; /* Scale the image to cover the entire area */
    background-position: center; 
    position: relative;
    overflow: hidden;
    z-index: 50;
}

</style>
