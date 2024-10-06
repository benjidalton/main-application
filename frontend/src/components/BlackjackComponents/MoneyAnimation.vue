<script setup>
import { ref, watch } from 'vue';

const props = defineProps({
	isVisible: Boolean,
	amount: Number, 
	duration: Number
});

const coins = ref([]);

watch(() => props.amount, (newAmount) => {
	if (newAmount > 0) {
		coins.value = Array(newAmount).fill(0);

		
		// Fade out the coins after the animation is done
		setTimeout(() => {
			props.isVisible = false;
		}, props.duration + 500); // Adjust time to ensure fade-out happens after bounce
	}
});

</script>

<template>
	<div v-if="isVisible" class="coin-animation">
		<div
			class="coin coin--animated"
			style="--coin-to-x: calc(-100px + 24px); --coin-to-y: calc(-105px + 24px); --coin-delay: 0.3s;"
		></div>
		<div
			class="coin coin--animated"
			style="--coin-to-x: calc(-70px + 24px); --coin-to-y: -90px; --coin-delay: 0.1s;"
		></div>
		<div
			class="coin coin--animated"
			style="--coin-to-x: calc(-30px + 24px); --coin-to-y: -125px; --coin-delay: 0s;"
		></div>
		<div
			class="coin coin--animated"
			style="--coin-to-x: calc(10px + 24px); --coin-to-y: -130px; --coin-delay: 0.2s;"
		></div>
		<div
			class="coin coin--animated"
			style="--coin-to-x: calc(30px + 24px); --coin-to-y: -100px; --coin-delay: 0.1s;"
		></div>
		<div
			class="coin coin--animated"
			style="--coin-to-x: calc(70px + 24px); --coin-to-y: -95px; --coin-delay: 0.4s;"
		></div>
		<div
			class="coin coin--animated"
			style="--coin-to-x: calc(100px + 24px); --coin-to-y: -100px; --coin-delay: 0.2s;"
		></div>
	<div
			class="coin coin--animated"
			style="--coin-to-x: calc(30px + 24px); --coin-to-y: -100px; --coin-delay: 0.1s;"
		></div>
		<div
			class="coin coin--animated"
			style="--coin-to-x: calc(70px + 24px); --coin-to-y: -95px; --coin-delay: 0.4s;"
		></div>
		<div
			class="coin coin--animated"
			style="--coin-to-x: calc(100px + 24px); --coin-to-y: -100px; --coin-delay: 0.2s;"
		></div>
	</div>
</template>


<style scoped>

.coin-animation {
	position: relative;
	display: flex;
	justify-content: center;
	align-items: flex-end;
	padding-right: 50px;
	padding-bottom: 10px;
}

.coin {
	position: absolute;
	top: 24px; /* Adjusted position if needed */
	left: 24px; /* Adjusted position if needed */
	z-index: 100;
	opacity: 0; /* Start hidden */
}

.coin::after {
	content: "$";
	display: flex;
	align-items: center;
	justify-content: center;
	width: 12px;
	height: 12px;
	font-size: 10px;
	color: rgb(237, 196, 107);
	background: rgb(227, 162, 23);
	border: 2px solid rgb(237, 196, 107);
	border-radius: 50%;
	opacity: 0;
	
}

.coin--animated,
.coin--animated::after {
	animation-delay: var(--coin-delay, 0s);
	animation-duration: var(--coin-duration, 1.5s);
	animation-direction: normal;
	animation-fill-mode: both;
	animation-play-state: running;
	animation-iteration-count: infinite;
	
}

.coin--animated {
	animation-name: coin-x-axis;
	animation-timing-function: ease-in;
}

.coin--animated::after {
	animation-name: coin-y-axis-and-flip;
	animation-timing-function: ease-out;
}

@keyframes coin-x-axis {
	30% {
		opacity: 1;
	}
	70% {
		opacity: 1;
	}
	to {
		left: calc(var(--coin-to-x) * 1.5);
	}
}

@keyframes coin-y-axis-and-flip {
	30% {
opacity: 1;
	}
	70% {
	opacity: 1;
	}
	to {
	transform: translateY(calc(var(--coin-to-y) * 1.5)) rotate3d(1, 1, 1, 1080deg);
	}
}
</style>