import threading
from time import sleep
from timeit import default_timer


class Timer:

    def __init__(self, text_variable, on_finish, countdown: int = 60):
        self._text_variable = text_variable
        self._on_finish = on_finish
        self._countdown = countdown
        self._time = self._countdown
        self._thread = threading.Thread
        self._going = False
        self._paused = False

    def get_time(self) -> str:
        return Timer._repr(self._time)

    def get_raw_time(self) -> int:
        return self._time

    def get_going(self) -> bool:
        return self._going

    def get_paused(self) -> bool:
        return self._paused

    def start(self):
        if not self._going:
            self._going = True
            self._paused = False
            self._thread = threading.Thread(target=self._run, daemon=True)
            self._thread.start()
            print("Started timer")
        else:
            print("Timer is already going")

    def pause(self):
        if self._going:
            self._going = False
            self._paused = True
            print("Paused timer")
        else:
            print("Timer is not going; nothing to pause")

    def stop(self):
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
        print("started _run")
        while self._going:
            s = default_timer()
            self._tick()
            self._text_variable.set(Timer._repr(self._time))
            if self._time <= 0:
                self.stop()
            sleep(0.999)
            f = default_timer()
            print(f - s)
        print("finished _run")

    def _tick(self):
        self._time -= 1

    @staticmethod
    def _repr(time: int) -> str:
        minutes = time // 60
        seconds = time % 60
        return "{:02d}:{:02d}".format(minutes, seconds)


class PlayerTimer(Timer):

    def __init__(self, text_variable, on_finish, player, countdown: int = 60):
        super().__init__(text_variable, on_finish, countdown)
        self.player = player

    def _run(self):
        print("started _run")
        while self._going:
            s = default_timer()
            self._tick()
            self._text_variable.set("{} | {}".format(self.player.number, Timer._repr(self._time)))
            if self._time <= 0:
                self.stop()
            sleep(0.999)
            f = default_timer()
            print(f - s)
        print("finished _run")

    def stop(self):
        if self._going or self._paused:
            self._going = False
            self._paused = False
            self._time = self._countdown
            self._text_variable.set("{} | {}".format(self.player.number, Timer._repr(self._time)))
            print("Stopped timer")
            try:
                if self.player.suspended:
                    self._on_finish(self.player)
                    print(111)
            except TypeError:
                pass
        else:
            print("Timer is not going; nothing to stop")
