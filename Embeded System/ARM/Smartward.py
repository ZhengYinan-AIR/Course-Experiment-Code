from tkinter import ttk
from tkinter import *
import sqlite3
import time

transmitlist=[]
class Smart_ward:
    # 数据库名字
    db_name = 'Smart_ward.db'

    # 初始化操作
    def __init__(self, window):
        self.win = window
        self.win.title("智能病房")
        #self.win.configure(bg='#F0F8FF')
        width = 900
        height = 500
        align_str = '%dx%d' % (width, height)
        window.geometry(align_str)

        self.nurseno = '001'

        # treeview进行左表格显示
        columns = ("#1", "#2", "#3", "#4", "#5", "#6", "#7", "#8")
        self.tree = ttk.Treeview(height=19, column=columns, show='headings')
        for col in columns:
            if col == '#6':
                self.tree.heading(col, text=col)
                self.tree.column(col, width=200, anchor=CENTER)
            else:
                self.tree.heading(col, text=col)
                self.tree.column(col, width=80, anchor=CENTER)
        # self.tree.grid(row=0, column=0, columnspan=1)
        self.tree.place(x=10, y=10)
        self.tree.heading("#1", text="病人编号", anchor=CENTER)
        self.tree.heading("#2", text="姓名", anchor=CENTER)
        self.tree.heading("#3", text="体温(℃)", anchor=CENTER)
        self.tree.heading("#4", text="血压(mmHg)", anchor=CENTER)
        self.tree.heading("#5", text="血糖(mmol/l)", anchor=CENTER)
        self.tree.heading("#6", text="登记日期", anchor=CENTER)
        self.tree.heading("#7", text="登记护士号", anchor=CENTER)
        self.tree.heading("#8", text="备注", anchor=CENTER)

        # 绘制表格
        self.dbdisplay()

        # label定义
        self.Pno = Label(text='', bg='#F0F8FF', fg='black', justify=CENTER)
        self.Pno.place(x=780, y=10)
        self.Pno['text'] = "病人编号"

        self.Pname = Label(text='', fg='black', bg='#F0F8FF', justify=CENTER)
        self.Pname.place(x=780, y=50)
        self.Pname['text'] = "姓名"

        self.temp = Label(text=' ', fg='black', bg='#F0F8FF', justify=CENTER)
        self.temp.place(x=780, y=90)
        self.temp['text'] = "体温(℃)"

        self.pressure = Label(text=' ', fg='black', bg='#F0F8FF', justify=CENTER)
        self.pressure.place(x=780, y=130)
        self.pressure['text'] = "血压(mmHg)"

        self.sugure = Label(text=' ', fg='black', bg='#F0F8FF', justify=CENTER)
        self.sugure.place(x=780, y=170)
        self.sugure['text'] = "血糖(mmol/l)"

        self.no = Label(text=' ', fg='black', bg='#F0F8FF', justify=CENTER)
        self.no.place(x=780, y=210)
        self.no['text'] = "登记护士号"

        self.message = Label(text=' ', fg='black', bg='#F0F8FF', justify=CENTER)
        self.message.place(x=780, y=250)
        self.message['text'] = "备注"

        self.warnning = Label(text=' ', fg='black', bg='#F0F8FF', justify=CENTER)
        self.warnning.place(x=810, y=420)

        # 用户输入entry
        self.Pno_change = ttk.Entry(window, show=None, width=15)
        self.Pno_change.place(x=780, y=30)

        self.Pname_change = ttk.Entry(window, show=None, width=15)
        self.Pname_change.place(x=780, y=70)

        self.temp_change = ttk.Entry(window, show=None, width=15)
        self.temp_change.place(x=780, y=110)

        self.pressure_change = ttk.Entry(window, show=None, width=15)
        self.pressure_change.place(x=780, y=150)

        self.sugure_change = ttk.Entry(window, show=None, width=15)
        self.sugure_change.place(x=780, y=190)

        self.no_change = ttk.Entry(window, show=None, width=15)
        self.no_change.place(x=780, y=230)

        self.message_change = ttk.Entry(window, show=None, width=15)
        self.message_change.place(x=780, y=270)

        # 按键
        self.change = ttk.Button(text='修改', command=self.Change).place(x=790, y=300)
        self.add = ttk.Button(text='添加', command=self.Add).place(x=790, y=340)
        self.up = ttk.Button(text='上传', command=self.UPdata).place(x=790, y=380)

    def dbdisplay(self):
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)
        query = "select * from Patient"
        params = ()
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            db_rows = conn.execute(query, params)
            conn.commit()
        # db_rows = self.run_query(query)
        # 填充表格
        for row in db_rows:
            self.tree.insert("", 'end', value=row)

    # 数据库操作方法
    # def run_query(self, query, params=()):
    #     with sqlite3.connect(self.db_name) as conn:
    #         cursor = conn.cursor()
    #         result_ = conn.execute(query, params)
    #         conn.commit()
    #         return result_
    def UPdata(self):
        global transmitlist
        transmitlist = []
        for item in self.tree.selection():
            item_text = self.tree.item(item, "values")
            sendstring = "502" + " " + item_text[0] + " " + item_text[1] + " " + item_text[2] + " " + item_text[
                3] + " " + item_text[4] + " " + item_text[6] + " " + item_text[7] + " " + "345"
            transmitlist.append(sendstring)
            print(sendstring)  # 输出所选行的第一列的值

        return

    def Change(self):
        state = [0, 0, 0, 0, 0, 0]
        Pno_get = self.Pno_change.get()  # 获取输入的信息
        Pname_get = self.Pname_change.get()
        temp_get = self.temp_change.get()
        print(temp_get)
        pressure_get = self.pressure_change.get()
        sugure_get = self.sugure_change.get()
        message_get = self.message_change.get()
        if Pno_get: state[0] = 1
        if Pname_get: state[1] = 1
        if temp_get: state[2] = 1
        if pressure_get: state[3] = 1
        if sugure_get: state[4] = 1
        if message_get: state[5] = 1
        if sum(state) != 0:
            list_real = []
            r = self.tree.item(self.tree.selection(), "values")
            if state[2] == 1:
                query = "update Patient set temp='%s' where Pno='%s'" % (temp_get, r[0])
                params = ()
                with sqlite3.connect(self.db_name) as conn:
                    cursor = conn.cursor()
                    db_rows = conn.execute(query, params)
                    conn.commit()
            if state[3] == 1:
                query = "update Patient set pressure='%s' where Pno='%s'" % (pressure_get, r[0])
                params = ()
                with sqlite3.connect(self.db_name) as conn:
                    cursor = conn.cursor()
                    db_rows = conn.execute(query, params)
                    conn.commit()
            if state[4] == 1:
                query = "update Patient set sugure='%s' where Pno='%s'" % (sugure_get, r[0])
                params = ()
                with sqlite3.connect(self.db_name) as conn:
                    cursor = conn.cursor()
                    db_rows = conn.execute(query, params)
                    conn.commit()
            if state[5] == 1:
                query = "update Patient set message='%s' where Pno='%s'" % (message_get, r[0])
                params = ()
                with sqlite3.connect(self.db_name) as conn:
                    cursor = conn.cursor()
                    db_rows = conn.execute(query, params)
                    conn.commit()
            self.dbdisplay()
            self.warnning['text'] = '修改成功'

    def Add(self):
        state = [0, 0, 0, 0, 0]
        Pno_get = self.Pno_change.get()  # 获取输入的信息
        Pname_get = self.Pname_change.get()
        temp_get = self.temp_change.get()
        pressure_get = self.pressure_change.get()
        sugure_get = self.sugure_change.get()
        data_get = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        if Pno_get: state[0] = 1
        if Pname_get: state[1] = 1
        if temp_get: state[2] = 1
        if pressure_get: state[3] = 1
        if sugure_get: state[4] = 1
        if Pno_get:
            query = "insert into Patient values('%s','%s','%s','%s','%s','%s','%s',NULL)" % (
            Pno_get, Pname_get, temp_get, pressure_get, sugure_get, data_get, self.nurseno)
            params = ()
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                db_rows = conn.execute(query, params)
                conn.commit()
            self.dbdisplay()
            self.warnning['text'] = '添加成功'
        else:
            self.warnning['text'] = '请输入病人编号'


window = Tk()
window.configure(bg='#F0F8FF')
window.attributes("-alpha", 0.95)
application = Smart_ward(window)
window.mainloop()
