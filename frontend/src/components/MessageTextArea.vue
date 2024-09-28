<script setup>

const props = defineProps({
	message: {
		user: String,
		prompt: String
	}
});
</script>

<template>
	<v-row class="row" dense align="center">
		<v-col md="1">
			<v-icon v-if="props.message.user==='human'" icon="mdi-account-star" style="transform: scale(150%);"></v-icon>
		</v-col>
		<v-col md=10>
			<div class="message-container">
				<div class="message-content">
					<p class="message">
						{{ props.message.text }}
					</p>
				</div>
			</div>
		</v-col>
		<v-col md="1">
			<v-icon v-if="props.message.user==='ai'" icon="mdi-robot-happy" style="transform: scale(150%);"></v-icon>
		</v-col>
	</v-row>
</template>

<style scoped>
.row {
	background-color: rgb(185, 185, 185);
	margin: 5px;
	border: 2px solid gray;
}
.text-field {
	color: rgb(39, 38, 51);
	font-size: 250px;
	transform: translate(0%, 15%);
}
.message-container {
	display: flex;
	position: relative;
	height: auto;
	width: 100%;
	/* border: 2px solid rgb(56, 51, 51); */
	border-radius: 15px;
	overflow-x: hidden;
	overflow-y: hidden;
	margin-top: 10px;
	margin-bottom: 10px;
	justify-content: center;
	align-items: center;
}
.message-container .message-content {
	display: flex;
	flex-direction: column;
	justify-content: center;
}
.message-container .message-content .message {
	font-size: 22px;
	text-align: left;
	margin-right: 150px;
	margin-left: 100px; 
	user-select: none;
}
</style>