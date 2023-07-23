import os, sys, json
from math import sqrt
from datetime import date
from dateutil.relativedelta import relativedelta
from typing import Union, Tuple

from scene import run, Scene
from scene import SpriteNode, LabelNode
from scene import Action as A
from scene import TIMING_ELASTIC_OUT

from .check import *
from .option import option, Setting


def emptyFunction():
    pass


class File:
    """
    파일 쓰기, 읽기 기능이 있는 클래스

    Args:
        path (str): 읽고 쓸 위치
    """

    def __init__(self, path):
        self.path = path

    def read(self, year) -> dict:
        """
        json 데이터를 읽어서 dict 형식으로 변환

        Args:
            year (int): 파일의 이름 2023.json

        Returns:
            dict: 읽어온 파일의 정보를 리턴
        """
        name = os.path.join(self.path, f"{year}.json")
        with open(name, "r", encoding="utf-8") as f:
            data = f.read()
        return json.loads(data)

    def write(self, year, data):
        """
        파일을 읽고 json 형식으로 저장

        Args:
            year (int): 파일의 이름 2023.json
            data (int): 파일에 저장할 데이터 정보

        Returns:
            dict: 읽어온 파일의 정보를 리턴
        """
        if isinstance(data, dict):
            data = json.dumps(data)

        name = os.path.join(self.path, f"{year}.json")
        with open(name, "w", encoding="utf-8") as f:
            f.write(data)

    def isfile(self, year) -> bool:
        """
        파일이 존재하는지 확인

        Args:
            year (int): 파일의 이름 2023.json

        Returns:
            bool: 파일의 존재여부
        """
        return os.path.isfile(os.path.join(self.path, f"{year}.json"))


class DataController:
    """
    파일을 저장하고 관리하는 클래스

    Args:
        date_class (Data): 날짜 정보가 들어간 Data 클래스
                          Data 클래스는 datetime 모듈의 date를 기반
    """

    def __init__(self, date_class):
        path, name = os.path.split(sys.argv[0])
        name = os.path.splitext(name)[0]
        path = os.path.join(path, name)

        self.data = []
        self.file = File(path)

        if not os.path.isdir(path):
            os.mkdir(path)

        year, month = date_class.year, date_class.month
        self.__createJsonFile(year)
        self.open(year, month)

    def commit(self, is_bool, num, year, month):
        """
        데이터를 집어넣을지, 지울지 결정한 후 저장합니다

        Args:
            is_bool (bool): 집어넣을지 지울지 결정.
            num (int): 집어넣을지 지울지 결정될 정보
        """
        if is_bool:
            self.append(num)
        else:
            self.remove(num)

        self.save(year, month)

    def append(self, num):
        """
        데이터를 집어넣고 순서대로 정렬합니다

        Args:
            num (int): 집어넣을 정보
        """
        self.data.append(num)
        self.data.sort()

    def remove(self, num):
        """
        데이터를 지웁니다

        Args:
            num (int): 지울 정보
        """
        self.data.remove(num)

    def save(self, year, month):
        """
        기존 데이터를 File 클래스로 저장

        Args:
            year (int): 파일의 이름 2023.json
            data (int): 파일에 저장할 데이터 정보
        """
        dic = self.file.read(year)
        dic[str(month)] = self.data

        self.file.write(year, dic)

    def open(self, year, month):
        """
        파일에서 데이터를 읽어옵니다

        Args:
            year (int): 파일의 이름 2023.json
            data (int): 파일에 읽어올 데이터 정보
        """
        self.__createJsonFile(year)

        self.data = self.file.read(year)[str(month)]

    def __createJsonFile(self, year):
        """
        json 파일을 만듭니다\n
        만약 파일이 있다면 실행되지 않습니다

        Args:
            year (int): 파일의 이름 2023.json
        """
        if self.file.isfile(year):
            return

        data = self.__createData()
        self.file.write(year, data)

    def __createData(self):
        """
        새로운 데이터를 만듭니다
        """
        return dict.fromkeys((str(i) for i in range(1, 12 + 1)), [])


class Screen:
    """
    Scene 클래스의 정보를 가진 클래스

    상속용
    """

    screen: Scene = None


