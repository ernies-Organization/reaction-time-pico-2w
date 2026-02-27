# Pico 2w in Memory Game

4-button memory/reaction game for Raspberry Pi Pico 2w in MicroPython.

## Features

- 4 buttons, 4 LEDs
- Reaction/memory rounds counted as score
- Local leaderboard saved to file
- Debug menu (BOOTSEL)
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

I used this [Breadboard Kit for Raspberry Pi Pico](https://thepihut.com/products/breadboard-kit-for-raspberry-pi-pico?utm_source=shop_app&list_generator=link_to_storefront&context=order_detail&user_id=777061826) (from the [pi hut](https://thepihut.com/))

## How to add the code

[Getting Started with Raspberry Pi Pico: Setup & First Script](https://raspberrytips.com/getting-started-with-raspberry-pi-pico/) ([raspberrytips](https://raspberrytips.com/))

![cropped-RaspberryTips](https://github.com/user-attachments/assets/d3cc1846-2d03-4a0b-9284-c47954c3f5ec)

## Leaderboard

Saves to the file specified in `leaderboard_file` in [memory_game.py](https://github.com/ernies-Organization/reaction-time-pico-2w/blob/main/memory_game.py). Default: `leaderboard.json`.

## Debug Menu

Press BOOTSEL if `debug_mode=True`:

- Show leaderboard
- Reset leaderboard
- Change game time
- Change the amount of places displayed on the leaderboard 

## License

[MIT License
](https://github.com/ernies-Organization/reaction-time-pico-2w?tab=MIT-1-ov-file)
