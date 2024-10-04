export class Hand extends Array {
	
	getTotalValue() {
		return this.reduce((total, card) => {
			if (typeof card.value === 'number') {
				return total + card.value;
			} else if (card.value === 'Jack' || card.value === 'Queen' || card.value === 'King') {
				return total + 10;
			} else if (card.value === 'Ace') {
				return total + 11;
			}
			return total;
		}, 0);
	}

	toString() {
		return this.map(card => `${card.value} of ${card.suit}`).join(', ');
	}
}