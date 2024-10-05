export class Hand extends Array {
	
	getTotalValue() {
		let aceCount = 0;
		let total = this.reduce((total, card) => {
			if (typeof card.value === 'number') {
				return total + card.value;
			} else if (card.value === 'Jack' || card.value === 'Queen' || card.value === 'King') {
				return total + 10;
			} else if (card.value === 'Ace') {
				aceCount += 1; // Increment Ace count
				return total + 11; // Treat Ace as 11 initially
			}
			return total;
		}, 0);
	
		// Adjust for Aces if total exceeds 21
		while (total > 21 && aceCount > 0) {
			total -= 10; // Reduce total by 10 for each Ace
			aceCount -= 1; // Treat an Ace as 1 instead of 11
		}
		return total;
	}

	toString() {
		return this.map(card => `${card.value} of ${card.suit}`).join(', ');
	}
}