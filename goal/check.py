def isCheckPosition(position):
    if not (isinstance(position, (tuple, list)) and (len(position) == 2)):
        raise ValueError("position 값은 (숫자, 숫자)")


def isCheckNumber(*args):
    if not all(map(lambda x: isinstance(x, (int, float)), args)):
        raise ValueError("숫자가 들어가야 함")


def isCheckNone(*args):
    if all(map(lambda x: x is None, args)):
        raise ValueError("None 가 들어가 있슴")


def isCheckSize(size):
    if isinstance(size, (tuple, list)) and (len(size) == 2):
        isCheckNumber(*size)
    elif isinstance(size, (int, float)):
        pass
    else:
        raise ValueError("사이즈는 숫자 또는 (숫자, 숫자)")


def isCheckColor(color):
    if isinstance(color, (tuple, list)) and (len(color) == 3):
        for c in color:
            if not (0 <= c <= 255):
                raise ValueError("RGB 색은 0~255 의 3가지 숫자")
    elif isinstance(color, str):
        pass
    else:
        raise ValueError("색이 아닌거 가틈")