class Action(Screen):
    """
    Node 클래스 들의 움직임 담당하는 클래스
    """

    @classmethod
    def buttonClick(cls, object):
        """
        버튼 클릭: 클릭 효과

        Args:
            object (Node)
        """
        object.run_action(
            A.sequence(
                A.scale_to(0.2, 0.2),
                A.scale_to(1, 0.2, TIMING_ELASTIC_OUT),
            ),
        )

    @classmethod
    def moveUpFadeIn(cls, object):
        """
        아래에서 위로 움직이면서 뚜렷해지고 커짐

        Args:
            object (Node)
        """
        object.run_action(
            A.sequence(
                A.group(
                    A.move_by(0, -25, 0),
                    A.scale_to(0.2, 0),
                    A.fade_to(0.5, 0),
                ),
                A.group(
                    A.move_by(0, 25, 0.2),
                    A.scale_to(1, 0.2),
                    A.fade_to(1, 0.2),
                ),
            ),
        )

    @staticmethod
    def moveUpFadeOut(object):
        """
        위로 움직이면서 흐릿해지고 작아짐

        Args:
            object (Node)
        """
        object.run_action(
            A.sequence(
                A.group(
                    A.move_by(0, 25, 0.2),
                    A.scale_to(0.2, 0.2),
                    A.fade_to(0.5, 0.2),
                ),
                A.remove(),
            ),
        )

    @classmethod
    def screenClick(cls, object, position):
        """
        화면 클릭: 물결이 퍼지는 효과

        Args:
            object (Node)
            position (숫자, 숫자): 클릭 위치
        """
        s = SpriteNode("shp:wavering", position=position, scale=0, parent=object)
        s.run_action(
            A.sequence(
                A.group(
                    A.scale_to(1),
                    A.fade_to(0),
                ),
                A.remove(),
            ),
        )
        object.run_action(A.sequence(A.wait(2), A.call(emptyFunction)))

    @classmethod
    def moveLeft(cls, object, is_start: bool):
        """
        왼쪽으로 이동

        Args:
            object (Node)
            is_start: true - 오른쪽에서 나타남,
                      false - 왼쪽으로 사라짐
        """
        x = cls.screen.size.width
        object.run_action(
            A.sequence(
                A.move_by(x, 0, 0) if is_start else emptyFunction(),
                A.move_by(-x, 0, 0.5),
                emptyFunction() if is_start else A.remove(),
            ),
        )

    @classmethod
    def moveRight(cls, object, is_start: bool):
        """
        오른쪽으로 이동

        Args:
            object (Node)
            is_start: true - 왼쪽에서 나타남,
                      false - 오른쪽으로 사라짐
        """
        x = cls.screen.size.width
        object.run_action(
            A.sequence(
                A.move_by(-x, 0, 0) if is_start else emptyFunction(),
                A.move_by(x, 0, 0.5),
                emptyFunction() if is_start else A.remove(),
            ),
        )


class ScreenRatio(Screen):
    """
    화면의 가로세로 정보를 구하는 함수를 가진 클래스
    """

    def isScreenWidth(self) -> bool:
        """
        화면의 가로세로 정보를 구함

        Returns:
            true - 세로\n
            false - 가로\n
        """
        return self.screen.size.width < self.screen.size.height


class Position(ScreenRatio):
    """
    위치정보를 담은 클래스

    Args:
        position (숫자, 숫자)
    """

    def __init__(self, position: Tuple[Union[int, float], Union[int, float]]):
        isCheckPosition(position)
        self.position = position


class Rectangle(Position):
    """
    네모난 모양을 만들 추상클래스

    rgs:
        position\n
        width (숫자): 너비\n
        height (숫자): 높이\n
    """

    def __init__(
        self,
        position,
        width: Union[int, float],
        height: Union[int, float],
    ):
        super().__init__(position)
        isCheckNumber(*position, width, height)
        self.width = width
        self.height = height
        self._screenPosition()

    def _screenPosition(self):
        """
        position 과 width, height 에 따라 x, y 값 결정

        Returns:
            (x, y) (숫자, 숫자): x, y 값
        """
        x, y = self.screen.size * self.position
        self.x = x - round(self.width / 2)
        self.y = y - round(self.height / 2)
        return (x, y)


