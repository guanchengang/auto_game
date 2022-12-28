import win32api
import win32con

import time

import pytweening  # 补间函数

'''
此模块的实现借鉴了pyautogui
'''


# 用于强制退出移动
def _checkSafePosition():
    if position() == (0, 0):
        raise Exception("safe position!")


# 得到当前鼠标位置
def position() -> tuple:
    return win32api.GetCursorPos()


# 实现鼠标左键单击
def leftClick(pos=None, duration=0.0):
    if pos:
        moveTo(pos=pos, duration=duration)
    mouseDown("LEFT")
    time.sleep(0.1)
    mouseUp("LEFT")


# 实现鼠标移动
def moveTo(pos, duration=0.0):
    start_position = position()
    width = abs(start_position[0]-pos[0])
    height = abs(start_position[1]-pos[1])
    num_move = int(max(width, height))
    sleep_time = duration/num_move

    # 小于最短休眠时间
    if sleep_time < 0.05:
        num_move = int(duration/0.05)
        sleep_time = 0.05

    # 持续时间太短就直接瞬移过去
    if duration < 0.1:
        win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, 0, 0, 0)
        return
    start_x, start_y = position()
    x, y = pos
    # 创建补间
    steps = [pytweening.getPointOnLine(start_x, start_y, x, y, pytweening.linear(i/num_move)) for i in range(num_move)]
    steps.append(pos)
    for i in steps:
        now_x, now_y = i
        time.sleep(sleep_time)
        _checkSafePosition()
        win32api.SetCursorPos((int(now_x), int(now_y)))


# 实现拖动操作
def dragTo(pos, duration):
    mouseDown("LEFT")
    moveTo(pos=pos, duration=duration)
    mouseUp("LEFT")


# 鼠标按下事件
def mouseDown(button):
    if button not in ("LEFT", "RIGHT"):
        raise Exception("button err!")
    event = win32con.MOUSEEVENTF_LEFTDOWN if button == "LEFT" else win32con.MOUSEEVENTF_RIGHTDOWN
    win32api.mouse_event(event, 0, 0, 0)


# 鼠标释放事件
def mouseUp(button):
    if button not in ("LEFT", "RIGHT"):
        raise Exception("button err!")
    event = win32con.MOUSEEVENTF_LEFTUP if button == "LEFT" else win32con.MOUSEEVENTF_RIGHTUP
    win32api.mouse_event(event, 0, 0, 0)
