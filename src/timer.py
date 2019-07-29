import threading
from time import sleep
from timeit import default_timer

# wave_obj = simpleaudio.WaveObject.from_wave_file("sounds/sound.wav") todo implement sound
# sound = wave_obj.play()


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
        return Timer._repr(self._time)

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
            self._going = True
            self._paused = False
            self._thread = threading.Thread(target=self._run, daemon=True)
            self._thread.start()
            print("Started timer")
        else:
            print("Timer is already going")

    def pause(self):
        """Pause the timer

        If the timer not running or currently paused, this does nothing.

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
            self._text_variable.set(Timer._repr(self._time))
            try:
                self._on_finish()
            except TypeError:
                pass
            print("Stopped timer")
        else:
            print("Timer is not going; nothing to stop")

    def _run(self):
        """The loop of the timer

        This runs until self._going is set to False. It updates the text variable
        and checks if the time hit 0. If it did, it stops by calling self.stop.

        """
        # print("started _run")
        while self._going:
            s = default_timer()
            start = default_timer()
            self._tick()
            self._text_variable.set(Timer._repr(self._time))
            if self._time <= 0:
                self.stop()
            stop = default_timer()
            sleep(0.999 - (stop - start))
            f = default_timer()
            print(f - s)
        # print("finished _run")

    def _tick(self):
        self._time -= 1

    @staticmethod
    def _repr(time: int) -> str:
        """Represent time in a readable format

        Args:
            time (int): The number of seconds

        Returns:
            str: The representation of the time

        """
        minutes = time // 60
        seconds = time % 60
        return "{:02d}:{:02d}".format(minutes, seconds)


class PlayerTimer(Timer):
    """Special timer for players

    It takes a player instance as an argument.
    The only difference from the parent is that it updates the Tkinter text
    variable in a different format, it only calls self._on_finish if
    the player is suspended and it resets the time differently.

    """
    def __init__(self, text_variable, on_finish, player, countdown: int = 60):
        super().__init__(text_variable, on_finish, countdown)
        self.player = player

    def _run(self):
        # print("started _run")
        while self._going:
            s = default_timer()
            start = default_timer()
            self._tick()
            self._text_variable.set("{:02d} | {}".format(self.player.number, Timer._repr(self._time)))
            if self._time <= 0:
                self.stop()
            stop = default_timer()
            sleep(1 - (stop - start))
            f = default_timer()
            print(f - s)
        # print("finished _run")

    def stop(self):
        if self._going or self._paused:
            self._going = False
            self._paused = False
            self._text_variable.set("{:02d} | 00:00".format(self.player.number))
            print("Stopped timer")
            try:
                if self.player.suspended:
                    self._on_finish(self.player)
            except TypeError:
                pass
        else:
            print("Timer is not going; nothing to stop")
