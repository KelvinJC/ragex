from dataclasses import dataclass


@dataclass
class Result:
    is_successful: bool
    detail: str
    error_message: str = None