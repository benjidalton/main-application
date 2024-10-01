<script setup>
import { ref, watch } from 'vue';
// import { VTextField, VRow, VCol, VIcon } from 'vuetify/lib/components/index.mjs';
const userPrompt = ref('');
const response = ref('');
const animationTrigger = ref(false);

const promptOptions = ["DB Query", "Normal"]
const selectedPromptOption = ref("DB Query");
const emit = defineEmits(['userPrompt', 'promptTypeChanged']);

function handleUserInput(event, source) {
	if (source == 'btn') {
		let defaultPrompt = 'Who are the top 5 home run hitters?';
		triggerSuccessAnimation();	
		emit('userPrompt', defaultPrompt, selectedPromptOption.value);
	}
	if ((source === 'enter'  && userPrompt.value != '') || (source === 'icon' && userPrompt.value != '')) {
		triggerSuccessAnimation();	
		emit('userPrompt', userPrompt.value, selectedPromptOption.value);
		userPrompt.value = '';
	}
}

const triggerSuccessAnimation = () => {
	animationTrigger.value = true;
	setTimeout(() => {
		animationTrigger.value = false;
	}, 1000); // Change this value according to your animation duration
};

watch(selectedPromptOption, (newValue) => {
	emit('promptTypeChanged', newValue);
});

</script>

<template>
	<v-row dense class="prompt-container">
		<v-col md="2">
			<v-select v-model="selectedPromptOption" :items="promptOptions" bg-color="rgb(255 255 255 / 92%)"/>

		</v-col>
			<v-col md="8">
				<v-text-field 
					class="user-prompt" 
					:label="selectedPromptOption === 'DB Query' ? 'What would you like to know about the current MLB season?' : 'How can I help you today?'"
					variant="outlined"
					clear-icon="mdi-close-circle"
					clearable
					v-model="userPrompt"
					bg-color="rgb(255 255 255 / 92%)"
					color="rgb(2, 81, 151)"
					@keyup.enter="handleUserInput($event, 'enter')"
				> 
					<template #append-inner>
						<span class="magic" :class="{ 'is-animated': animationTrigger }" @click="handleUserInput($event, 'icon')">
							<v-icon icon="mdi-arrow-right-circle-outline" />
						</span>
					</template>
				</v-text-field>
		</v-col>
	</v-row>
</template>

<style scoped>

.user-prompt {
	color: rgb(2, 81, 151);
}

.v-text-field {
	font-size: 20px;
}

.magic {
	display: inline-flex;
	align-items: center;
	transition: transform 1s ease, opacity 1s ease;
	padding-right: 20px;
	cursor: pointer;
}

.is-animated {
	transform: translateX(20px);
	opacity: 0;
}

</style>