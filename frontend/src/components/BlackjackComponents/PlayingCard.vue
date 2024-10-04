<script setup>
import { PlayingCard } from '@/models/PlayingCard';
import { ref, computed, onMounted } from 'vue';

const props = defineProps({
	card: {
		type: PlayingCard,
		required: true
	},
	startingX: {
		type: Number
	}

})

onMounted(() => {
	console.log('card: ', props.card)
	image.value = `/Users/benji/Programming/baseball-app/frontend/src/assets/card-images/${props.card.imagePath}`

	console.log(image.value)

})

const image = ref(null)
const startX = ref(0);
const startY = ref(0);

const posX = ref(0);
const posY = ref(0);
const isDragging = ref(false);
const cardStyle = computed(() => {
	return {
        transform: `translate(${posX.value}px, ${posY.value}px)`,
        cursor: isDragging.value ? 'grabbing' : 'grab',
		left: `${props.startingX}px`
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
	<!-- <v-card
		@dragstart="onDragStart"
		@dragend="onDragEnd"
		@drag="onDrag"
		draggable="true"
		:style="{ transform: `translate(${posX}px, ${posY}px)`, cursor: isDragging ? 'grabbing' : 'grab' }"
		class="draggable-card"
	>
		<v-card-title>Draggable Card</v-card-title>
		<v-card-text>
			You can drag this card around.
		</v-card-text>
	</v-card> -->

	<div 
		class="draggable-card" 
		@mousedown="startDrag" 
		:style="cardStyle"
	>
		<v-card class="playing-card">
			<!-- <img src="@/assets/card-images/2_of_Clubs.png"> -->
			<v-img v-if="image != null" :width="300" aspect-ratio="16/9" :src="''+image+''" class="card-image" />
			<v-card-title>{{ card.value }}</v-card-title>
			<v-card-text>
				{{ card.suit }}
			</v-card-text>
			</v-card>
	</div>

	
</template>

<style scoped>
.draggable-card {
  width: 200px; 
  height: 600px;
  bottom: 0;
  user-select: none;
  position: absolute;
}

.playing-card {
	background-color: rgb(210, 210, 255); 
	width: 200px; 
	height: 300px; 
	border: 3px solid gray
}
</style>
