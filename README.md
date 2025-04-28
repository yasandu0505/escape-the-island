# Stranded: Escape the Island 🌴🌴🌴🌴

## Overview
Stranded: Escape the Island is a text-based survival adventure game where you play as the lone survivor of a plane crash on a mysterious island. Your goal is to explore the island, manage your resources, and find a way to escape or be rescued.

## Game Features
- **Choice-Driven Gameplay**: Every decision impacts your journey and survival chances
- **Dynamic Map Exploration**: Visit multiple areas including the beach, jungle, river, and mountains
- **Resource Management**: Monitor your energy levels and collect survival items
- **Multiple Endings**: Achieve rescue, escape on your own, or face the consequences of poor choices
- **Random Events**: Encounter unexpected situations that can help or hinder your survival
- **Save/Load System**: Continue your adventure where you left off

## How to Play

### Installation
1. Ensure you have Python 3.6+ installed on your system
2. Clone this repository:
   ```
   git clone https://github.com/yourusername/stranded-game.git
   ```
3. Navigate to the game directory:
   ```
   cd stranded-game
   ```
4. Run the game:
   ```
   python stranded_game.py
   ```

### Commands
- Use single letter commands (n, s, e, w, etc.) to navigate between locations
- Special commands are available in specific locations:
  - `r` - Rest (at the beach)
  - `s` - Search (at the wreckage)
  - `f` - Fish (at the river)
  - `d` - Drink (at the river)
  - `s` - Signal for help (at the mountain peak)
  - `e` - Explore deeper (in the cave)
- Type `save` to save your game progress
- Type `quit` to exit the game

### Winning the Game
There are two ways to win:
1. **Rescue Ending**: Find equipment and signal for help from the mountain peak
2. **Escape Ending**: Discover a hidden path in the mysterious cave

Be careful with your energy! Every action costs energy, and if you run out without having supplies, your journey might come to an unfortunate end.

## Game Structure
The game is built with an object-oriented approach:
- `Location` class: Manages location descriptions and available options
- `Player` class: Tracks player state, inventory, and actions
- `Game` class: Controls game flow, map connections, and special events

## Future Enhancements
- Additional locations and secret areas
- Expanded crafting system
- Weather effects that impact gameplay
- More detailed inventory management
- NPC encounters and dialogues

## Credits
Developed by Yasandu Imanjith

## License
This project is licensed under the MIT License - see the LICENSE file for details.