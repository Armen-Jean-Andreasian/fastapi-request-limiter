import os
import time
import json


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Backup:
    @staticmethod
    def save_archive(file_path: str) -> None:
        """
        :param file_path: str
        :return:
        """
        abs_file_path = os.path.abspath(os.path.join(os.curdir, file_path))
        with open(abs_file_path, 'w') as backup_file:
            json.dump(RequestsArchive().history, backup_file)
        return None

    @staticmethod
    def load_archive(file_path: str) -> dict:
        abs_file_path = os.path.abspath(os.path.join(os.curdir, file_path))
        try:
            with open(abs_file_path) as backup_file:
                return json.load(backup_file)
        except FileNotFoundError:
            return dict()


class RequestsArchive(metaclass=Singleton):
    """
    history = {'ip': {"expiration_time": expiration_time},}

    history = {'127.0.0.1':{"expiration_time": expiration_time}}

    history[ip] = {"expiration_time": False}
    """

    def __init__(self, archive_path: str | None = None):
        self.history = Backup.load_archive(archive_path := 'file.json' if not archive_path else archive_path)

    def __iter__(self):
        yield from self.history

    def add_ip(self, ip: str, seconds: float = 5.0):
        """Adds the given ip to history with N seconds cooldown, by default it's 5. """
        expiration_time = time.time() + seconds

        if type(self.history.get(ip)) is not bool:  # if the IP is permanently banned
            self.history[ip] = {"expiration_time": expiration_time}
        return self

    def extend_time(self, ip: str, seconds: int = None):
        """Extends the cooldown of the given ip for N seconds, by default it's 5. """
        seconds = 5.0 if seconds is None else float(seconds)

        if ip in self.history:
            if self.history[ip] is not False:  # if the IP is permanently banned
                self.history[ip]["expiration_time"] += seconds
        else:
            self.add_ip(ip=ip, seconds=seconds)
        return self

    def get_remaining_time(self, ip: str) -> float:
        """
        Returns the remaining cooldown for the IP
        """

        if ip in self.history:
            if remaining_time := self.history[ip]["expiration_time"]:
                return remaining_time - time.time()


class BanHammer:
    @staticmethod
    def block_it(ip: str):
        """Blocks the user permanently, switches the penalty from int to boolean """
        RequestsArchive().history[ip] = {"expiration_time": False}
        return None
