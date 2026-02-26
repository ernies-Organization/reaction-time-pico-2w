# ============================================================
# Memory Game for Raspberry Pi Pico 2w
# ============================================================

from machine import Pin
import time
import random
import ujson as json
import rp2


# ============================================================
# Configuration (only edit here)
# ============================================================

debug_mode = False          # Enables debug printing + BOOTSEL menu
led_on_time = 300          # LED ON duration in milliseconds
led_off_time = 150         # LED OFF duration between flashes
LEADERBOARD_PATH = "memery_game_leaderboard.json" # File name for the leaderboard (has to have ".json" at the end)
leaderboard_lenth = 10 # lenth of leader board displayed 

# ============================================================
# Hardware Setup
# ============================================================

# LED output pins (adjust if your wiring changes)
led_pins = [
    Pin(0, Pin.OUT),
    Pin(2, Pin.OUT),
    Pin(4, Pin.OUT),
    Pin(6, Pin.OUT)
]

# Button input pins (PULL_DOWN wiring)
button_pins = [
    Pin(7, Pin.IN, Pin.PULL_DOWN),
    Pin(5, Pin.IN, Pin.PULL_DOWN),
    Pin(3, Pin.IN, Pin.PULL_DOWN),
    Pin(1, Pin.IN, Pin.PULL_DOWN)
]

button_labels = ["K4", "K3", "K2", "K1"]


# ============================================================
# LED Utility Functions
# ============================================================

def light_led(index):
    """Turn on LED (1–4)."""
    led_pins[index - 1].on()


def turn_off_led(index):
    """Turn off LED (1–4)."""
    led_pins[index - 1].off()


def all_leds_on():
    """Turn on all LEDs."""
    for i in range(1, 5):
        light_led(i)


def all_leds_off():
    """Turn off all LEDs."""
    for i in range(1, 5):
        turn_off_led(i)


# ============================================================
# Leaderboard Persistence
# ============================================================

def _ensure_file():
    """Create leaderboard file if it does not exist."""
    try:
        with open(LEADERBOARD_PATH, "r"):
            pass
    except:
        with open(LEADERBOARD_PATH, "w") as f:
            f.write("[]")


def _load():
    """Load leaderboard entries from file."""
    _ensure_file()
    try:
        with open(LEADERBOARD_PATH, "r") as f:
            return json.load(f)
    except:
        return []


def _save(entries):
    """Save leaderboard entries to file."""
    with open(LEADERBOARD_PATH, "w") as f:
        json.dump(entries, f)

def record_result(name, rounds):
    """
    Store or update player score.
    Only highest score per player is kept.
    Zero-round games are ignored.
    If multiple players have the same score,
    the order is based on when they achieved it.
    """
    if rounds == 0:
        return

    entries = _load()
    found = False

    for entry in entries:
        if entry["player_name"] == name:
            # Only update if new score is higher
            if rounds > entry["rounds"]:
                entry["rounds"] = rounds
            found = True
            break

    if not found:
        entries.append({
            "player_name": name,
            "rounds": rounds
        })

    # Stable sort: highest score first.
    # Equal scores keep original insertion order.
    entries.sort(key=lambda x: x["rounds"], reverse=True)

    _save(entries)
    
def print_leaderboard():
    """Print top scores to serial console."""
    entries = _load()
    entries.sort(key=lambda x: x["rounds"], reverse=True)

    print("\n=== Leaderboard ===")
    for i, entry in enumerate(entries[:leaderboard_lenth], 1):
        print(f"{i}) {entry['player_name']} - {entry['rounds']} rounds")


# ============================================================
# Debug Menu (Accessible via BOOTSEL if debug_mode=True)
# ============================================================

def debug_menu():
    global led_on_time, led_off_time, leaderboard_lenth

    print("""\n*** DEBUG MENU ***
1 - Change LED timing
2 - Reset leaderboard
3 - Change the lenth of the leaderboard displayed
Enter - Exit""")

    while True:
        choice = input("Choice: ").strip()

        if choice == "1":
            try:
                new_on = int(input(f"LED ON time ({led_on_time} ms): "))
                new_off = int(input(f"LED OFF time ({led_off_time} ms): "))
                led_on_time = new_on
                led_off_time = new_off
                print("Timing updated.")
            except:
                print("Invalid input.")

        elif choice == "2":
            _save([])
            print("Leaderboard reset.")
        
        elif choice == "3":
            new_leaderboard_lenth = int(input(f"lenth of leaderboard displayed ({leaderboard_lenth}):"))
            leaderboard_lenth = new_leaderboard_lenth
        
        else:
            break

    pause_animation()

    # Resume indicator
    all_leds_on()
    time.sleep_ms(200)
    all_leds_off()
    print("Resuming game...\n")


# ============================================================
# Pause Animation
# ============================================================

def pause_animation():
    """
    LED sweep animation while paused.
    Exits when any game button is pressed.
    """
    print("\nPress any button to continue...")

    while True:
        for led in range(1, 5):
            light_led(led)
            time.sleep_ms(80)
            turn_off_led(led)

            # Exit on button press
            for i in range(4):
                if button_pins[i].value() == 0:
                    time.sleep_ms(20)
                    while button_pins[i].value() == 0:
                        pass
                    return


# ============================================================
# Button Handling
# ============================================================

def wait_for_button():
    """
    Wait for any game button press.
    BOOTSEL opens debug menu when debug_mode is enabled.
    """
    while True:

        # Debug menu trigger
        if debug_mode and rp2.bootsel_button():
            all_leds_off()
            debug_menu()

        # Game button detection
        for i in range(4):
            if button_pins[i].value() == 0:
                time.sleep_ms(20)  # debounce
                while button_pins[i].value() == 0:
                    pass

                if debug_mode:
                    print("Pressed:", button_labels[i])

                return i + 1


# ============================================================
# Game Logic
# ============================================================

memory_sequence = []


def show_sequence():
    """Display the current sequence to the player."""
    for value in memory_sequence:
        light_led(value)
        time.sleep_ms(led_on_time)
        turn_off_led(value)
        time.sleep_ms(led_off_time)


def game_over():
    """Handle end-of-game logic and restart."""
    rounds_completed = len(memory_sequence) - 1

    print(f"\nGame Over! You completed {rounds_completed} rounds.")
    record_result(player_name, rounds_completed)
    print_leaderboard()

    print("\nPress any button to restart")
    all_leds_on()
    wait_for_button()
    all_leds_off()

    memory_sequence.clear()
    start_game()


def start_game():
    """Main game loop."""
    while True:
        memory_sequence.append(random.randint(1, 4))

        show_sequence()

        if debug_mode:
            print("Sequence:", memory_sequence)
        
        print(f"Curent round: {len(memory_sequence)}")
        
        for index in range(len(memory_sequence)):
            player_input = wait_for_button()

            light_led(player_input)
            time.sleep_ms(led_on_time)
            turn_off_led(player_input)

            if player_input != memory_sequence[index]:
                game_over()


# ============================================================
# Program Entry Point
# ============================================================

# Startup indicator
all_leds_on()
time.sleep_ms(500)
all_leds_off()

player_name = input("Enter your name: ")

print("\nPress any button to continue...")
all_leds_on()
wait_for_button()
all_leds_off()

start_game()
