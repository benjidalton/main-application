<script setup>

</script>

<template>
<v-container class="container" fluid>
	<slot></slot>

</v-container>
</template>

<style scoped>
.container {
	position: relative;
	display: flex;
	flex-direction: column;
	padding: 0;
	margin-top: 62px;
	box-sizing: border-box;
	justify-content: center;
	align-content: center;
	align-items: center;
	overflow-y: hidden;
	height: calc(100vh - 60px);
	/* border: 5px solid red;	 */
	background-color: rgb(247, 247, 247);
	overflow: hidden;
	
}
</style>