class ButtonRectangle(Rectangle):
    """
    버튼을 만드는 클래스

    Args:
        sprite (str): 버튼 스프라이트 이미지\n
        position\n
        setting (Setting): 클래스의 크기 및 모양을 결정할 정보\n
    """

    object_list = []

    def __init__(self, sprite, position, setting):
        x, y = self.screen.size * position
        self.sprite = SpriteNode(
            sprite, position=(x, y), color=setting.color, parent=self.screen
        )
        self.sprite.size = (
            self.sprite.size * setting.size
            if isinstance(setting.size, (int, float))
            else setting.size
        )
        width, height = self.sprite.size
        super().__init__(position, width, height)

        self.object_list.append(self)

    def click(self, position) -> bool:
        """
        클릭시 실행

        Args:
            position

        Returns:
            bool: 클릭 인정되면 true
        """
        check = False
        if (
            self.x <= position[0] <= self.x + self.width
            and self.y <= position[1] <= self.y + self.height
        ):
            Action.buttonClick(self.sprite)
            check = True

        return check

    @classmethod
    def did_change_size(cls):
        """
        폰의 방향이 바뀔 시 실행
        """
        for button in cls.object_list:
            x, y = button._screenPosition()
            button.sprite.position = (x, y)


class Circle(Position):
    """
    원 모양을 만들 추상클래스

    rgs:
        position\n
        radius (숫자): 반지름\n
    """

    def __init__(self, position, radius):
        super().__init__(position)
        isCheckNumber(*position, radius)
        self.radius = radius


# ------------------- ButtonCircle 안씀 -------------------#
# class ButtonCircle(Circle):                             #
#     object_list = []                                    #
#                                                         #
#     def __init__(self, text, position, radius):         #
#         super().__init__(position, radius)              #
#         self.text = LabelNode(text, parent=self.screen) #
#         self.text.position = (self.x, self.y)           #
#                                                         #
#     def click(self):                                    #
#         pass                                            #
#                                                         #
#     def add_child(self, obj, position):                 #
#         # self.screen.add_child(self.text)              #
#         self.object_list.append(self)                   #
#                                                         #
#     @classmethod                                        #
#     def did_change_size(cls):                           #
#         for button in cls.object_list:                  #
#             x, y = button._screenPosition()             #
#             button.text.position = (x, y)               #
# _________________________________________________________#


class TextInScreen(Position):
    """
    화면에 글자를 뿌릴 클래스

    Args:
        text (str): 글자\n
        position\n
        setting (Setting): 클래스의 크기 및 모양을 결정할 정보\n
    """

    object_list = []

    def __init__(self, text, position, setting):
        super().__init__(position)
        self.setting = setting
        self.label = LabelNode(text, color=setting.color, parent=self.screen)
        self.__changeSize()
        self.__changePosition()
        self.object_list.append(self)

    def changeText(self, text, is_bool):
        """
        text 내용을 바꿈

        Args:
        text (str): 바꿀 글자\n
        is_bool: true 라면 글자 사이즈를 바꿈
        """
        self.label.text = text

        if is_bool and isinstance(self.setting.size, (int, float)):
            self.__changeSize()

    def __changePosition(self):
        """
        위치를 정렬
        """
        x, y = self.screen.size * self.position
        self.label.position = (x, y)
        return (x, y)

    def __changeSize(self):
        """
        글자크기를 지정
        """
        self.label.size = (
            self.label.size * self.setting.size
            if isinstance(self.setting.size, (int, float))
            else self.setting.size
        )

    @classmethod
    def did_change_size(cls):
        """
        폰의 방향이 바뀔 시 실행
        """
        for text in cls.object_list:
            text.__changePosition()


class TextInCalender(Position):
    """
    달력에 글자를 뿌릴 클래스

    Args:
        text (str): 글자\n
        position\n
        width_x (int): 가로 x 인덱스\n
        width_y (int): 가로 y 인덱스\n
        height_x (int): 세로 x 인덱스\n
        height_y (int): 세로 y 인덱스\n
        setting (Setting): 클래스의 크기 및 모양을 결정할 정보\n
        is_sunday (bool): true 라면 일요일로 생각하고 다른색 지정\n
    """

    def __init__(
        self, text, position, width_x, width_y, height_x, height_y, setting, is_sunday
    ):
        super().__init__(position)
        self.width_x = width_x  # 가로 x
        self.width_y = width_y  # 가로 y
        self.height_x = height_x  # 세로 x
        self.height_y = height_y  # 세로 y

        self.object = LabelNode(text, parent=self.screen)
        self.object.size = (
            self.object.size * setting.size
            if isinstance(setting.size, (int, float))
            else setting.size
        )
        color = Setting.sunday.color if is_sunday else setting.color
        self.object.color = color
        self.did_change_size()

    def did_change_size(self):
        """
        폰의 방향이 바뀔 시 실행

        가로&세로 x, y 에 맞춰서 위치 지정
        """
        if self.isScreenWidth():
            x, y = self.screen.size * (self.height_x, self.height_y)
        else:
            x, y = self.screen.size * (self.width_x, self.width_y)
        self.position = (x, y)
        self.object.position = (x, y)


