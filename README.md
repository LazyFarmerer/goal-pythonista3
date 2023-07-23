
# 설명서
달력을 만들고 날자를 클릭하여 체크 합니다

##### 1. 실행환경
pythonista3 (IOS)

##### 2. 사용법 예시
``` python
import goal
goal.option.폰방향.기본
goal.option.타이틀.색 = (255, 0, 0)
goal.option.타이틀.사이즈 = (20, 20)
goal.main("하루 40분 걷기")
```

##### -- 도움말이 보기 싫다면 이걸 복사해 넣으세요

``` python
goal.option.도움말.안봄
```


##### -- 화면을 어떻게 할지 선택합니다
``` python
goal.option.폰방향.기본
goal.option.폰방향.가로
goal.option.폰방향.세로
```

##### -- 달력의 스티커를 지정할 수 있습니다
자세한 정보들은 키보드 위 + 버튼 클릭

기본: "typw:Check"
``` python
goal.option.버튼.스티커 = "typw:Check"
```

##### -- 색과 크기를 정합니다
- 색

헥스코드 #ff0000 또는 rgb 색 (255, 0, 0) 으로 입력 가능합니다
- 크기

(20, 20) 으로 입력시 가로세로 크기
숫자만 입력시 비율 (기본 1) 만약 3일 경우 3배로 커짐

##### -- 타이틀의 색과 크기를 정합니다
``` python
goal.option.타이틀.색 = "#00ff00"
goal.option.타이틀.사이즈 = 3
```

##### -- 년월표시 색과 크기를 정합니다
``` python
goal.option.년월.색 = "#00ff00"
goal.option.년월.사이즈 = (20, 20)
```

##### -- 색과 크기 지정 가능한 옵션들
타이틀, 년월, 버튼, 요일, 일

##### -- 색만 지정 가능한 옵션들
일요일
