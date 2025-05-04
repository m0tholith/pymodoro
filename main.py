import os
import subprocess
import threading
import time


class _Getch:
    """Gets a single character from standard input.  Does not echo to the
    screen."""

    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self):
        return self.impl()


class _GetchUnix:
    def __init__(self):
        import sys
        import tty

    def __call__(self):
        import sys
        import termios
        import tty

        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt

        return msvcrt.getch()


getch = _Getch()

NANOSEC = 1

step = -1
t = 0


def time_from_step():
    global step
    step %= 8
    if step == 7:
        return 15 * 60
    if step % 2 == 0:
        return 25 * 60
    else:
        return 5 * 60


def inc():
    global step
    global t
    step += 1
    t = time_from_step() * NANOSEC


input_data = ""
input_thread = threading.Thread(target=None)


def get_input():
    global input_data
    c = getch()
    input_data = c


start_time = time.time()
time_since = start_time
now_time = start_time
t = 0


def print_info():
    time_s = int((t + start_time - now_time) / NANOSEC)
    secs = time_s % 60
    mins = int(time_s / 60)
    cols, rows = os.get_terminal_size(0)
    output = (
        subprocess.run(
            f"figlet -f banner3-D '{str(mins).zfill(2)}:{str(secs).zfill(2)}'",
            stdout=subprocess.PIPE,
            shell=True,
        )
        .stdout.decode()
        .splitlines()
    )
    print(f"\x1b[H\x1b[2J{"\n" * int((rows - len(output)) / 2)}")
    for i in output:
        print(f"{" " * int((cols - len(i)) / 2)}{i}\r")


print("\x1b[?25l")
paused = False
pause_time = start_time
while True:

    if not input_thread.is_alive():
        input_thread = threading.Thread(target=get_input)
        input_thread.start()
    if len(input_data) > 0:
        if input_data == "\x1b":
            exit()
        elif input_data == "s":
            inc()
            start_time = time.time()
            print_info()
        elif input_data == "p":
            t += NANOSEC * 60
            print_info()
        elif input_data == "m":
            t -= NANOSEC * 60
            print_info()
        elif input_data == " ":
            paused = not paused
            pause_time = time.time()
        input_data = ""

    diff = now_time
    now_time = time.time()
    diff = now_time - diff
    if paused:
        start_time += diff
        time_since += diff
    if now_time - t > start_time:
        inc()
        start_time = now_time
    if now_time - NANOSEC > time_since:
        print_info()
        time_since = now_time