class ButtonInCalender(Circle):
    """
    달력에 클릭 가능한 글자를 뿌릴 클래스

    Args:
        num (int): 일\n
        position\n
        radius\n
        width_x (int): 가로 x 인덱스\n
        width_y (int): 가로 y 인덱스\n
        height_x (int): 세로 x 인덱스\n
        height_y (int): 세로 y 인덱스\n
        is_sunday (bool): true 라면 일요일로 생각하고 다른색 지정\n
    """

    def __init__(
        self,
        num,
        position,
        radius,
        width_x,
        width_y,
        height_x,
        height_y,
        is_active,
        is_sunday,
    ):
        super().__init__(position, radius)
        self.num = num
        self.width_x = width_x  # 가로 x
        self.width_y = width_y  # 가로 y
        self.height_x = height_x  # 세로 x
        self.height_y = height_y  # 세로 y
        self.is_active = is_active
        self.is_sunday = is_sunday
        self.object = self.__createObject()
        self.did_change_size()

    def did_change_size(self):
        """
        폰의 방향이 바뀔 시 실행

        가로&세로 x, y 에 맞춰서 위치 지정
        """
        if self.isScreenWidth():
            x, y = self.screen.size * (self.height_x, self.height_y)
        else:
            x, y = self.screen.size * (self.width_x, self.width_y)
        self.position = (x, y)
        self.object.position = (x, y)

    def click(self, position) -> bool:
        """
        클릭 시 실행\n
        클릭하면 오브젝트가 변경

        Args:
            position

        Returns:
            bool: 클릭 인정시 true
        """
        isdis = self.__distance(position) <= self.radius
        # 여기서 클릭 맞으면 트루리턴
        if isdis:
            self.__changeObject()
        return isdis

    def __createObject(self):
        """
        오브젝트를 만들어냄

        Returns:
            Node
        """
        if self.is_active is True:
            object = SpriteNode(Setting.complete, parent=self.screen)
        else:
            object = LabelNode(str(self.num), parent=self.screen)

        object.size = (
            object.size * Setting.days.size
            if isinstance(Setting.days.size, (int, float))
            else Setting.days.size
        )
        object.color = Setting.sunday.color if self.is_sunday else Setting.week.color
        return object

    def __changeObject(self):
        """
        오브젝트를 변경 함
        """
        Action.moveUpFadeOut(self.object)

        self.is_active = not self.is_active

        self.object = self.__createObject()
        self.did_change_size()
        # self._screenPosition()
        Action.moveUpFadeIn(self.object)

    def __distance(self, position) -> float:
        x1, y1 = self.position
        x2, y2 = position

        dis_x = (x2 - x1) ** 2
        dis_y = (y2 - y1) ** 2
        return sqrt(dis_x + dis_y)


class Date:
    """
    datetime 모듈의 date를 기반으로 만들어진 클래스

    Args:
        date_class (date)
    """

    _weekday = ["월", "화", "수", "목", "금", "토", "일"]

    def __init__(self, date_class):
        self.date = date_class
        self.reset()

    def reset(self):
        """
        date 를 기반으로 변수 지정
        """
        self.year = self.date.year
        self.month = self.date.month
        self.day = self.date.day
        startweek = date(self.year, self.month, 1)
        self.week = startweek.weekday()
        self.last_Day = self.__lastDay(self.year, self.month)

    def nextMonth(self):
        """
        date 의 다음달
        """
        self.date += relativedelta(months=1)
        self.reset()

    def previousMonth(self):
        """
        date 의 전달
        """
        self.date -= relativedelta(months=1)
        self.reset()

    def __lastDay(self, year, month):
        """
        해당 월의 마지막날 구함

        Returns:
            int
        """
        month += 1
        if month == 13:
            month = 1
            year += 1
        d = date(year, month, 1) - relativedelta(days=1)
        return d.day


