from typing import Literal, NamedTuple

OutputFormat = Literal["pdf", "png"]


class MagnitudeRange(NamedTuple):
    bandpass: str
    max_magnitude: float
    min_magnitude: float
