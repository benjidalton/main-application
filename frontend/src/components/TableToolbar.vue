<script setup>
import { ref, computed, watch, onMounted } from 'vue';

const props = defineProps({
	title: {
		type: String
	}
});

const emit = defineEmits(['saveItem', 'searchText']);

const dialog = ref(false);
const newItem = ref('');
const search = ref('');

const label = computed(() => (`New ${props.title}`));

function toggleDialog() {
	dialog.value = !dialog.value;
	if (!dialog.value) {
		newItem.value = '';
	}
}

function save() {
	if (newItem.value != '') {
		emit('saveItem', newItem.value);
		toggleDialog();
	}
}

function emitSearch() {
	emit('searchText', search.value);
}
</script>

<template>
	<v-toolbar
		flat
		class="d-flex align-center"
		color="#3a3c45"
	>
		<v-row align="center">
			<v-col>
				<v-toolbar-title style="padding-left: 10px;">{{ props.title }}</v-toolbar-title>
			</v-col>
			<v-col cols="8">
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
			<v-col>
				<v-btn
					class="mb-2"
					dark
					v-bind="props"
					style="margin-top: 10px; font-weight: bold; color: aliceblue"
					@click="toggleDialog"
				>
					<v-icon icon="mdi-plus" style="font-size: 24px;"/>
					<span style="color: aliceblue;">New Item</span>
				</v-btn>
			</v-col>
		</v-row>
		
		
		<v-dialog
			v-model="dialog"
			max-width="500px"
			persistent
			@keyup.enter="save"
			
		>
			<v-card style="background-color: #e3e4e8;">
				<v-card-title>
					<span class="text-h5">New Item</span>
				</v-card-title>

				<v-card-text>
					<v-container>
						<v-row>
							<v-text-field
								v-model="newItem"
								:label=label
							></v-text-field>
						</v-row>
					</v-container>
				</v-card-text>

				<v-card-actions>
					<v-spacer></v-spacer>
					<v-btn
						color="red"
						variant="tonal"
						@click="toggleDialog"
						
					>
						Cancel
						<v-icon icon="mdi-close"/>
					</v-btn>
					<v-btn
						color="green"
						variant="tonal"
						@click="save"
						align="center"
					>
						Save
						<v-icon icon="mdi-content-save" color="success"/>
					</v-btn>
				</v-card-actions>
			</v-card>
		</v-dialog>
	</v-toolbar>
</template>


<style></style>