class Calender(Screen):
    """
    달력 클래스

    이 클래스 기반으로 글자와 글자위치 정함

    Args:
        date_class (Data)\n
        data_list (list): 데이터가 들어있는 리스트\n

    data_list 안에 있는 정보와 일(day) 일치하면 체크
    없다면 체크아님
    """

    height_x = (0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8)
    height_y = (0.55, 0.5, 0.45, 0.4, 0.35, 0.3, 0.25)
    width_x = (0.29, 0.36, 0.43, 0.5, 0.57, 0.64, 0.71)
    width_y = (0.6, 0.51, 0.42, 0.33, 0.24, 0.15, 0.06)

    def __init__(self, date_class, data_list):
        self.object_list = []
        self.date = date_class

        self.__createCalender(data_list)

    def __createCalender(self, data_list):
        """
        직접 글자를 그리는 함수

        Args:
            data_list (list)
        """
        y = 0
        # 월화수목금토일
        for x, week in enumerate(self.date._weekday):
            is_sunday = x == 6
            object = TextInCalender(
                text=week,
                position=(0, 0),  # 어차피 들어가서 입력됨
                width_x=self.width_x[x],
                width_y=self.width_y[y],
                height_x=self.height_x[x],
                height_y=self.height_y[y],
                setting=Setting.week,
                is_sunday=is_sunday,
            )
            self.object_list.append(object)

        y += 1
        x = self.date.week
        # 1, 2, 3, 4, 5 .....
        for day in range(1, self.date.last_Day + 1):
            is_active = day in data_list
            is_sunday = x == 6
            object = ButtonInCalender(
                num=day,
                position=(0, 0),  # 어차피 들어가서 입력됨
                radius=25,
                width_x=self.width_x[x],
                width_y=self.width_y[y],
                height_x=self.height_x[x],
                height_y=self.height_y[y],
                is_active=is_active,
                is_sunday=is_sunday,
            )
            self.object_list.append(object)
            x += 1
            if 7 <= x:
                x = 0
                y += 1

    def did_change_size(self):
        """
        폰의 방향이 바뀔 시 실행
        """
        for obj in self.object_list:
            obj.did_change_size()


class CalenderController:
    """
    Calender 클래스를 컨트롤 하기 위한 클래스

    Args:
        date_class (Data)\n
        data_list (list): 데이터가 들어있는 리스트\n
    """

    def __init__(self, date_class, data_list):
        self.calender = None

        self.create(date_class, data_list)

    def create(self, date_class, data_list):
        """
        달력 클래스를 만듦

        Args:
            date_class (Data)\n
            data_list (list): 데이터가 들어있는 리스트\n
        """
        self.calender = Calender(date_class, data_list)

    def nextMonth(self, date_class, data_list):
        """
        한달 뒤 달력 클래스를 만듦

        Args:
            date_class (Data)\n
            data_list (list): 데이터가 들어있는 리스트\n
        """
        for obj in self.calender.object_list:
            Action.moveLeft(obj.object, False)

        self.calender = Calender(date_class, data_list)

        for obj in self.calender.object_list:
            Action.moveLeft(obj.object, True)

    def previousMonth(self, date_class, data_list):
        """
        한달 전 달력 클래스를 만듦

        Args:
            date_class (Data)\n
            data_list (list): 데이터가 들어있는 리스트\n
        """
        for obj in self.calender.object_list:
            Action.moveRight(obj.object, False)

        self.calender = Calender(date_class, data_list)

        for obj in self.calender.object_list:
            Action.moveRight(obj.object, True)


class DataUI(Scene):
    """
    직접 화면에 보이는 클래스

    각종 데이터들 입력
    """

    def setup(self):
        super().setup()
        Screen.screen = self
        self.date = Date(date.today())
        self.dataController = DataController(self.date)
        data_list = self.dataController.data
        self.calenderController = CalenderController(self.date, data_list)

    def _getYearMonth(self):
        """
        년, 월 리턴

        Returns:
            int, int: 년, 월
        """
        return (self.date.year, self.date.month)


