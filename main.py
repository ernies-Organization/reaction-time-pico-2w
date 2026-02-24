# ============================================================
# Pico Reaction Game
# Two-button reaction game with local leaderboard
# Debug menu via BOOTSEL
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
game_time = 10

# Change this to set where leaderboard is saved
leaderboard_file = "leaderboard.txt"


# ============================================================
# WIRING
# ============================================================
#
# BUTTON A:
#   GP14 -> push button -> GND
#
# BUTTON B:
#   GP15 -> push button -> GND
#
# LED:
#   GP16 -> 220Ω resistor -> LED (+)
#   LED (-) -> GND
#
# BOOTSEL:
#   Built into Pico (no wiring needed)
#
# ============================================================


button_a = Pin(14, Pin.IN, Pin.PULL_UP)
button_b = Pin(15, Pin.IN, Pin.PULL_UP)
led = Pin(16, Pin.OUT)


# ============================================================
# FILE HANDLING
# ============================================================

def ensure_leaderboard_file():
    """
    Ensures leaderboard file exists at configured location.
    """
    try:
        os.stat(leaderboard_file)
    except:
        with open(leaderboard_file, "w") as f:
            f.write("")


def load_entries():
    ensure_leaderboard_file()

    entries = []

    with open(leaderboard_file, "r") as f:
        for line in f:
            parts = line.strip().split(",")
            if len(parts) == 2:
                entries.append((parts[0], int(parts[1])))

    return entries


def save_entries(entries):
    with open(leaderboard_file, "w") as f:
        for name, score in entries:
            f.write(name + "," + str(score) + "\n")


def record_result(name, score):
    if score == 0:
        return

    entries = load_entries()
    entries.append((name, score))
    entries.sort(key=lambda x: x[1], reverse=True)

    save_entries(entries)


# ============================================================
# BUTTON HANDLING
# ============================================================

def wait_for_button():
    while True:
        if not button_a.value():
            time.sleep(0.2)
            return "A"

        if not button_b.value():
            time.sleep(0.2)
            return "B"


# ============================================================
# GAME LOGIC
# ============================================================

def start_game():
    print("Get ready...")
    time.sleep(2)

    score = 0
    start_time = time.time()

    while time.time() - start_time < game_time:

        led.off()
        time.sleep(random.uniform(1, 3))

        led.on()
        wait_for_button()
        score += 1

    game_over(score)


def game_over(score):
    print("\nGame Over")
    print("Score:", score)

    name = input("Enter your name: ")
    record_result(name, score)

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
            for name, score in entries:
                print(name, "-", score)

        elif choice == "2":
            save_entries([])
            print("Leaderboard reset.")

        elif choice == "3":
            print("Current time:", game_time)
            try:
                game_time = int(input("New time (seconds): "))
            except:
                print("Invalid number.")

        elif choice == "4":
            break

        print("Press any game button to continue...")
        wait_for_button()


# ============================================================
# MAIN
# ============================================================

def main():

    print("Leaderboard file location:", leaderboard_file)
    ensure_leaderboard_file()

    while True:

        if debug_mode and rp2.bootsel_button():
            debug_menu()

        print("\nPress any game button to start...")
        wait_for_button()

        start_game()


main()
