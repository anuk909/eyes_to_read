from pydantic.dataclasses import dataclass


@dataclass
class User:
    username: str
    password_hash: str
