<script setup>

import Table from '@/components/Table.vue';
// import TopNavBar from './components/TopNavBar.vue'

</script>

<template>
	<v-toolbar></v-toolbar>
		<v-sheet>
			<Table />
		</v-sheet>
</template>


<style scoped>
#app {
	font-family: Avenir, Helvetica, Arial, sans-serif;
	-webkit-font-smoothing: antialiased;
	-moz-osx-font-smoothing: grayscale;
	text-align: center;
	color: #2c3e50;
	margin-top: 60px;
}
#sticky-nav {
	position: fixed;
	top: 0;
	z-index: 10;
	height: auto;
	/* background-color: white; */
}
</style>