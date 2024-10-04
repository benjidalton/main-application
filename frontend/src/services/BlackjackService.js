import { PlayingCard } from "../models/PlayingCard.js";


const playerHand = [];
const dealerHand = [];
/**
 * Creates a deck of 52 cards, with number cards, face cards (Jack, Queen, King), and aces.
 * @returns {PlayingCard[]} A shuffled deck of cards
 */
export function createDeck() {
	const suits = [ "Hearts", "Diamonds", "Clubs", "Spades" ];
	const values = [ 2, 3, 4, 5, 6, 7, 8, 9, 10 ];
	const faceCards = [ "Jack", "Queen", "King" ];
	const deck = [];
	
  
	for (const suit of suits) {
		for (const value of values) {
			deck.push(new PlayingCard(suit, value, `${value}_of_${suit}.png`));
		}
	}
  
	for (const suit of suits) {
		for (const faceCard of faceCards) {
			deck.push(new PlayingCard(suit, faceCard, `${faceCard}_of_${suit}.png`));
		}
	}

	for (const suit of suits) {
		deck.push(new PlayingCard(suit, "Ace", `Ace_of_${suit}.png`));
	}
	return deck;
}

/**
 * Randomly chooses a card from the deck and then removes it from the deck.
 * @returns {PlayingCard} A random card
 */
export function dealCard() {
	if (deck.length === 0) {
		throw new Error("The deck is empty! Cannot deal more cards.");
	}
	const randomIndex = Math.floor(Math.random() * deck.length);

	// Remove the card at the random index from the deck and add it to dealt cards
	const dealtCard = deck.splice(randomIndex, 1)[0];
	return dealtCard;
}

export function initialDeal(hand1, hand2) {
	for (let i = 0; i < 4; i++) {
		if (i % 2 === 0) {
			hand1.push(dealCard())
		} else {
			hand2.push(dealCard())
		}
	}

	return
}

export function checkPlayerHandValue() {
	if (playerHand.getTotalValue() > 21) {
		console.log("Busted! Your total exceeds 21.");
		return true; 
	} else if (playerHand.getTotalValue() === 21) {
		console.log("Blackjack! You hit 21.");
		return true;
	}
	return false;
}


export const deck = createDeck();