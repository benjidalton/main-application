<script setup>
import { ref } from 'vue';
const props = defineProps({
	gameStarted : Boolean,
	money: Number
})

const emit = defineEmits(['betChanged']);

const bet = ref(100);

const betOptions = ref([10, 20, 50, 100, 200]);

function selectBet(value) {
	bet.value = value;
	emit('betChanged', bet.value);
}

</script>

<template>

	<v-card id="scoreboard" >
		<v-card-title style="text-align: left; padding-top: 20px;">
			<span style="font-size: 40px; padding-top: 5px;">Money: </span>
			<div id="money-counter" >
				<span style="font-size: 40px;">{{ money }}</span>
			</div>
		</v-card-title>
		<v-row style="padding-top: 40px; padding-left: 50px; align-items: center">
			<v-icon icon="mdi-lock" v-if="gameStarted" style="padding-right: 20px; font-size: 40px;"/>
			<v-icon 
				icon="mdi-lock" 
				v-else 
				style="padding-right: 20px;  visibility: hidden;" 
				/>
			<span style="font-size: 40px;">Bet: </span>
			<div id="bet-counter">
				
				<v-menu transition="scale-transition" :disabled="gameStarted" offset-y attach="body">
					<template v-slot:activator="{ props }">
						<!-- <div id="bet-counter"> -->
							<span style="font-size: 40px;" v-bind="props" :style="'cursor: pointer'">{{ bet }}</span>
						<!-- </div> -->
					</template>
					<v-list id="prompts-list" style="right: 18px;">
						<v-list-item
							v-for="(option, index) in betOptions"
							:key="index"
							style="cursor: pointer;"
							@click="selectBet(option)"
						>
						<v-list-item-title v-text="option" style="font-family: Casino;"></v-list-item-title>
						</v-list-item>
					</v-list>
				</v-menu>
				
			</div>
		</v-row>
	</v-card>
</template>

<style scoped>


#scoreboard {
	position: absolute;
	top: 2vh;
	left: 38vw;
	width: 24vw;
	height: 20vh;  /* Increased height to fit the input */
	border: 5px dotted red;
	background-color: rgb(0, 0, 0);
	font-family: 'Casino';
	color: #FFD700;
	outline: 5px dotted #C0C0C0;
  
}

#money-counter {
	position: absolute;
	display: flex;
	top: 0;
	border: 2px solid rgb(39, 37, 37);
	border-radius: 5px;
	width: 50%;
	height: 80px;
	margin-top: 10px;
	margin-right: 20px;
	right: 0;
	background-color: rgb(243, 243, 243);
	justify-content: center;
	align-items: center;
	transition: border-color 0.5s ease-in-out;
	background-color: black
 
}
.highlight-border {
	border: 5px solid green;
	border-color: green; /* Highlight in green */
	animation: fadeOutBorder 3s forwards; /* Trigger fade out */
}

#bet-counter {
	position: absolute;
	display: flex;
	top: 0;
	border: 2px solid rgb(39, 37, 37);
	border-radius: 5px;
	width: 50%;
	height: 80px;
	margin-top: 100px;
	margin-right: 20px;
	right: 0;
	background-color: rgb(243, 243, 243);
	justify-content: center;
	align-items: center;
	background-color: black
}

#bet-input {
	font-size: 20px;
	text-align: center;
	justify-content: center;
	z-index:20;
}

#prompts-list {
	width: 100px;
	justify-content: center;
	text-align: center;
	background-color: #f7ffe3;
}

.v-list-item-title {
	padding: 5px;
	font-size: 30px;
}
</style>