import pygame
import tkinter as tk
import readChart
import rpe_easing
import errorOut
import threading

# 初始化 pygame
pygame.init()

# 初始化 pygame 音频模块
pygame.mixer.init()

# 加载 bgm
pygame.mixer.music.load(f"resources/chart/{readChart.chart}.mp3")

# 时间转换函数
def baseToSecond(time):
    if time[1] == 0:
        return (60 / readChart.bpm) * time[0]
    else:
        return (60 / readChart.bpm) * (time[0] + (time[1] / time[2]))

# 窗口类
class PlayerWindow:
    def __init__(self, windowNumber):
        self.root = tk.Tk()
        self.root.title("PlayerWindow")
        self.windowNumber = windowNumber
        self.root.overrideredirect(True)
        self.x = 0
        self.y = 0
        self.xEvents = readChart.chartFiles['judgeLineList'][self.windowNumber]["eventLayers"][0]["moveXEvents"]
        self.yEvents = readChart.chartFiles['judgeLineList'][self.windowNumber]["eventLayers"][0]["moveYEvents"]
        self.xEventIndex = 0
        self.yEventIndex = 0
        self.a = 1
        self.aEvents = readChart.chartFiles['judgeLineList'][self.windowNumber]["eventLayers"][0]["alphaEvents"]
        self.aEventIndex = 0
        self.w = 400
        self.h = 200        
        self.root.geometry("400x200+100+100")
        self.text = ""
        if "textEvents" in readChart.chartFiles['judgeLineList'][self.windowNumber]["extended"]:
            self.textEvents = readChart.chartFiles['judgeLineList'][self.windowNumber]["extended"]["textEvents"]
        else:
            self.textEvents = []
        self.textIndex = 0
        self.label = tk.Label(self.root, text=f"{self.text}")
        self.label.pack(pady=20)
        if "scaleXEvents" in readChart.chartFiles['judgeLineList'][self.windowNumber]["extended"]:
            self.scaleXEvents = readChart.chartFiles['judgeLineList'][self.windowNumber]["extended"]["scaleXEvents"]
        else:
            self.scaleXEvents = []
        if "scaleYEvents" in readChart.chartFiles['judgeLineList'][self.windowNumber]["extended"]:
            self.scaleYEvents = readChart.chartFiles['judgeLineList'][self.windowNumber]["extended"]["scaleYEvents"]
        else:
            self.scaleYEvents = []
        self.sXIndex = 0
        self.sYIndex = 0
        if "colorEvents" in readChart.chartFiles['judgeLineList'][self.windowNumber]["extended"]:
            self.colorEvents = readChart.chartFiles['judgeLineList'][self.windowNumber]["extended"]["colorEvents"]
        else:
            self.colorEvents = []
        self.colorIndex = 0
        self.color = "#FFFFFF"
        
    def moveWindowX(self):
        time = pygame.mixer.music.get_pos() / 1000
        if self.xEventIndex < len(self.xEvents):
            if time > baseToSecond(self.xEvents[self.xEventIndex]["endTime"]):
                x = self.xEvents[self.xEventIndex]["end"]
                self.x = (x / 1350) * self.root.winfo_screenwidth() + self.root.winfo_screenwidth() / 2
                self.xEventIndex += 1
            elif time > baseToSecond(self.xEvents[self.xEventIndex]["startTime"]):
                easingType = self.xEvents[self.xEventIndex]["easingType"]
                if self.xEvents[self.xEventIndex]["end"] != self.xEvents[self.xEventIndex]["start"]:
                    result = rpe_easing.ease_funcs[easingType - 1]((time-baseToSecond(self.xEvents[self.xEventIndex]["startTime"])) / (baseToSecond(self.xEvents[self.xEventIndex]["endTime"]) - baseToSecond(self.xEvents[self.xEventIndex]["startTime"])))
                    x = self.xEvents[self.xEventIndex]["start"] + (self.xEvents[self.xEventIndex]["end"] - self.xEvents[self.xEventIndex]["start"]) * result
                    self.x = (x / 1350) * self.root.winfo_screenwidth() + self.root.winfo_screenwidth() / 2
                else:
                    x = self.xEvents[self.xEventIndex]["start"]
                    self.x = (x / 1350) * self.root.winfo_screenwidth() + self.root.winfo_screenwidth() / 2
                    
    def moveWindowY(self):
        time = pygame.mixer.music.get_pos() / 1000
        if self.yEventIndex < len(self.yEvents):
            if time > baseToSecond(self.yEvents[self.yEventIndex]["endTime"]):
                y = self.yEvents[self.yEventIndex]["end"]
                self.y = (1 - y / 900) * self.root.winfo_screenheight() - self.root.winfo_screenheight() / 2
                self.yEventIndex += 1
            elif time > baseToSecond(self.yEvents[self.yEventIndex]["startTime"]):
                easingType = self.yEvents[self.yEventIndex]["easingType"]
                if self.yEvents[self.yEventIndex]["end"] != self.yEvents[self.yEventIndex]["start"]:
                    result = rpe_easing.ease_funcs[easingType - 1]((time-baseToSecond(self.yEvents[self.yEventIndex]["startTime"])) / (baseToSecond(self.yEvents[self.yEventIndex]["endTime"]) - baseToSecond(self.yEvents[self.yEventIndex]["startTime"])))
                    y = self.yEvents[self.yEventIndex]["start"] + (self.yEvents[self.yEventIndex]["end"] - self.yEvents[self.yEventIndex]["start"]) * result
                    self.y = (1 - y / 900) * self.root.winfo_screenheight() - self.root.winfo_screenheight() / 2
                else:
                    y = self.yEvents[self.yEventIndex]["start"]
                    self.y = (1 - y / 900) * self.root.winfo_screenheight() - self.root.winfo_screenheight() / 2
        
    def windowAlpha(self):
        time = pygame.mixer.music.get_pos() / 1000
        if self.aEventIndex < len(self.aEvents):
            if time > baseToSecond(self.aEvents[self.aEventIndex]["endTime"]):
                a = self.aEvents[self.aEventIndex]["end"]
                self.a = 1 - (255 - a) / 255
                self.aEventIndex += 1
            elif time > baseToSecond(self.aEvents[self.aEventIndex]["startTime"]):
                easingType = self.aEvents[self.aEventIndex]["easingType"]
                if self.aEvents[self.aEventIndex]["end"] != self.aEvents[self.aEventIndex]["start"]:
                    result = rpe_easing.ease_funcs[easingType - 1]((time-baseToSecond(self.aEvents[self.aEventIndex]["startTime"])) / (baseToSecond(self.aEvents[self.aEventIndex]["endTime"]) - baseToSecond(self.aEvents[self.aEventIndex]["startTime"])))
                    a = self.aEvents[self.aEventIndex]["start"] + (self.aEvents[self.aEventIndex]["end"] - self.aEvents[self.aEventIndex]["start"]) * result
                    self.a = 1 - (255 - a) / 255
                else:
                    a = self.aEvents[self.aEventIndex]["start"]
                    self.a = 1 - (255 - a) / 255
    def scaleXChange(self,x):
        result = (x * 4000 ) * (self.root.winfo_screenwidth() / 1350)
        if result > self.root.winfo_screenwidth():
            result = self.root.winfo_screenwidth()
        return result
    def scaleXWindow(self):
        time = pygame.mixer.music.get_pos() / 1000
        if self.sXIndex < len(self.scaleXEvents):
            if time > baseToSecond(self.scaleXEvents[self.sXIndex]["endTime"]):
                scaleX = self.scaleXEvents[self.sXIndex]["end"]
                self.w = self.scaleXChange(scaleX)
                self.sXIndex += 1
            elif time > baseToSecond(self.scaleXEvents[self.sXIndex]["startTime"]):
                easingType = self.scaleXEvents[self.sXIndex]["easingType"]
                if self.scaleXEvents[self.sXIndex]["end"] != self.scaleXEvents[self.sXIndex]["start"]:
                    result = rpe_easing.ease_funcs[easingType - 1]((time-baseToSecond(self.scaleXEvents[self.sXIndex]["startTime"])) / (baseToSecond(self.scaleXEvents[self.sXIndex]["endTime"]) - baseToSecond(self.scaleXEvents[self.sXIndex]["startTime"])))
                    scaleX = self.scaleXEvents[self.sXIndex]["start"] + (self.scaleXEvents[self.sXIndex]["end"] - self.scaleXEvents[self.sXIndex]["start"]) * result
                    self.w = self.scaleXChange(scaleX)
                else:
                    scaleX = self.scaleXEvents[self.sXIndex]["start"]
                    self.w = self.scaleXChange(scaleX)
    def scaleYChange(self,y):
        result = (y * 5 ) * (self.root.winfo_screenheight() / 900)
        if result > self.root.winfo_screenheight():
            result = self.root.winfo_screenheight()
        return result
    def scaleYWindow(self):
        time = pygame.mixer.music.get_pos() / 1000
        if self.sYIndex < len(self.scaleYEvents):
            if time > baseToSecond(self.scaleYEvents[self.sYIndex]["endTime"]):
                scaleY = self.scaleYEvents[self.sYIndex]["end"]
                self.h = self.scaleYChange(scaleY)
                self.sYIndex += 1
            elif time > baseToSecond(self.scaleYEvents[self.sYIndex]["startTime"]):
                easingType = self.scaleYEvents[self.sYIndex]["easingType"]
                if self.scaleYEvents[self.sYIndex]["end"] != self.scaleYEvents[self.sYIndex]["start"]:
                    result = rpe_easing.ease_funcs[easingType - 1]((time-baseToSecond(self.scaleYEvents[self.sYIndex]["startTime"])) / (baseToSecond(self.scaleYEvents[self.sYIndex]["endTime"]) - baseToSecond(self.scaleYEvents[self.sYIndex]["startTime"])))
                    scaleY = self.scaleYEvents[self.sYIndex]["start"] + (self.scaleYEvents[self.sYIndex]["end"] - self.scaleYEvents[self.sYIndex]["start"]) * result
                    self.h = self.scaleYChange(scaleY)
                else:
                    scaleY = self.scaleYEvents[self.sYIndex]["start"]
                    self.h = self.scaleYChange(scaleY)
    def getText(self):
        time = pygame.mixer.music.get_pos() / 1000
        if self.textIndex < len(self.textEvents):
            if time > baseToSecond(self.textEvents[self.textIndex]["endTime"]):
                self.text = self.textEvents[self.textIndex]["end"]
                self.textIndex += 1
            elif time > baseToSecond(self.textEvents[self.textIndex]["startTime"]):
                self.text = self.textEvents[self.textIndex]["start"]
    def getColor(self):
        time = pygame.mixer.music.get_pos() / 1000
        if self.colorIndex < len(self.colorEvents):
            if time > baseToSecond(self.colorEvents[self.colorIndex]["endTime"]):
                color = self.colorEvents[self.colorIndex]["end"]
                self.color = f"#{color[0]:02X}{color[1]:02X}{color[2]:02X}"
                self.colorIndex += 1
            elif time > baseToSecond(self.colorEvents[self.colorIndex]["startTime"]):
                color = self.colorEvents[self.colorIndex]["start"]
                self.color = f"#{color[0]:02X}{color[1]:02X}{color[2]:02X}"
    def updateWindow(self):
        self.moveWindowX()
        self.moveWindowY()
        self.windowAlpha()
        self.scaleXWindow()
        self.scaleYWindow()
        self.getText()
        self.getColor()
        # 更新窗口位置
        self.root.geometry(f"{int(self.w)}x{int(self.h)}+{int(self.x - self.w / 2)}+{int(self.y - self.h / 2)}")
        # 窗口透明度
        self.root.attributes("-alpha", self.a)
        # 窗口文本
        self.label.config(text=f"{self.text}",font=("Arial", 24),anchor="center",bg=self.color)
        self.label.place(relx=0.5, rely=0.5, anchor="center")
        # 窗口背景色
        self.root.config(bg=self.color)
    
        self.root.after(16, self.updateWindow)

# 窗口列表
windows = []

# 创建窗口
for i in range(readChart.NumberOfLines):
    window = PlayerWindow(i)
    windows.append(window)
    window.updateWindow()

# 定义一个事件来通知主循环音乐播放结束
pygame.QUIT_EVENT = pygame.USEREVENT + 1

pygame.mixer.music.play()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT_EVENT:
            running = False
    
    if not pygame.mixer.music.get_busy():
        pygame.event.post(pygame.event.Event(pygame.QUIT_EVENT))
    
    for window in windows:
        window.root.update()

for window in windows:
    window.root.destroy()