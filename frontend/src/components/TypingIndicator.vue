<script setup>

</script>

<template>
	<div class="typing-indicator">
		<span></span><span></span><span></span>
	</div>
</template>


<style scoped>
.typing-indicator {
	display: inline-block;
}

.typing-indicator span {
	display: inline-block;
	width: 10px;
	height: 10px;
	margin: 0 4px;
	background-color: #333;
	border-radius: 50%;
	animation: bounce 1.4s infinite ease-in-out both;
}

.typing-indicator span:nth-child(1) {
	animation-delay: -0.32s;
}

.typing-indicator span:nth-child(2) {
	animation-delay: -0.16s;
}

@keyframes bounce {
	0%, 80%, 100% {
		transform: scale(0);
	}
	40% {
		transform: scale(1);
	}
}
</style>