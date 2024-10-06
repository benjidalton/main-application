<script setup>
import { ref } from 'vue';

const emit = defineEmits(['cardBackChanged'])

const cardBackOptions = ref([
    { label: "Black and Gold", imageUrl: '/src/assets/card-images/black_gold_back.png' },
    { label: "Shiny Black", imageUrl: '/src/assets/card-images/shiny_card_back.png' },
    { label: "Black Floral", imageUrl: '/src/assets/card-images/black_floral.jpg' },
    { label: "Crown", imageUrl: '/src/assets/card-images/crown_card_back.jpg' },
    { label: "Orange", imageUrl:  '/src/assets/card-images/orange_back.png' },
    { label: "Warp Drive", imageUrl:  '/src/assets/card-images/warp_drive_back.png' },
    { label: "Blue Star", imageUrl:  '/src/assets/card-images/blue_star_back.png' },
])

function selectCardBack(cardBack) {
    emit('cardBackChanged', cardBack.imageUrl); 
}

</script>

<template>
    <v-menu transition="scale-transition" >
		<template v-slot:activator="{ props }">
			<v-btn
				id="open-menu-button"
				v-bind="props"
			>
			<v-icon size="30px" style="padding-right: 20px;">mdi-cards-playing</v-icon>
			Choose Card Back
		</v-btn>
		</template>
        <v-list id="prompts-list">
            <v-list-item
                v-for="(cardBack, index) in cardBackOptions"
                :key="index"
                @click="selectCardBack(cardBack)"
                style="cursor: pointer;"
            >
            <!-- <v-card style="width: 100px; height: auto; margin: 5px; background-image: url(cardBack);"/> -->
            <v-img :src="cardBack.imageUrl" :key="index" max-height="120px"/>
            <!-- <v-list-item-title>{{ cardBack.label }}</v-list-item-title> -->
            </v-list-item>
        </v-list>
		</v-menu>

</template>


<style scoped>

#open-menu-button {
	position: absolute;
	top: 5px;
	right: 5px;
	z-index: 1000;
	height: 50px;
	width: fit-content;
	outline: 5px dotted #FFD700;
	border-radius: 5px;
	background-color: rgb(0, 0, 0);
	font-weight: bold;
	font-family: 'Casino';
	color: #FFD700;
	font-size: 24px;
}

#prompts-list {
	background-color: #f9fdee;
}


</style>