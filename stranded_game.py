import json
import os
import random
import time

class Location:
    def __init__(self, name, description, options=None):
        self.name = name
        self.description = description
        self.options = options if options else {}
    
    def get_description(self):
        return self.description
    
    def get_options(self):
        return self.options
    
    def add_option(self, key, description, destination, energy_cost=1):
        self.options[key] = {
            "description": description,
            "destination": destination,
            "energy_cost": energy_cost
        }

class Player:
    def __init__(self, name="Survivor", energy=100, health=100, inventory=None):
        self.name = name
        self.energy = energy
        self.health = health
        self.inventory = inventory if inventory else []
        self.current_location = "beach"  # Starting location
    
    def move(self, destination, energy_cost):
        if self.energy >= energy_cost:
            self.energy -= energy_cost
            self.current_location = destination
            return True
        else:
            print("You don't have enough energy to do that!")
            return False
    
    def rest(self, amount=20):
        self.energy = min(100, self.energy + amount)
        print(f"You rested and regained some energy. Current energy: {self.energy}")
    
    def eat(self, food_item, energy_gain=15):
        if food_item in self.inventory:
            self.inventory.remove(food_item)
            self.energy = min(100, self.energy + energy_gain)
            print(f"You ate {food_item} and gained energy. Current energy: {self.energy}")
            return True
        else:
            print(f"You don't have {food_item} in your inventory!")
            return False
    
    def add_to_inventory(self, item):
        self.inventory.append(item)
        print(f"Added {item} to your inventory!")
    
    def get_status(self):
        return f"\nSTATUS:\nEnergy: {self.energy}/100\nHealth: {self.health}/100\nInventory: {', '.join(self.inventory) if self.inventory else 'Empty'}"

