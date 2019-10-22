from enum import IntEnum


class Color(IntEnum):
    BLACK = 0,
    RED = 1,
    YELLOW = 2,

    def to_char(self):
        mapping = {
            Color.BLACK: 'B',
            Color.RED: 'R',
            Color.YELLOW: 'Y',
        }
        return mapping[self]

    @staticmethod
    def from_char(char: str):
        mapping = {
            'B': Color.BLACK,
            'R': Color.RED,
            'Y': Color.YELLOW,
        }
        return mapping[char]

    def to_html(self):
        mapping = {
            Color.BLACK: 'black',
            Color.RED: 'red',
            Color.YELLOW: 'yellow',
        }
        return mapping[self]
