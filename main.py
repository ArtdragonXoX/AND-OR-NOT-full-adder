from PySide6.QtWidgets import QApplication,QMainWindow,QTableWidgetItem
from PySide6.QtCore import  Qt,Signal,QObject
from ui_demo import Ui_MainWindow
import time
from threading import Thread

#qRegisterMetaType()


class Customsignals(QObject):                   #信号类
    printToQlabel = Signal(int,str)          #对Qlabel类打印的信号
    printToRecord = Signal(list)                #专门处理记录列表的信号
    showQlabel = Signal(int)                 #处理控件显示的信号
    hideQlabel = Signal()                       #将所有加法器过程显示控件隐藏
    default = Signal()


Mysignals=Customsignals()

class MainWindow(QMainWindow):
    p=''
    row=0
    sleeptime=0.0
    def __init__(self):
        super(MainWindow,self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowFlags(Qt.FramelessWindowHint)         #将界面设置为无框
        self.setAttribute(Qt.WA_TranslucentBackground)      #将界面属性设置为半透明
        self.default_location()                             #默认界面
        self.band()                                         #槽绑定

    def mousePressEvent(self, event):        #鼠标左键按下时获取鼠标坐标
        if event.button() == Qt.LeftButton:
            self._move_drag = True
            self.m_Position = event.globalPos() - self.pos()
            event.accept()
    
    def mouseMoveEvent(self, QMouseEvent):    #鼠标在按下左键的情况下移动时,根据坐标移动界面
        if Qt.LeftButton and self._move_drag:
            self.move(QMouseEvent.globalPos() - self.m_Position)
            QMouseEvent.accept()
    
    def mouseReleaseEvent(self, QMouseEvent):    #鼠标按键释放时,取消移动
        self._move_drag = False
    

    def band(self):                         #槽绑定
        self.ui.Countbuttons.clicked.connect(self.add)
        Mysignals.printToQlabel.connect(self.print_Qlabel)
        Mysignals.printToRecord.connect(self.addrecord)
        Mysignals.showQlabel.connect(self.showfunc)
        Mysignals.hideQlabel.connect(self.hideAdder)
        Mysignals.default.connect(self.default_location)
        self.ui.ChangeSleep.clicked.connect(self.changesleeptime)

    def default_location(self):                 #默认界面
        self.ui.StandA0.resize(0,0)             #0
        self.ui.StandA1.resize(0,0)             #1
        self.ui.StandB0.resize(0,0)             #2
        self.ui.StandB1.resize(0,0)             #3
        self.ui.Carry0.resize(0,0)              #4
        self.ui.Carry1.resize(0,0)              #5
        self.ui.Standxor0.resize(0,0)           #6
        self.ui.Standxor1.resize(0,0)           #7
        self.ui.Standout0.resize(0,0)           #8
        self.ui.Standout1.resize(0,0)           #9
        self.ui.Carryup0.resize(0,0)            #10
        self.ui.Carryup1.resize(0,0)            #11
        self.ui.Carrydown0.resize(0,0)          #12
        self.ui.Carrydown1.resize(0,0)          #13
        self.ui.Carryout0.resize(0,0)           #14
        self.ui.Carryout1.resize(0,0)           #15
        self.ui.NumstandA.clear()
        self.ui.NumstandB.clear()
        self.ui.Numcarry.clear()
        self.ui.Numstandout.clear()
        self.ui.Numcarryout.clear()
        self.ui.ChangeSleep.setEnabled(False)
        self.ui.Countbuttons.setEnabled(True)
        self.ui.Countbuttons.setText("开始计算")
        self.p="↓"
        self.row=0

    def hideAdder(self):
        self.ui.StandA0.resize(0,0)             #0
        self.ui.StandA1.resize(0,0)             #1
        self.ui.StandB0.resize(0,0)             #2
        self.ui.StandB1.resize(0,0)             #3
        self.ui.Carry0.resize(0,0)              #4
        self.ui.Carry1.resize(0,0)              #5
        self.ui.Standxor0.resize(0,0)           #6
        self.ui.Standxor1.resize(0,0)           #7
        self.ui.Standout0.resize(0,0)           #8
        self.ui.Standout1.resize(0,0)           #9
        self.ui.Carryup0.resize(0,0)            #10
        self.ui.Carryup1.resize(0,0)            #11
        self.ui.Carrydown0.resize(0,0)          #12
        self.ui.Carrydown1.resize(0,0)          #13
        self.ui.Carryout0.resize(0,0)           #14
        self.ui.Carryout1.resize(0,0)           #15
        self.ui.NumstandA.clear()
        self.ui.NumstandB.clear()
        self.ui.Numcarry.clear()
        self.ui.Numstandout.clear()
        self.ui.Numcarryout.clear()

    def showfunc(self,num):                      #显示控件
        number={
            0:self.ui.StandA0,
            1:self.ui.StandA1,
            2:self.ui.StandB0,
            3:self.ui.StandB1,
            4:self.ui.Carry0,
            5:self.ui.Carry1,
            6:self.ui.Standxor0,
            7:self.ui.Standxor1,
            8:self.ui.Standout0,
            9:self.ui.Standout1,
            10:self.ui.Carryup0,
            11:self.ui.Carryup1,
            12:self.ui.Carrydown0,
            13:self.ui.Carrydown1,
            14:self.ui.Carryout0,
            15:self.ui.Carryout1
        }
        fb=number.get(num)
        fb.resize(861,441)

    def print_Qlabel(self,num,text):             #往Qlabel内打印text
        operate={
            0:self.ui.BinA,
            1:self.ui.BinB,
            2:self.ui.Binres,
            3:self.ui.ptr,
            4:self.ui.res,
            5:self.ui.NumstandA,
            6:self.ui.NumstandB,
            7:self.ui.Numcarry,
            8:self.ui.Numstandout,
            9:self.ui.Numcarryout
        }
        method = operate.get(num)
        method.setText(text)


    def addrecord(self,tab):              #增加记录
        i=0
        self.ui.Record.insertRow(self.row)
        #print(tab)
        for j in tab:
            cell=QTableWidgetItem(str(j))
            self.ui.Record.setItem(self.row,i,cell)
            i+=1
        self.row+=1

    def changesleeptime(self):              #更改延时时间
        self.sleeptime=self.ui.Sleeptime.value()

    def conjun(a,b): #与
        return int(a)&int(b)

    def xor(a,b): #异或
        ta=int(a)
        tb=int(b)
        return ((~ta&tb)|(ta&~tb))

    def add(self): #加
        numF=self.ui.Firstnum.text()
        numS=self.ui.Secondnum.text()
        self.sleeptime=self.ui.Sleeptime.value()
        self.ui.Countbuttons.setEnabled(False)
        self.ui.Countbuttons.setText("计算中")
        self.ui.ChangeSleep.setEnabled(True)
        self.ui.Binres.setText("结果的二进制")
        self.ui.Record.setRowCount(0)
        self.ui.res.setText("计算结果")
        task=Thread(target=self.innerfunc,args=(numF,numS))
        task.start()

    def innerfunc(self,num1,num2):
        Mysignals.printToQlabel.emit(3,self.p)
        a=int(num1)
        b=int(num2)
        a=f'{a:b}'
        b=f'{b:b}'
        l=max(len(a),len(b))
        a=f'{a:0>{l}}'
        b=f'{b:0>{l}}'
        Mysignals.printToQlabel.emit(0,a)
        Mysignals.printToQlabel.emit(1,b)
        a=a[::-1]
        b=b[::-1]
        carry=0
        res=''
        for i,j in zip(a,b):
            
            Mysignals.printToQlabel.emit(3,self.p)
            Mysignals.printToQlabel.emit(5,i)
            Mysignals.printToQlabel.emit(6,j)
            Mysignals.printToQlabel.emit(7,str(carry))
            if i=='1':
                Mysignals.showQlabel.emit(1)
            else:
                Mysignals.showQlabel.emit(0)
            if j=='1':
                Mysignals.showQlabel.emit(3)
            else:
                Mysignals.showQlabel.emit(2)
            if carry==1:
                Mysignals.showQlabel.emit(5)
            else:
                Mysignals.showQlabel.emit(4)
            tab=[]
            tab+=i
            tab+=j
            tab+=str(carry)
            standard=MainWindow.xor(i,j)
            time.sleep(self.sleeptime)
            if standard==1:
                Mysignals.showQlabel.emit(7)
            else:
                Mysignals.showQlabel.emit(6)
            standard=MainWindow.xor(carry,standard)
            time.sleep(self.sleeptime)
            if standard==1:
                Mysignals.printToQlabel.emit(8,'1')
                Mysignals.showQlabel.emit(9)
            else:
                Mysignals.printToQlabel.emit(8,'0')
                Mysignals.showQlabel.emit(8)
            Mysignals.printToQlabel.emit(8,str(standard))
            tab+=str(standard)
            time.sleep(self.sleeptime)
            if MainWindow.conjun(i,j)==1:
                Mysignals.showQlabel.emit(13)
            else:
                Mysignals.showQlabel.emit(12)
            if MainWindow.conjun(MainWindow.xor(i,j),carry)==1:
                Mysignals.showQlabel.emit(11)
            else:
                Mysignals.showQlabel.emit(10)
            carry=MainWindow.conjun(i,j)|MainWindow.conjun(MainWindow.xor(i,j),carry)
            time.sleep(self.sleeptime)
            if carry==1:
                Mysignals.printToQlabel.emit(9,'1')
                Mysignals.showQlabel.emit(15)
            else:
                Mysignals.printToQlabel.emit(9,'0')
                Mysignals.showQlabel.emit(14)
            Mysignals.printToQlabel.emit(9,str(carry))
            tab+=str(carry)
            res+=str(standard)
            time.sleep(self.sleeptime)
            Mysignals.printToRecord.emit(tab)
            Mysignals.printToQlabel.emit(2,res[::-1])
            Mysignals.hideQlabel.emit()
            self.p+='  '
        res+=str(carry)
        if carry==1:
            Mysignals.printToQlabel.emit(3,self.p)
            Mysignals.printToRecord.emit([0,0,str(carry),str(carry),0])
            Mysignals.printToQlabel.emit(5,'0')
            Mysignals.printToQlabel.emit(6,'0')
            Mysignals.printToQlabel.emit(7,'1')
            Mysignals.showQlabel.emit(0)
            Mysignals.showQlabel.emit(2)
            Mysignals.showQlabel.emit(5)
            time.sleep(self.sleeptime)
            Mysignals.showQlabel.emit(6)
            time.sleep(self.sleeptime)
            Mysignals.showQlabel.emit(9)
            Mysignals.printToQlabel.emit(8,'1')
            time.sleep(self.sleeptime)
            Mysignals.showQlabel.emit(10)
            Mysignals.showQlabel.emit(12)
            time.sleep(self.sleeptime)
            Mysignals.showQlabel.emit(14)
            Mysignals.printToQlabel.emit(9,'0')
            time.sleep(self.sleeptime)
            Mysignals.hideQlabel.emit()
            Mysignals.printToQlabel.emit(2,res[::-1])
        res=int(str(int(res[::-1])),2)
        Mysignals.printToQlabel.emit(4,str(res))
        Mysignals.default.emit()



if __name__ == '__main__':
    app = QApplication([])  # 启动一个应用
    window = MainWindow()  # 实例化主窗口
    window.show()  # 展示主窗口
    app.exec()  # 避免程序执行到这一行后直接退出