class Game:
    def __init__(self):
        self.player = Player()
        self.locations = self.initialize_locations()
        self.game_over = False
        self.days_passed = 1
        self.ending = None
    
    def initialize_locations(self):
        # Define all the locations in the game
        locations = {
            "beach": Location(
                "Beach",
                "You are on the beach where your plane crashed. The waves crash gently on the shore. "
                "You can see parts of the wreckage scattered around."
            ),
            "jungle_edge": Location(
                "Jungle Edge",
                "You stand at the edge of a dense jungle. The vegetation is thick, and you can hear strange noises coming from within."
            ),
            "jungle_deep": Location(
                "Deep Jungle",
                "You're deep within the jungle. The canopy above blocks much of the sunlight. It's humid and difficult to see far."
            ),
            "river": Location(
                "River",
                "A rapid river cuts through the landscape. The water looks fresh but flows quickly."
            ),
            "mountain_base": Location(
                "Mountain Base",
                "You're at the base of a large mountain. The path upward looks steep and treacherous."
            ),
            "mountain_peak": Location(
                "Mountain Peak",
                "You've reached the peak of the mountain. From here, you can see the entire island and the vast ocean beyond."
            ),
            "cave": Location(
                "Mysterious Cave",
                "A dark cave with strange markings on the walls. Something about this place feels unnatural."
            ),
            "wreckage": Location(
                "Plane Wreckage",
                "What remains of your plane. Maybe there are useful supplies to salvage."
            )
        }
        
        # Define connections between locations
        locations["beach"].add_option("n", "Go north along the beach", "jungle_edge", 2)
        locations["beach"].add_option("w", "Explore the plane wreckage", "wreckage", 3)
        locations["beach"].add_option("r", "Rest on the beach", "beach", 0)
        
        locations["wreckage"].add_option("e", "Return to the beach", "beach", 1)
        locations["wreckage"].add_option("s", "Search the wreckage for supplies", "wreckage", 5)
        
        locations["jungle_edge"].add_option("s", "Return to the beach", "beach", 2)
        locations["jungle_edge"].add_option("n", "Enter the deep jungle", "jungle_deep", 4)
        locations["jungle_edge"].add_option("e", "Go to the river", "river", 3) 
        
        locations["jungle_deep"].add_option("s", "Go back to the jungle edge", "jungle_edge", 3)
        locations["jungle_deep"].add_option("w", "Climb toward the mountain", "mountain_base", 5)
        locations["jungle_deep"].add_option("e", "Investigate a strange rock formation", "cave", 4)
        
        locations["river"].add_option("w", "Return to the jungle edge", "jungle_edge", 3)
        locations["river"].add_option("f", "Try to catch fish", "river", 4)
        locations["river"].add_option("d", "Drink from the river", "river", 1)
        
        locations["mountain_base"].add_option("e", "Return to the deep jungle", "jungle_deep", 3)
        locations["mountain_base"].add_option("u", "Climb up the mountain", "mountain_peak", 7)
        
        locations["mountain_peak"].add_option("d", "Descend to the mountain base", "mountain_base", 3)
        locations["mountain_peak"].add_option("s", "Try to signal for help", "mountain_peak", 5)
        
        locations["cave"].add_option("w", "Exit the cave", "jungle_deep", 2)
        locations["cave"].add_option("e", "Explore deeper into the cave", "cave", 4)
        
        return locations
    
    def display_location(self):
        current_loc = self.player.current_location
        location = self.locations[current_loc]
        print("\n" + "="*50)
        print(f"DAY {self.days_passed} - {location.name}")
        print("="*50)
        print(location.get_description())
        print(self.player.get_status())
        print("\nOptions:")
        for key, option in location.get_options().items():
            print(f"  [{key}] {option['description']} (Energy cost: {option['energy_cost']})")
    
    def handle_special_actions(self, choice):
        current_loc = self.player.current_location
        
        # Handle resting
        if current_loc == "beach" and choice == "r":
            self.player.rest()
            return True
            
        # Handle searching the wreckage
        elif current_loc == "wreckage" and choice == "s":
            if random.random() < 0.6:  # 60% chance to find something
                items = ["water bottle", "energy bar", "first aid kit", "rope", "flashlight"]
                item = random.choice(items)
                self.player.add_to_inventory(item)
            else:
                print("You searched but found nothing useful.")
            return True
            
        # Handle fishing
        elif current_loc == "river" and choice == "f":
            if random.random() < 0.4:  # 40% chance to catch fish
                self.player.add_to_inventory("fish")
            else:
                print("You tried to catch fish but weren't successful.")
            return True
            
        # Handle drinking from the river
        elif current_loc == "river" and choice == "d":
            self.player.energy = min(100, self.player.energy + 10)
            print("You drink from the river and feel refreshed. Energy +10")
            return True
            
        # Handle signaling for help
        elif current_loc == "mountain_peak" and choice == "s":
            if "flashlight" in self.player.inventory:
                print("You use your flashlight to signal for help!")
                if random.random() < 0.3:  # 30% chance of rescue
                    print("You see a ship in the distance! They've spotted your signal!")
                    self.ending = "rescue"
                    self.game_over = True
                else:
                    print("You signal for a while, but no one seems to notice.")
            else:
                print("You try to signal, but without proper equipment, it's not very effective.")
            return True
            
        # Handle cave exploration
        elif current_loc == "cave" and choice == "e":
            if "flashlight" in self.player.inventory:
                print("Using your flashlight, you explore deeper and discover ancient carvings...")
                if random.random() < 0.2:  # 20% chance to find escape route
                    print("The carvings reveal a hidden path that might lead off the island!")
                    self.ending = "escape"
                    self.game_over = True
            else:
                print("It's too dark to explore further without a light source.")
            return True
            
        return False
    
    def process_turn(self, choice):
        # First check if it's a special action
        if self.handle_special_actions(choice):
            return
            
        # Otherwise, process as movement
        current_loc = self.player.current_location
        options = self.locations[current_loc].get_options()
        
        if choice in options:
            destination = options[choice]["destination"]
            energy_cost = options[choice]["energy_cost"]
            
            if self.player.move(destination, energy_cost):
                # Successfully moved
                if random.random() < 0.2:  # 20% chance of a random event
                    self.random_event()
        else:
            print("Invalid choice. Please try again.")
    
    def random_event(self):
        events = [
            "You find a wild fruit tree! +10 energy",
            "You trip and fall, twisting your ankle. -5 energy",
            "A sudden rain shower passes over. You collect some fresh water.",
            "You spot some animal tracks. Maybe you could hunt for food?",
            "The weather turns stormy, making travel more difficult."
        ]
        
        event = random.choice(events)
        print(f"\nRANDOM EVENT: {event}")
        
        if "wild fruit" in event:
            self.player.energy = min(100, self.player.energy + 10)
        elif "twist" in event:
            self.player.energy = max(0, self.player.energy - 5)
        elif "water" in event:
            self.player.add_to_inventory("water bottle")
    
    def check_game_state(self):
        # Check if player ran out of energy
        if self.player.energy <= 0:
            print("\nYou've collapsed from exhaustion...")
            if "food" in self.player.inventory or "water bottle" in self.player.inventory or "energy bar" in self.player.inventory:
                print("Fortunately, you had some supplies to help you recover.")
                self.player.energy = 30
            else:
                print("Without any supplies to help you recover, you succumb to the elements.")
                self.ending = "death"
                self.game_over = True
        
        # Check if a day has passed (every 5 turns)
        if self.days_passed % 5 == 0:
            self.days_passed += 1
            print(f"\nA new day dawns. It's day {self.days_passed} on the island.")
            # Reduce energy overnight
            self.player.energy = max(0, self.player.energy - 10)
            print("You lost some energy overnight.")
    
    def save_game(self):
        save_data = {
            "player": {
                "name": self.player.name,
                "energy": self.player.energy,
                "health": self.player.health,
                "inventory": self.player.inventory,
                "current_location": self.player.current_location
            },
            "days_passed": self.days_passed,
            "game_over": self.game_over,
            "ending": self.ending
        }
        
        with open("island_survival_save.json", "w") as save_file:
            json.dump(save_data, save_file)
        
        print("\nGame saved successfully!")
    
    def load_game(self):
        try:
            with open("island_survival_save.json", "r") as save_file:
                save_data = json.load(save_file)
            
            self.player = Player(
                name=save_data["player"]["name"],
                energy=save_data["player"]["energy"],
                health=save_data["player"]["health"],
                inventory=save_data["player"]["inventory"]
            )
            self.player.current_location = save_data["player"]["current_location"]
            self.days_passed = save_data["days_passed"]
            self.game_over = save_data["game_over"]
            self.ending = save_data["ending"]
            
            print("\nGame loaded successfully!")
            return True
        except (FileNotFoundError, json.JSONDecodeError):
            print("\nNo valid save file found.")
            return False
    
    def display_ending(self):
        print("\n" + "="*50)
        print("GAME OVER")
        print("="*50)
        
        if self.ending == "rescue":
            print("""
            After days of struggling to survive, your signals from the mountain peak were finally spotted!
            A rescue helicopter arrives, and you're taken back to civilization.
            You've escaped the island, but the mysteries you discovered will stay with you forever.
            """)
        elif self.ending == "escape":
            print("""
            Following the ancient carvings in the cave, you discovered a hidden underground river.
            Building a makeshift raft, you navigated through a tunnel that led you to the open sea.
            Against all odds, you were picked up by a passing fishing vessel two days later.
            The island's secrets remain, waiting for someone else to discover them...
            """)
        elif self.ending == "death":
            print("""
            The harsh realities of survival on the island proved too much.
            Without energy to continue, you succumbed to exhaustion and the elements.
            Perhaps the next castaway will have better luck unraveling the island's mysteries...
            """)
    
    def play(self):
        # Game introduction
        print("\n" + "="*50)
        print("STRANDED: ESCAPE THE ISLAND")
        print("="*50)
        print("""
        Your plane has crashed on a mysterious island. You are the only survivor.
        Explore the island, find resources, and try to find a way to escape or signal for rescue.
        But be careful - every action costs energy, and if you run out, your journey may come to an end.
        
        Good luck, survivor!
        """)
        
        load_choice = input("Would you like to load a saved game? (y/n): ").lower()
        if load_choice == 'y':
            if not self.load_game():
                self.player.name = input("Enter your name, survivor: ")
        else:
            self.player.name = input("Enter your name, survivor: ")
        
        # Main game loop
        while not self.game_over:
            self.display_location()
            
            action = input("\nWhat would you like to do? (or type 'save' to save game, 'quit' to exit): ").lower()
            
            if action == 'save':
                self.save_game()
                continue
            elif action == 'quit':
                save_before_quit = input("Would you like to save before quitting? (y/n): ").lower()
                if save_before_quit == 'y':
                    self.save_game()
                print("Thanks for playing!")
                break
            
            self.process_turn(action)
            self.check_game_state()
        
        if self.game_over:
            self.display_ending()
            print("\nThanks for playing STRANDED: ESCAPE THE ISLAND!")

if __name__ == "__main__":
    game = Game()
    game.play()