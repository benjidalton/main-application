<script setup>

const props = defineProps({
	rules: Array
})
</script>

<template>

	<v-menu transition="scale-transition" >
		<template v-slot:activator="{ props }">
			<v-btn
				id="open-rules-button"
				v-bind="props"
			>
			<v-icon size="30px" style="padding-right: 20px;">mdi-information</v-icon>
			Blackjack Rules
		</v-btn>
		</template>
			<v-list id="prompts-list">
				<v-list-item
					v-for="(rule, index) in rules"
					:key="index"
					style="cursor: pointer;"
				>
				<v-list-item-title v-text="rule"></v-list-item-title>
				</v-list-item>
			</v-list>
		</v-menu>

</template>


<style scoped>
#open-rules-button {
	position: absolute;
	bottom: 5px;
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
	/* background-color: #f7ffe3; */
	background-color: #f9fdee;
}

</style>