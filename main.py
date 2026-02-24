# ============================================================
# Pico Memory Game (4 buttons, 4 LEDs)
# Debug menu via BOOTSEL
# Leaderboard saves to chosen file
# ============================================================

from machine import Pin
import time
import random
import os
import rp2

# ============================================================
# CONFIGURATION
# ============================================================

debug_mode = True
game_time = 10  # seconds for testing reaction rounds

# Leaderboard file (change in config)
leaderboard_file = "leaderboard.txt"

# ============================================================
# WIRING (so others know)
# ============================================================

# Buttons (GP0-GP7 taken, using GP8-11)
# BUTTON 1 -> GP8 -> push button -> GND
# BUTTON 2 -> GP9 -> push button -> GND
# BUTTON 3 -> GP10 -> push button -> GND
# BUTTON 4 -> GP11 -> push button -> GND

# LEDs
# LED 1 -> GP12 -> 220Ω resistor -> LED (+) -> GND
# LED 2 -> GP13 -> 220Ω resistor -> LED (+) -> GND
# LED 3 -> GP14 -> 220Ω resistor -> LED (+) -> GND
# LED 4 -> GP15 -> 220Ω resistor -> LED (+) -> GND

# BOOTSEL built-in (no wiring)

# ============================================================
# PINS SETUP
# ============================================================

buttons = [
    Pin(8, Pin.IN, Pin.PULL_UP),
    Pin(9, Pin.IN, Pin.PULL_UP),
    Pin(10, Pin.IN, Pin.PULL_UP),
    Pin(11, Pin.IN, Pin.PULL_UP)
]

leds = [
    Pin(12, Pin.OUT),
    Pin(13, Pin.OUT),
    Pin(14, Pin.OUT),
    Pin(15, Pin.OUT)
]

button_labels = ["Button1","Button2","Button3","Button4"]

# ============================================================
# FILE HANDLING
# ============================================================

def ensure_leaderboard_file():
    """Create leaderboard if missing"""
    try:
        os.stat(leaderboard_file)
    except:
        with open(leaderboard_file,"w") as f:
            f.write("")

def load_entries():
    ensure_leaderboard_file()
    entries = []
    with open(leaderboard_file,"r") as f:
        for line in f:
            parts = line.strip().split(",")
            if len(parts) == 2:
                entries.append((parts[0], int(parts[1])))
    return entries

def save_entries(entries):
    with open(leaderboard_file,"w") as f:
        for name, score in entries:
            f.write(name + "," + str(score) + "\n")

def record_result(name, score):
    if score == 0:
        return
    entries = load_entries()
    entries.append((name,score))
    entries.sort(key=lambda x: x[1], reverse=True)
    save_entries(entries)

# ============================================================
# BUTTON HANDLING
# ============================================================

def wait_for_button():
    """Waits until any game button is pressed; returns 1-4"""
    while True:
        for i in range(4):
            if not buttons[i].value():
                time.sleep(0.2)  # debounce
                while not buttons[i].value():
                    pass
                return i+1  # 1-4

# ============================================================
# LED FUNCTIONS
# ============================================================

def light_led(n):
    leds[n-1].on()

def turn_off_led(n):
    leds[n-1].off()

def all_leds_on():
    for i in range(4):
        leds[i].on()

def all_leds_off():
    for i in range(4):
        leds[i].off()

# ============================================================
# GAME LOGIC
# ============================================================

def start_game():
    print("Get ready...")
    time.sleep(2)
    score = 0
    start_time = time.time()

    while time.time() - start_time < game_time:
        # pick random LED
        led_num = random.randint(1,4)
        light_led(led_num)
        wait_for_button()
        turn_off_led(led_num)
        score += 1
        time.sleep(0.2)
    game_over(score)

def game_over(score):
    print("\nGame Over!")
    print("Rounds completed:", score)
    name = input("Enter your name: ")
    record_result(name,score)
    print("Press any game button to continue...")
    wait_for_button()

# ============================================================
# DEBUG MENU
# ============================================================

def debug_menu():
    global game_time
    while True:
        print("\n--- DEBUG MENU ---")
        print("1 - Show leaderboard")
        print("2 - Reset leaderboard")
        print("3 - Change game time")
        print("4 - Exit")
        choice = input("Select option: ")
        if choice == "1":
            entries = load_entries()
            print("\nLeaderboard:")
            for n, s in entries:
                print(n,"-",s)
        elif choice == "2":
            save_entries([])
            print("Leaderboard reset.")
        elif choice == "3":
            print("Current game time:", game_time)
            try:
                game_time = int(input("New game time (seconds): "))
            except:
                print("Invalid input")
        elif choice == "4":
            break
        print("Press any game button to continue...")
        wait_for_button()

# ============================================================
# MAIN LOOP
# ============================================================

def main():
    ensure_leaderboard_file()
    print("Leaderboard file:", leaderboard_file)

    while True:
        if debug_mode and rp2.bootsel_button():
            debug_menu()
        print("\nPress any game button to start...")
        wait_for_button()
        start_game()

main()
