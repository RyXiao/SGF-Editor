import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import filedialog
import copy


class Application(ttk.Frame):

    # 初始化棋盘，默认十九路棋盘
    def __init__(self, master):
        super().__init__(master, padding=(20, 10))
        self.pack(fill=BOTH, expand=YES)
        # 模式, 九路：9，十三路：13，十九路：19
        self.mode_num = 19
        # # 窗口尺寸设置，默认：1.8
        self.size = 1.8
        # # 棋盘每格的边长
        self.gap = 360 * self.size / (self.mode_num - 1)
        # # 相对于9路棋盘的矫正比例
        self.p = 1 if self.mode_num == 9 else (2 / 3 if self.mode_num == 13 else 4 / 9)
        # 初始化棋盘，所有超过边界的值设置为-1
        self.positions = [[0 for i in range(self.mode_num + 2)] for i in range(self.mode_num + 2)]
        for i in range(self.mode_num + 2):
            for j in range(self.mode_num + 2):
                if (i * j == 0 or i == self.mode_num + 1 or j == self.mode_num + 1):
                    self.positions[i][j] = -1

        # 记录鼠标经过的地方,用于显示shadow时
        self.cross_last = None

        # 当前轮到棋子颜色，黑：0，白：1，默认黑
        self.present = 0
        self.stop = False

        self.photoW = ttk.PhotoImage(file="./Pictures/W.png")
        self.photoB = ttk.PhotoImage(file="./Pictures/B.png")
        self.photoBD = ttk.PhotoImage(file="./Pictures/" + "BD" + "-" + str(self.mode_num) + ".png")
        self.photoWD = ttk.PhotoImage(file="./Pictures/" + "WD" + "-" + str(self.mode_num) + ".png")
        self.photoBU = ttk.PhotoImage(file="./Pictures/" + "BU" + "-" + str(self.mode_num) + ".png")
        self.photoWU = ttk.PhotoImage(file="./Pictures/" + "WU" + "-" + str(self.mode_num) + ".png")

        # 用于黑白棋子图片切换的列表
        self.photoWBU_list = [self.photoBU, self.photoWU]
        self.photoWBD_list = [self.photoBD, self.photoWD]

        #画布控件，作为容器

        self.canvas_bottom = ttk.Canvas(self, bg='#369', bd = 0, width = 600*self.size, height =400*self.size)
        self.canvas_bottom.place(x=0,y=0)
        # 画棋盘
        self.canvas_bottom.create_rectangle(0 * self.size, 0 * self.size, 400 * self.size, 400 * self.size,
                                            fill='white')

        # 画外框
        self.canvas_bottom.create_rectangle(20 * self.size, 20 * self.size, 380 * self.size, 380 * self.size, width=3)
        # 画9个点,先定位中间，然后移动到周围8个点对应就是10线移动到4线，19路棋盘就是移动6，13路就是3，9路就是2
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                self.original = self.canvas_bottom.create_oval(200 * self.size - self.size * 2,
                                                               200 * self.size - 2 * self.size,
                                                               200 * self.size + self.size * 2,
                                                               200 * self.size + self.size * 2, fill='#000')
                self.canvas_bottom.move(self.original, i * self.gap * (
                    6 if self.mode_num == 19 else (3 if self.mode_num == 13 else 2)),
                                        j * self.gap * (
                                            6 if self.mode_num == 19 else (3 if self.mode_num == 13 else 2)))
        # 画中间的线条
        for i in range(1, self.mode_num - 1):
            self.canvas_bottom.create_line(20 * self.size, 20 * self.size + i * self.gap, 380 * self.size,
                                           20 * self.size + i * self.gap, width=2)
            self.canvas_bottom.create_line(20 * self.size + i * self.gap, 20 * self.size, 20 * self.size + i * self.gap,
                                           380 * self.size, width=2)
        self.create_buttonbox()

        #鼠标移动时，调用shadow函数，显示随着鼠标移动的棋子
        self.canvas_bottom.bind('<Motion>', self.shadow)
        #鼠标左键单击时，调用leftdown函数，放下当前颜色棋子
        self.canvas_bottom.bind('<Button-1>', self.leftdown)
        #鼠标右键单击时，调用rightdown函数，放下当前颜色棋子
        self.canvas_bottom.bind('<Button-3>', self.rightdown)


    def create_buttonbox(self):
        container = ttk.Frame(self)
        container.pack(anchor=E,fill=Y)
        self.whiteButton = ttk.Button(master=container,bootstyle="success", text='白', command = self.whitemode, )
        self.whiteButton.pack(fill=X, expand=True, ipadx=100, ipady=15)
        self.blackButton = ttk.Button(master=container, bootstyle="dark", text='黑', command = self.blackmode)
        self.blackButton.pack(fill=X, expand=True, ipadx=100, ipady=15, pady=1)
        self.newGameButton = ttk.Button(master=container, bootstyle="outline", text='新建棋谱', command = self.newGame)
        self.newGameButton.pack(fill=X, expand=True, ipadx=100, ipady=15, pady=1)
        self.quiteButton = ttk.Button(master=container, bootstyle="outline", text='退出', command = self.quit_game)
        self.quiteButton.pack(fill=X, expand=True, ipadx=100, ipady=15, pady=1)
        self.openButton = ttk.Button(master=container, bootstyle="outline", text='打开棋谱', command=self.openFile)
        self.openButton.pack(fill=X, expand=True, ipadx=100, ipady=15, pady=1)
        self.saveButton = ttk.Button(master=container, bootstyle="outline", text='保存棋谱', command=self.saveFile)
        self.saveButton.pack(fill=X, expand=True, ipadx=100, ipady=15, pady=1)
        self.blackButton['state'] = 'disabled'

    def openFile(self):
        return 0

    def quit_game(self):
        self.quit()

    def saveFile(self):
        strB = "(;CA[gb2312]AB"
        strW = "AW"
        strDefault = "AP[MultiGo:4.4.4]SZ[19]"
        for i in range(1, self.mode_num + 1):
            for j in range(1, self.mode_num + 1):
                if self.positions[i][j] == 1:
                    strB += '[' + num_alpha[str(j)] + num_alpha[str(i)] + ']'
                if self.positions[i][j] == 2:
                    strW += '[' + num_alpha[str(j)] + num_alpha[str(i)] + ']'
        SGF_content = strB + strW + strDefault
        FilePath = filedialog.asksaveasfilename(title=u'保存文件')
        if FilePath is not None:
            with open(file=FilePath, mode='w', encoding='utf-8') as file:
                file.write(SGF_content)

    # 重置棋盘，并且将棋盘设置为黑棋先下
    def newGame(self):
        global newApp
        self.present = 0
        self.canvas_bottom.delete('image')
        for i in range(1, self.mode_num + 1):
            for j in range(1, self.mode_num + 1):
                self.positions[i][j] = 0
        newApp = True
        self.quit()

    def shadow(self, event):
        if not self.stop:
            # 找到最近的格子，在当前位置靠近的格点显示棋子图片，并删除上一位置的棋子图片
            if (20 * self.size < event.x < 380 * self.size) and (20 * self.size < event.y < 380 * self.size):
                dx = (event.x - 20 * self.size) % self.gap
                dy = (event.y - 20 * self.size) % self.gap
                self.cross = self.canvas_bottom.create_image(
                    event.x - dx + round(dx / self.gap) * self.gap + 22 * self.p,
                    event.y - dy + round(dy / self.gap) * self.gap - 27 * self.p,
                    image=self.photoWBU_list[self.present])
                self.canvas_bottom.addtag_withtag('image', self.cross)
                if self.cross_last != None:
                    self.canvas_bottom.delete(self.cross_last)
                self.cross_last = self.cross

    # 定义鼠标左键添加棋子
    def leftdown(self, event):
        if (20 * self.size - self.gap * 0.4 < event.x < self.gap * 0.4 + 380 * self.size) and (
                20 * self.size - self.gap * 0.4 < event.y < 380 * self.size + self.gap * 0.4):
            dx = (event.x - 20 * self.size) % self.gap
            dy = (event.y - 20 * self.size) % self.gap
            x = int((event.x - 20 * self.size - dx) / self.gap + round(dx / self.gap) + 1)
            y = int((event.y - 20 * self.size - dy) / self.gap + round(dy / self.gap) + 1)
            if self.present == 0:
                color = 1
            else:
                color = 2
            # 判断位置是否已经被占据
            if self.positions[y][x] == 0:
                # 未被占据，则尝试占据，获得占据后杀死的棋子列表
                self.positions[y][x] = self.present + 1
                self.image_added = self.canvas_bottom.create_image(
                    event.x - dx + round(dx / self.gap) * self.gap + 4 * self.p,
                    event.y - dy + round(dy / self.gap) * self.gap - 5 * self.p, image=self.photoWBD_list[self.present])
                self.canvas_bottom.addtag_withtag('position' + str(x) + str(y), self.image_added)
                deadlist = self.get_deadlist(x, y, color)
                self.kill(deadlist)
            elif self.positions[y][x] == 1:
                if self.present == 0:
                    self.positions[y][x] = 0
                    self.canvas_bottom.delete('position' + str(x) + str(y))
                else:
                    self.positions[y][x] = 2
                    self.canvas_bottom.delete('position' + str(x) + str(y))
                    self.image_added = self.canvas_bottom.create_image(
                        event.x - dx + round(dx / self.gap) * self.gap + 4 * self.p,
                        event.y - dy + round(dy / self.gap) * self.gap - 5 * self.p,
                        image=self.photoWBD_list[self.present])
                    self.canvas_bottom.addtag_withtag('position' + str(x) + str(y), self.image_added)
                    deadlist = self.get_deadlist(x, y, color)
                    self.kill(deadlist)
            else:
                if self.present == 0:
                    self.positions[y][x] = 1
                    self.canvas_bottom.delete('position' + str(x) + str(y))
                    self.image_added = self.canvas_bottom.create_image(
                        event.x - dx + round(dx / self.gap) * self.gap + 4 * self.p,
                        event.y - dy + round(dy / self.gap) * self.gap - 5 * self.p,
                        image=self.photoWBD_list[self.present])
                    self.canvas_bottom.addtag_withtag('position' + str(x) + str(y), self.image_added)
                    deadlist = self.get_deadlist(x, y, color)
                    self.kill(deadlist)
                else:
                    self.positions[y][x] = 0
                    self.canvas_bottom.delete('position' + str(x) + str(y))

    # 定义鼠标右键添加棋子，右键添加的是当前颜色的相反色棋子
    def rightdown(self, event):
        if (20 * self.size - self.gap * 0.4 < event.x < self.gap * 0.4 + 380 * self.size) and (
                20 * self.size - self.gap * 0.4 < event.y < 380 * self.size + self.gap * 0.4):
            dx = (event.x - 20 * self.size) % self.gap
            dy = (event.y - 20 * self.size) % self.gap
            x = int((event.x - 20 * self.size - dx) / self.gap + round(dx / self.gap) + 1)
            y = int((event.y - 20 * self.size - dy) / self.gap + round(dy / self.gap) + 1)
            if self.present == 0:
                color = 2
            else:
                color = 1
            # 判断位置是否已经被占据
            if self.positions[y][x] == 0:
                # 未被占据，则尝试占据，获得占据后杀死的棋子列表
                self.positions[y][x] = 1 - self.present + 1
                self.image_added = self.canvas_bottom.create_image(
                    event.x - dx + round(dx / self.gap) * self.gap + 4 * self.p,
                    event.y - dy + round(dy / self.gap) * self.gap - 5 * self.p,
                    image=self.photoWBD_list[1 - self.present])
                self.canvas_bottom.addtag_withtag('position' + str(x) + str(y), self.image_added)
                deadlist = self.get_deadlist(x, y, color)
                self.kill(deadlist)
            elif self.positions[y][x] == 1:
                if self.present == 0:
                    self.positions[y][x] = 2
                    self.canvas_bottom.delete('position' + str(x) + str(y))
                    self.image_added = self.canvas_bottom.create_image(
                        event.x - dx + round(dx / self.gap) * self.gap + 4 * self.p,
                        event.y - dy + round(dy / self.gap) * self.gap - 5 * self.p,
                        image=self.photoWBD_list[self.present])
                    self.canvas_bottom.addtag_withtag('position' + str(x) + str(y), self.image_added)
                    deadlist = self.get_deadlist(x, y, color)
                    self.kill(deadlist)
                else:
                    self.positions[y][x] = 0
                    self.canvas_bottom.delete('position' + str(x) + str(y))

            else:
                if self.present == 0:
                    self.positions[y][x] = 0
                    self.canvas_bottom.delete('position' + str(x) + str(y))

                else:
                    self.positions[y][x] = 1
                    self.canvas_bottom.delete('position' + str(x) + str(y))
                    self.image_added = self.canvas_bottom.create_image(
                        event.x - dx + round(dx / self.gap) * self.gap + 4 * self.p,
                        event.y - dy + round(dy / self.gap) * self.gap - 5 * self.p,
                        image=self.photoWBD_list[1 - self.present])
                    self.canvas_bottom.addtag_withtag('position' + str(x) + str(y), self.image_added)
                    deadlist = self.get_deadlist(x, y, color)
                    self.kill(deadlist)

    def if_dead(self, deadList, yourChessman, yourPosition):
        for i in [-1, 1]:
            if [yourPosition[0] + i, yourPosition[1]] not in deadList:
                if self.positions[yourPosition[1]][yourPosition[0] + i] == 0:
                    return False
            if [yourPosition[0], yourPosition[1] + i] not in deadList:
                if self.positions[yourPosition[1] + i][yourPosition[0]] == 0:
                    return False
        if ([yourPosition[0] + 1, yourPosition[1]] not in deadList) and (
                self.positions[yourPosition[1]][yourPosition[0] + 1] == yourChessman):
            midvar = self.if_dead(deadList + [[yourPosition[0] + 1, yourPosition[1]]], yourChessman,
                                  [yourPosition[0] + 1, yourPosition[1]])
            if not midvar:
                return False
            else:
                deadList += copy.deepcopy(midvar)

        if ([yourPosition[0] - 1, yourPosition[1]] not in deadList) and (
                self.positions[yourPosition[1]][yourPosition[0] - 1] == yourChessman):
            midvar = self.if_dead(deadList + [[yourPosition[0] - 1, yourPosition[1]]], yourChessman,
                                  [yourPosition[0] - 1, yourPosition[1]])
            if not midvar:
                return False
            else:
                deadList += copy.deepcopy(midvar)

        if ([yourPosition[0], yourPosition[1] + 1] not in deadList) and (
                self.positions[yourPosition[1] + 1][yourPosition[0]] == yourChessman):
            midvar = self.if_dead(deadList + [[yourPosition[0], yourPosition[1] + 1]], yourChessman,
                                  [yourPosition[0], yourPosition[1] + 1])
            if not midvar:
                return False
            else:
                deadList += copy.deepcopy(midvar)

        if ([yourPosition[0], yourPosition[1] - 1] not in deadList) and (
                self.positions[yourPosition[1] - 1][yourPosition[0]] == yourChessman):
            midvar = self.if_dead(deadList + [[yourPosition[0], yourPosition[1] - 1]], yourChessman,
                                  [yourPosition[0], yourPosition[1] - 1])
            if not midvar:
                return False
            else:
                deadList += copy.deepcopy(midvar)
        return deadList

    def whitemode(self):
        self.present = 1
        self.blackButton['state']='active'
        self.whiteButton['state']='disabled'
    #激活黑棋模式
    def blackmode(self):
        self.present = 0
        self.blackButton['state']='disabled'
        self.whiteButton['state']='active'

    def get_deadlist(self, x, y, color):
        deadlist = []
        for i in [-1, 1]:
            if self.positions[y][x + i] == (2 if color == 1 else 1) and ([x + i, y] not in deadlist):
                killList = self.if_dead([[x + i, y]], (2 if color == 1 else 1), [x + i, y])
                if not killList == False:
                    deadlist += copy.deepcopy(killList)
            if self.positions[y + i][x] == (2 if color == 1 else 1) and ([x, y + i] not in deadlist):
                killList = self.if_dead([[x, y + i]], (2 if color == 1 else 1), [x, y + i])
                if not killList == False:
                    deadlist += copy.deepcopy(killList)
        return deadlist

    def kill(self, killList):
        if len(killList) > 0:
            for i in range(len(killList)):
                self.positions[killList[i][1]][killList[i][0]] = 0
                self.canvas_bottom.delete('position' + str(killList[i][0]) + str(killList[i][1]))

global mode_num, newApp, num_alpha

# 设置19路棋盘
mode_num = 19
newApp = False

# 通过数值专城英文作为SGF的坐标
num_alpha = {'1': 'a', '2': 'b', '3': 'c', '4': 'd', '5': 'e', '6': 'f', '7': 'g', '8': 'h', '9': 'i', '10': 'j',
             '11': 'k', '12': 'l', '13': 'm', '14': 'n', '15': 'o', '16': 'p', '17': 'q', '18': 'r', '19': 's'}

if __name__ == '__main__':
    while True:
        newApp = False
        app = ttk.Window("SGF Editor V1", "yeti", size=(1080, 750))
        Application(app)
        app.mainloop()
        if newApp:
            app.destroy()
        else:
            break

