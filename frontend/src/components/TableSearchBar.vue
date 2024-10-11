<script setup>
import { ref, computed, watch, onMounted } from 'vue';

const props = defineProps({
	title: {
		type: String
	}
});

const emit = defineEmits(['searchText']);

const search = ref('');

function emitSearch() {
	emit('searchText', search.value);
}
</script>

<template>
	<v-toolbar
		flat
		class="d-flex align-center"
		style="background-color: var(--custom-card-bg-opacity); border-top-left-radius: 10px; border-top-right-radius: 10px;"
	>
		<v-row align="center">
			<v-col style="padding: 50px;">
				<v-text-field
					v-model="search"
					label="Search"
					prepend-inner-icon="mdi-magnify"
					variant="outlined"
					hide-details
					single-line
					@input="emitSearch"
				></v-text-field>
			</v-col>
		</v-row>
	</v-toolbar>
</template>


<style>

</style>