import threading
from os.path import join
from time import sleep
from timeit import default_timer

import simpleaudio


class Timer:
    """Class used to create timer objects for the round itself and for players"""

    def __init__(self, text_variable, on_finish, countdown: int = 60):
        self._text_variable = text_variable
        self._on_finish = on_finish
        self._countdown = countdown
        self._time = self._countdown
        self._thread = threading.Thread
        self._going = False
        self._paused = False

    def get_time(self) -> str:
        """Get the time in a readable format

        Returns:
            str: The current time

        """
        return Timer.repr(self._time)

    def get_raw_time(self) -> int:
        """Get the raw time

        Returns:
            int: The current time in seconds

        """
        return self._time

    def get_going(self) -> bool:
        """Check if the timer is currently running

        Returns:
            bool: True if the timer is running, False otherwise

        """
        return self._going

    def get_paused(self) -> bool:
        """Check if the timer is currently paused

        Returns:
            bool: True if the timer is paused, False otherwise

        """
        return self._paused

    def start(self):
        """Start the timer

        If the timer is already running, this method does nothing.
        This creates a new thread and starts it immediately with self._run.

        """
        if not self._going:
            if self._thread == threading.Thread or not self._thread.is_alive():
                self._going = True
                self._paused = False
                self._thread = threading.Thread(target=self._run, daemon=True)
                self._thread.start()
                print("Started timer")
            else:
                print("Timer's thread is not done yet")
        else:
            print("Timer is already going")

    def pause(self):
        """Pause the timer

        If the timer is not running or currently paused, this does nothing.

        """
        if self._going and not self._paused:
            self._going = False
            self._paused = True
            print("Paused timer")
        else:
            print("Timer is not going; nothing to pause")

    def stop(self):
        """Stop the timer

        If the timer is already stopped, this does nothing.
        It resets the time, the Tkinter text variable and executes the
        self._on_finish optional function.

        """
        if self._going or self._paused:
            self._going = False
            self._paused = False
            self._time = self._countdown
            self._text_variable.set(Timer.repr(self._time))
            try:
                self._on_finish()
            except TypeError:
                pass
            print("Stopped timer")
        else:
            print("Timer is not going; nothing to stop")

    @staticmethod
    def repr(time: int) -> str:
        """Represent time in a readable format

        Args:
            time (int): The number of seconds

        Returns:
            str: The representation of the time

        """
        minutes = time // 60
        seconds = time % 60
        return "{:02d}:{:02d}".format(minutes, seconds)

    def _run(self):
        """The loop of the timer

        This runs until self._going is set to False. It updates the text variable
        and checks if the time hit 0. If it did, it stops by calling self.stop.

        """
        start = 0
        stop = 0
        while self._going:
            # s = default_timer()

            sleep(0.999 - (stop - start))
            start = default_timer()
            if self._going:
                self._tick()
            self._text_variable.set(Timer.repr(self._time))
            if self._time <= 0:
                self.stop()
            stop = default_timer()

            # f = default_timer()
            # print(f - s)

    def _tick(self):
        self._time -= 1


class PlayerTimer(Timer):
    """Special timer for players

    It takes a player instance as an argument.
    The only difference from the parent is that it updates the Tkinter text
    variable in a different format, it only calls self._on_finish if
    the player is suspended and it resets the time differently.

    """
    def __init__(self, text_variable, on_finish, player, countdown: int = 60):
        super().__init__(text_variable, on_finish, countdown)
        self._player = player

    def _run(self):
        start = 0
        stop = 0
        while self._going:
            # s = default_timer()

            sleep(0.999 - (stop - start))
            start = default_timer()
            if self._going:
                self._tick()
            self._text_variable.set("{:02d} | {}".format(self._player.number, Timer.repr(self._time)))
            if self._time <= 0:
                self.stop()
            stop = default_timer()

            # f = default_timer()
            # print(f - s)

    def stop(self):
        if self._going or self._paused:
            self._going = False
            self._paused = False
            self._time = self._countdown
            self._text_variable.set("{:02d} | {}".format(self._player.number, Timer.repr(self._time)))
            print("Stopped timer")
            try:
                if self._player.suspended:
                    self._on_finish(self._player)
            except TypeError:
                pass
        else:
            print("Timer is not going; nothing to stop")


