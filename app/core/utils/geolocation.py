import requests
from typing_extensions import Self


class Geolock:
    ip: str = requests.get("https://api64.ipify.org?format=json").json()["ip"]
    location_data: dict = requests.get(f"https://ipapi.co/{ip}/json/").json()

    def __new__(cls, **kwargs) -> Self:
        obj = super().__new__(cls)
        obj.ip = cls.ip
        obj.location_data = cls.location_data
        for k, v in kwargs.items():
            setattr(cls, k, v)
        return obj

    def __init__(self, *, location: str | None = None) -> None:
        if location is not None:
            self.location_data = location
