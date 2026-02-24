# Pico 2w in Memory Game

4-button memory/reaction game for Raspberry Pi Pico 2w in MicroPython.

## Features

- 4 buttons, 4 LEDs
- Reaction/memory rounds counted as score
- Local leaderboard saved to file
- Debug menu (BOOTSEL)
- Game time adjustable
- Does not record 0 rounds

## Wiring

- BUTTON 1 -> GP8 -> Button -> GND  
- BUTTON 2 -> GP9 -> Button -> GND  
- BUTTON 3 -> GP10 -> Button -> GND  
- BUTTON 4 -> GP11 -> Button -> GND  

- LED 1 -> GP12 -> 220Ω -> LED (+) -> GND  
- LED 2 -> GP13 -> 220Ω -> LED (+) -> GND  
- LED 3 -> GP14 -> 220Ω -> LED (+) -> GND  
- LED 4 -> GP15 -> 220Ω -> LED (+) -> GND  

BOOTSEL is built-in

## Leaderboard

Saves to the file specified in `leaderboard_file` in main.py. Default: `leaderboard.txt`.

## Debug Menu

Hold BOOTSEL if `debug_mode=True`:

- Show leaderboard
- Reset leaderboard
- Change game time

## License

MIT License
