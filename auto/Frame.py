import win32gui
import win32con
import ctypes.wintypes
from pyscreeze import screenshot as _s_shot
from PIL import Image


# 获取所有可视窗口的句柄和名字
def getVisibleWindows() -> dict:
    def _myCallback(hwnd, extra):
        windows = extra
        temp = list()
        if win32gui.IsWindowVisible(hwnd):
            temp.append(hex(hwnd))
            temp.append(win32gui.GetClassName(hwnd))
            temp.append(win32gui.GetWindowText(hwnd))
            windows[hwnd] = temp
    windows = {}
    win32gui.EnumWindows(_myCallback, windows)
    return windows


# 获取某窗口的位置,win32gui.getWindowRect有误差
def getWindowRect(hwnd) -> tuple:
    try:
        f = ctypes.windll.dwmapi.DwmGetWindowAttribute
    except WindowsError:
        f = None
    if f:
        rect = ctypes.wintypes.RECT()
        DWMWA_EXTENDED_FRAME_BOUNDS = 9
        f(ctypes.wintypes.HWND(hwnd),
          ctypes.wintypes.DWORD(DWMWA_EXTENDED_FRAME_BOUNDS),
          ctypes.byref(rect),
          ctypes.sizeof(rect)
          )
        return rect.left, rect.top, rect.right, rect.bottom


# 窗口截图 return的img对象是RGB格式的
def screenshot(hwnd=None) -> object:
    if hwnd is None:
        return _s_shot()
    p = getWindowRect(hwnd)
    # reg = (x,y,width,height)
    reg = (p[0], p[1], p[2]-p[0], p[3]-p[1])
    img = _s_shot(region=reg)
    return img


# 只为获取基准图,外部不调用此函数
def _saveImage(img, filename):
    """
        _saveImage(screenshot(hwnd),'example.png')
    """
    img.save(filename)


# 设置窗口位置大小及焦点
# 并不推荐使用这个函数
def setMainWindow(hwnd, size, position=(0, 0)):
    win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST,
                          position[0], position[1],
                          size[0], size[1], win32con.SWP_SHOWWINDOW)


# 只返回找到的第一个窗口的句柄
def getWindowHwndByName(name, accurate=False) -> int:
    windows = getVisibleWindows()
    for i in windows.keys():
        if accurate:
            if name == windows[i][2]:
                return i
        else:
            if name in windows[i][2]:
                return i
    return None


# 把图片转化成image对象 RGB格式
def toImage(filename: str) -> object:
    img = Image.open(filename, mode='r')
    return img


# 用于提示
def alert(text=''):
    win32gui.MessageBox(0, text, "!", 0)


print(getVisibleWindows())
print(getWindowHwndByName('auto_game – Frame.py'))
setMainWindow('590416',size=(500,500))