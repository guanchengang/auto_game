from Frame import alert
from Mouse import position
from time import sleep
import sys
import Frame
"""
   这个文件可以用于找一些固定点位
   以目标窗口的原点（左上角）为基础 
"""
alert("按下确定之后,把鼠标移动到对应位置,等几秒钟(需要在模拟器界面)")
sleep(5)
hwnd = Frame.getWindowHwndByName('MuMu模拟器')
if hwnd is None:
    print("没有目标窗口")
    sys.exit(0)
pos = Frame.getWindowRect(hwnd)
left_top = (pos[0], pos[1])
now = position()
result = (now[0]-left_top[0],
          now[1]-left_top[1])
print("目标位置为:", result)

