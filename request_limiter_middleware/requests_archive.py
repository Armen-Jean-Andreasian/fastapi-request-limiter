import os
import time
from fastapi import HTTPException
import json

class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class RequestsArchive(metaclass=Singleton):
    """
    history = {'ip': {"expiration_time": expiration_time},}

    history = {'127.0.0.1':{"expiration_time": expiration_time}}

    history[ip] = {"expiration_time": False}
    """
    def __init__(self):
        self.history = dict()

    def add_ip(self, ip: str, seconds: int = 5):
        """Adds the given ip to history with N seconds cooldown, by default it's 5. """
        expiration_time = time.time() + seconds

        if type(self.history[ip]) is not bool:  # if the IP is permanently banned
            self.history[ip] = {"expiration_time": expiration_time}

        return self

    def extend_time(self, ip: str, seconds: int = None):
        """Extends the cooldown of the given ip for N seconds, by default it's 5. """
        seconds = 5 if seconds is None else seconds

        if ip in self.history:
            if type(self.history[ip]) is not bool:  # if the IP is permanently banned
                self.history[ip]["expiration_time"] += seconds
        else:
            self.add_ip(ip=ip, seconds=seconds)
        return self

    def get_remaining_time(self, ip: str) -> int:
        """Returns the remaining cooldown for the ip in seconds"""
        if ip in self.history:
            if type(self.history[ip]["expiration_time"]) is bool:  # if the IP is permanently banned
                raise HTTPException(status_code=400, detail="Goodbye")

            if type(self.history[ip]["expiration_time"]) is float:
                remaining_time = self.history[ip]["expiration_time"] - time.time()
                return max(0, round(remaining_time))
        else:
            return 0
class BanHammer:
    @staticmethod
    def block_it(ip: str):
        """Blocks the user permanently, switches the penalty from int to boolean """
        RequestsArchive().history[ip] = {"expiration_time": False}
        return None


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
        with open(abs_file_path) as backup_file:
            archive = json.load(backup_file)
        return archive
