from scene import DEFAULT_ORIENTATION, PORTRAIT, LANDSCAPE

from .check import *


class Option:
    class __Help:
        @property
        def 안봄(self):
            Setting.help = False
            return False
    class __Orientation:
        @property
        def 기본(self):
            Setting.orientation = DEFAULT_ORIENTATION
            return DEFAULT_ORIENTATION
        @property
        def 세로(self):
            Setting.orientation = PORTRAIT
            return PORTRAIT
        @property
        def 가로(self):
            Setting.orientation = LANDSCAPE
            return LANDSCAPE
    class __Calender:
        @property
        def 스티커(self):
            return Setting.complete
        @스티커.setter
        def 스티커(self, s):
            Setting.complete = s
    class __Title:
        @property
        def 색(self):
            return Setting.title.color
        @색.setter
        def 색(self, color):
            isCheckColor(color)
            Setting.title.color = color
        @property
        def 사이즈(self):
            return Setting.title.size
        @사이즈.setter
        def 사이즈(self, size):
            isCheckSize(size)
            Setting.title.size = size
    class __Button:
        @property
        def 색(self):
            return Setting.button.color
        @색.setter
        def 색(self, color):
            isCheckColor(color)
            Setting.button.color = color
        @property
        def 사이즈(self):
            return Setting.button.size
        @사이즈.setter
        def 사이즈(self, size):
            isCheckSize(size)
            Setting.button.size = size
    class __YeayMonth:
        @property
        def 색(self):
            return Setting.yearMonth.color
        @색.setter
        def 색(self, color):
            isCheckColor(color)
            Setting.yearMonth.color = color
        @property
        def 사이즈(self):
            return Setting.yearMonth.size
        @사이즈.setter
        def 사이즈(self, size):
            isCheckSize(size)
            Setting.yearMonth.size = size
    class __Percent:
        @property
        def 색(self):
            return Setting.percent.color
        @색.setter
        def 색(self, color):
            isCheckColor(color)
            Setting.percent.color = color
        @property
        def 사이즈(self):
            return Setting.percent.size
        @사이즈.setter
        def 사이즈(self, size):
            isCheckSize(size)
            Setting.percent.size = size
    class __Week:
        @property
        def 색(self):
            return Setting.week.color
        @색.setter
        def 색(self, color):
            isCheckColor(color)
            Setting.week.color = color
        @property
        def 사이즈(self):
            return Setting.week.size
        @사이즈.setter
        def 사이즈(self, size):
            isCheckSize(size)
            Setting.week.size = size
    class __Sunday:
        @property
        def 색(self):
            return Setting.sunday.color
        @색.setter
        def 색(self, color):
            isCheckColor(color)
            Setting.sunday.color = color
    class __Days:
        @property
        def 색(self):
            return Setting.week.color
        @색.setter
        def 색(self, color):
            isCheckColor(color)
            Setting.week.color = color
        @property
        def 사이즈(self):
            return Setting.week.size
        @사이즈.setter
        def 사이즈(self, size):
            isCheckSize(size)
            Setting.week.size = size
    
    도움말 = __Help()
    폰방향 = __Orientation()
    달력 = __Calender()
    타이틀 = __Title()
    버튼 = __Button()
    년월 = __YeayMonth()
    달성도 = __Percent()
    요일 = __Week()
    일요일 = __Sunday()
    일 = __Days()

class _Object:
    size = 1
    color = "#ffffff"
class _Sunday:
    color = "#ff0000"

class Setting:
    orientation = DEFAULT_ORIENTATION
    complete = "typw:Check"
    help = True
    title = _Object()
    button = _Object()
    yearMonth = _Object()
    percent = _Object()
    week = _Object()
    sunday = _Sunday()
    days = _Object()

option = Option()
option.타이틀.사이즈 = 2
