import { PlayingCard } from "../models/PlayingCard.js";
import { createInterface } from 'readline';

class Hand extends Array {
	
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
		console.log('this', this)
		return this.map(card => `${card.value} of ${card.suit}`).join(', ');
	}
}

// Create a readline interface for user input
const rl = createInterface({
    input: process.stdin,
    output: process.stdout
});

// Function to prompt the user for input
function promptUser(query) {
    return new Promise((resolve) => {
        rl.question(query, (answer) => {
            resolve(answer);
        });
    });
}





let playerHand = new Hand();
let dealerHand = new Hand();
/**
 * Creates a deck of 52 cards, with number cards, face cards (Jack, Queen, King), and aces.
 * @returns {PlayingCard[]} A shuffled deck of cards
 */
function createDeck() {
	const suits = [ "Hearts", "Diamonds", "Clubs", "Spades" ];
	const values = [ 2, 3, 4, 5, 6, 7, 8, 9, 10 ];
	const faceCards = [ "Jack", "Queen", "King" ];
	const deck = [];
  
	let id = 1;
	for (const suit of suits) {
		for (const value of values) {
			deck.push(new PlayingCard(id, suit, value, ''));
		}
	}
  
	for (const suit of suits) {
		for (const faceCard of faceCards) {
			deck.push(new PlayingCard(id, suit, faceCard, ''));
		}
	}

	for (const suit of suits) {
		deck.push(new PlayingCard(id, suit, "Ace", ''));
	}
	console.log('id', id)
  
	return deck;
}



let deck = createDeck();
console.log('deck: ', deck)

/**
 * Randomly chooses a card from the deck and then removes it from the deck.
 * @returns {PlayingCard} A random card
 */
function dealCard() {
	if (deck.length === 0) {
		throw new Error("The deck is empty! Cannot deal more cards.");
	}
	const randomIndex = Math.floor(Math.random() * deck.length);

	// Remove the card at the random index from the deck and add it to dealt cards
	const dealtCard = deck.splice(randomIndex, 1)[0];
	return dealtCard;
}

function initialDeal() {
	for (let i = 0; i < 4; i++) {
		if (i % 2 === 0) {
			playerHand.push(dealCard())
		} else {
			dealerHand.push(dealCard())
		}
	}
}

initialDeal();

async function playGame() {
    while (true) {
        console.log("Your hand:", playerHand.toString());
        console.log("Total value:", playerHand.getTotalValue());

        if (playerHand.getTotalValue() > 21) {
            console.log("Busted! Your total exceeds 21.");
            break; 
        } else if (playerHand.getTotalValue() === 21) {
            console.log("Blackjack! You hit 21.");
            break;
        }

        const choice = await promptUser("Do you want to 'hit' or 'stand'? ");
        
        if (choice === 'hit') {
			playerHand.push(dealCard());
        } else if (choice === 'stand') {
            console.log("You chose to stand.");
            break;
        } else {
            console.log("Invalid choice. Please type 'hit' or 'stand'.");
        }
    }
    rl.close(); // Close the readline interface
}

// Start the game
playGame();