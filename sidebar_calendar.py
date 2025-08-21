# sidebar_calendar.py
import datetime
import customtkinter as ctk

try:
    from tkcalendar import Calendar
    _HAS_TKCAL = True
except Exception:
    _HAS_TKCAL = False


def add_calendar_section(sidebar: ctk.CTkFrame):
    """
    사이드바 하단에 달력 + 실시간 시계를 붙인다.
    - sidebar: CTkFrame (grid 레이아웃 사용 중)
    - 반환: {"frame": ..., "calendar": ..., "clock": ...} 딕셔너리
    """
    # 사이드바 남는 공간을 아래로 밀어, 하단에 고정
    # (이미 다른 곳에서 rowconfigure를 했다면, 기존 값 유지됨)
    try:
        sidebar.grid_rowconfigure(90, weight=1)
    except Exception:
        pass

    cal_wrap = ctk.CTkFrame(sidebar)
    cal_wrap.grid(row=91, column=0, padx=8, pady=(8, 6), sticky="snew")
    cal_wrap.grid_rowconfigure(0, weight=0)
    cal_wrap.grid_columnconfigure(0, weight=1)

    # 다크톤 색 (tkcalendar는 표준 tkinter 색 사용)
    _BG   = "#1f1f1f"
    _HDR  = "#2a2a2a"
    _CELL = "#303030"
    _FG   = "#ffffff"

    today = datetime.date.today()

    if _HAS_TKCAL:
        cal = Calendar(
            cal_wrap,
            selectmode="none",
            year=today.year, month=today.month, day=today.day,
            showweeknumbers=False, firstweekday="monday",
            background=_BG, disabledbackground=_BG, bordercolor=_BG,
            headersbackground=_HDR, headersforeground=_FG,
            normalbackground=_CELL, normalforeground=_FG,
            weekendbackground=_CELL, weekendforeground=_FG,
            othermonthbackground=_BG, othermonthforeground="#8a8a8a",
        )
        cal.grid(row=0, column=0, padx=4, pady=(4, 0), sticky="nsew")

        # 오늘 하이라이트
        cal.calevent_create(today, "오늘", "today")
        cal.tag_config("today", background="#3b82f6", foreground="white")
    else:
        # tkcalendar 미설치 시 안내만 표시
        cal = ctk.CTkLabel(
            cal_wrap,
            text="달력 모듈(tkcalendar) 미설치\n\npip install tkcalendar",
            justify="center",
            anchor="center"
        )
        cal.grid(row=0, column=0, padx=8, pady=(8, 0), sticky="nsew")

    # 실시간 시계
    clock = ctk.CTkLabel(cal_wrap, text="", anchor="center")
    clock.grid(row=1, column=0, padx=8, pady=(6, 8), sticky="new")

    def _tick():
        # 약식: 24시간 HH:MM 형식
        now = datetime.datetime.now().strftime("%Y-%m-%d  %H:%M")
        clock.configure(text=now)
        # 부모가 파괴되지 않은 경우에만 반복
        try:
            clock.after(1000, _tick)
        except Exception:
            pass

    _tick()

    return {"frame": cal_wrap, "calendar": cal, "clock": clock}