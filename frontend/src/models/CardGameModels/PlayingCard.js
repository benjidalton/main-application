export class PlayingCard {
	constructor(suit, value, imagePath) {
		this.suit = String(suit);
		this.value = value;
		this.imagePath = imagePath;
		this.rotation = Math.floor(Math.random() * (-25 - 10 + 1)) + 10;
	}
}