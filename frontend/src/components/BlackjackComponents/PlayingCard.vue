<script setup>
import { ref } from 'vue';


const posX = ref(0);
const posY = ref(0);
const isDragging = ref(false);

function onDragStart(event) {
	isDragging.value = true;
  	event.dataTransfer.setData('text/plain', ''); // You can set your data here
};

function onDragEnd() {
	isDragging.value = false;
};

function onDrag(event) {
	posX.value += event.movementX;
  	posY.value += event.movementY;
};

function allowDrop(event) {
	event.preventDefault();
};
</script>

<template>
	<v-card
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
	</v-card>

	
</template>

<style scoped>
.draggable-card {
  width: 200px; /* Set width as needed */
  user-select: none; /* Prevent text selection */
  position: absolute; /* Important for positioning */
}
</style>