class ScreenUI(DataUI):
    """
    직접 화면에 보이는 클래스

    각종 글자와 버튼 생성
    """

    def setup(self):
        super().setup()
        TextInScreen(self.title, (0.5, 0.9), Setting.title)
        year, month = self._getYearMonth()
        self.year_month = TextInScreen(f"{year}/{month}", (0.5, 0.8), Setting.yearMonth)
        self.percent = TextInScreen(
            f"{len(self.dataController.data)}/{self.date.last_Day}({len(self.dataController.data) / self.date.last_Day:.2%})",
            (0.7, 0.7),
            Setting.percent,
        )
        self.left_btn = self.__createBtn(
            sprite="typw:Left",
            position=(0.1, 0.8),
        )
        self.right_btn = self.__createBtn(
            sprite="typw:Right",
            position=(0.9, 0.8),
        )

    def did_change_size(self):
        """
        폰의 방향이 바뀔 시 실행
        """
        super().did_change_size()
        ButtonRectangle.did_change_size()
        TextInScreen.did_change_size()
        self.calenderController.calender.did_change_size()

    def __createBtn(self, sprite: str, position):
        """
        ButtonRectangle 클래스 생성

        Args:
            sprite (str): 버튼 스프라이트 이미지\n
            position\n

        Returns:
            ButtonRectangle
        """
        btn = ButtonRectangle(sprite=sprite, position=position, setting=Setting.button)
        return btn


class TouchUI(ScreenUI):
    """
    직접 화면에 보이는 클래스

    터치시 작동할 함수 지정
    """

    def touch_began(self, touch):
        """
        화면 클릭시 실행

        Args:
            touch: touch.location 으로 클릭위치 받음
        """
        Action.screenClick(self, touch.location)
        year, month = self._getYearMonth()

        if self.left_btn.click(touch.location):
            self.dataController.save(year, month)
            self.date.previousMonth()
            year, month = self._getYearMonth()
            self.dataController.open(year, month)
            data_list = self.dataController.data
            self.calenderController.previousMonth(self.date, data_list)
            self.__textUpdate(True)
            return

        if self.right_btn.click(touch.location):
            self.dataController.save(year, month)
            self.date.nextMonth()
            year, month = self._getYearMonth()
            self.dataController.open(year, month)
            data_list = self.dataController.data
            self.calenderController.nextMonth(self.date, data_list)
            self.__textUpdate(True)
            return

        for obj in self.calenderController.calender.object_list:
            if isinstance(obj, ButtonInCalender):
                if obj.click(touch.location):
                    self.dataController.commit(obj.is_active, obj.num, year, month)
                    self.__textUpdate(False)
                    break

    def __textUpdate(self, is_bool):
        year, month = self._getYearMonth()
        self.year_month.changeText(f"{year}/{month}", is_bool)
        self.percent.changeText(
            f"{len(self.dataController.data)}/{self.date.last_Day}({len(self.dataController.data) / self.date.last_Day:.2%})",
            is_bool,
        )


class Goal(TouchUI):
    """
    직접 화면에 보이는 메인 클래스
    """

    def __init__(self, title):
        self.title = title
        super().__init__()


def main(title=None):
    if Setting.help:
        print(
            """
        간단한 도움말 입니다

        
-- 사용법 예시
ex)
import goal
goal.option.폰방향.기본
goal.option.타이틀.색 = (255, 0, 0)
goal.option.타이틀.사이즈 = (20, 20)
goal.main("하루 40분 걷기")


-- 도움말이 보기 싫다면 이걸 복사해서 넣으세요
ex)
goal.option.도움말.안봄


-- 화면을 어떻게 할지 선택합니다
ex)
goal.option.폰방향.기본
goal.option.폰방향.가로
goal.option.폰방향.세로


-- 달력의 스티커를 지정할 수 있습니다
자세한 정보들은 키보드 위 + 버튼 클릭
기본: "typw:Check"
ex)
goal.option.버튼.스티커 = "typw:Left"


-- 색과 크기를 정할 수 있습니다
- 색
 헥스코드 #ff0000 또는 rgb색 (255, 0, 0) 으로 입력 가능합니다
- 크기
 (20, 20) 으로 입력시 가로세로 크기
 숫자만 입력시 비율 (기본 1) 만약 3 일 경우 3배로 커짐


-- 타이틀의 색과 크기를 정합니다
ex)
goal.option.타이틀.색 = "#ff0000"
goal.option.타이틀.사이즈 = 3


-- 년월표시 색과 크기를 정합니다
ex)
goal.option.년월.색 = "#00ff00"
goal.option.년월.사이즈 = (20, 20)


-- 색과 크기 지정 가능한 옵션들
타이틀, 년월, 버튼, 달성도, 요일, 일


-- 색만 지정 가능한 옵션들
일요일
        """
        )
    if title is None:
        title = os.path.splitext(os.path.basename(sys.argv[0]))[0]

    run(Goal(title), Setting.orientation)


if __name__ == "__main__":
    main("테스트")

