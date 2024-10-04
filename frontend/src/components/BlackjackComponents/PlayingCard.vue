<script setup>
import { ref, computed } from 'vue';


const startX = ref(0);
const startY = ref(0);

const posX = ref(0);
const posY = ref(0);
const isDragging = ref(false);
const cardStyle = computed(() => {
	return {
        transform: `translate(${posX.value}px, ${posY.value}px)`,
        cursor: isDragging.value ? 'grabbing' : 'grab',
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
		<v-card>
		<v-card-title>Drag Me!</v-card-title>
		<v-card-text>
			You can drag this card around the screen.
		</v-card-text>
		</v-card>
	</div>

	
</template>

<style scoped>
.draggable-card {
  width: 200px; 
  user-select: none;
  position: absolute;
}
</style>