class SelfFixTimer(Timer):

    def __init__(self, text_variable, on_finish, countdown: int = 60):
        super().__init__(text_variable, on_finish, countdown)
        self._measuring = False
        self._measure_start = 0.0
        self._measure_stop = 0.0
        self._seconds_passed = 0
        self._accumulator = 0.0

    def pause(self):
        if self._going and not self._paused:
            self._going = False
            self._paused = True
            self._seconds_passed = 0
            self._measuring = False
            print("Paused timer")
        else:
            print("Timer is not going; nothing to pause")

    def stop(self):
        if self._going or self._paused:
            self._going = False
            self._paused = False
            self._time = self._countdown
            self._seconds_passed = 0
            self._accumulator = 0.0
            self._text_variable.set(Timer.repr(self._time))
            try:
                self._on_finish()
            except TypeError:
                pass
            print("Stopped timer")
        else:
            print("Timer is not going; nothing to stop")

    def _run(self):
        start = 0
        stop = 0
        self._start_measure()
        while self._going:
            # s = default_timer()

            sleep(0.999 - (stop - start))
            start = default_timer()
            if self._going:
                self._tick()
            self._text_variable.set(Timer.repr(self._time))
            if self._time <= 0:
                self.stop()

            if self._going and self._time % 120 == 0:
                print("Time: " + str(self._time))
                self._fix_time()
                self._start_measure()
            stop = default_timer()

            # f = default_timer()
            # print(f - s)

    def _start_measure(self):
        if not self._measuring:
            self._measuring = True
            self._measure_start = default_timer()

    def _fix_time(self):
        if self._measuring:
            self._measure_stop = default_timer()
            seconds_actually_passed: float = self._measure_stop - self._measure_start  # How many seconds actually passed in
            print("Actually passed: " + str(seconds_actually_passed))                  # those presumably 2 minutes
            print("Ticks passed: " + str(self._seconds_passed))
            delta: float = seconds_actually_passed - self._seconds_passed  # The difference should be 1 - 2 seconds
            print("Delta: " + str(delta))

            self._accumulator += delta
            print("Accumulator: " + str(self._accumulator))

            if self._accumulator >= 1:
                sec_forward = int(self._accumulator)
                self._time -= sec_forward
                self._accumulator -= sec_forward
                print("Forward {} second(s)".format(sec_forward))

            self._measuring = False
            self._seconds_passed = 0

    def _tick(self):
        self._time -= 1
        self._seconds_passed += 1


class TimeOutTimer(Timer):

    _sound_wave = simpleaudio.WaveObject.from_wave_file(join("data", "sounds", "sound.wav"))

    def __init__(self, text_variable, on_finish, countdown: int = 60):
        super().__init__(text_variable, on_finish, countdown)

    def start(self):
        if not self._going:
            if self._thread == threading.Thread or not self._thread.is_alive():
                self._going = True
                self._paused = False
                self._thread = threading.Thread(target=self._run, daemon=True)
                self._thread.start()
                self._sound_wave.play()
                print("Started timer")
            else:
                print("Timer's thread is not done yet")
        else:
            print("Timer is already going")

    def _run(self):
        start = 0
        stop = 0
        while self._going:
            # s = default_timer()

            sleep(0.999 - (stop - start))
            start = default_timer()
            if self._going:
                self._tick()
            self._text_variable.set(Timer.repr(self._time))
            if self._time == 10:
                self._sound_wave.play()
            elif self._time <= 0:
                self.stop()
                self._sound_wave.play()
            stop = default_timer()

            # f = default_timer()
            # print(f - s)
