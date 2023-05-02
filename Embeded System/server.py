from tkinter import ttk
from tkinter import *
import tkinter.messagebox
import sqlite3
import time
import threading
import socket

# 数据库名字
db_name = 'Server.db'
data_recieve_process = []


def start():
    global tree
    global tree1
    global Rno_search
    global Pno_search
    window = Tk()
    window.configure(bg='#F0F8FF')
    window.attributes("-alpha", 0.95)

    window.title("医院管理系统")

    width = 1180
    height = 800
    align_str = '%dx%d' % (width, height)
    window.geometry(align_str)

    nurseno = '001'

    # treeview进行左表格显示
    columns = ("#1", "#2", "#3", "#4", "#5", "#6", "#7", "#8", '#9')
    tree = ttk.Treeview(height=24, column=columns, show='headings')
    for col in columns:
        if col == '#9' or col == '#7':
            tree.heading(col, text=col)
            tree.column(col, width=300, anchor=CENTER)
        else:
            tree.heading(col, text=col)
            tree.column(col, width=80, anchor=CENTER)
    # tree.grid(row=0, column=0, columnspan=1)
    tree.place(x=10, y=10)
    tree.heading("#1", text="房间号", anchor=CENTER)
    tree.heading("#2", text="病人编号", anchor=CENTER)
    tree.heading("#3", text="姓名", anchor=CENTER)
    tree.heading("#4", text="体温(℃)", anchor=CENTER)
    tree.heading("#5", text="血压(mmHg)", anchor=CENTER)
    tree.heading("#6", text="血糖(mmol/l)", anchor=CENTER)
    tree.heading("#7", text="登记日期", anchor=CENTER)
    tree.heading("#8", text="登记护士号", anchor=CENTER)
    tree.heading("#9", text="备注", anchor=CENTER)

    # 选择表格
    columns1 = ("#1", "#2", "#3", "#4", "#5", "#6", "#7", "#8", '#9')
    tree1 = ttk.Treeview(height=8, column=columns, show='headings')
    for col in columns1:
        if col == '#9' or col == '#7':
            tree1.heading(col, text=col)
            tree1.column(col, width=300, anchor=CENTER)
        else:
            tree1.heading(col, text=col)
            tree1.column(col, width=80, anchor=CENTER)
    # tree.grid(row=0, column=0, columnspan=1)
    tree1.place(x=10, y=600)
    tree1.heading("#1", text="房间号", anchor=CENTER)
    tree1.heading("#2", text="病人编号", anchor=CENTER)
    tree1.heading("#3", text="姓名", anchor=CENTER)
    tree1.heading("#4", text="体温(℃)", anchor=CENTER)
    tree1.heading("#5", text="血压(mmHg)", anchor=CENTER)
    tree1.heading("#6", text="血糖(mmol/l)", anchor=CENTER)
    tree1.heading("#7", text="登记日期", anchor=CENTER)
    tree1.heading("#8", text="登记护士号", anchor=CENTER)
    tree1.heading("#9", text="备注", anchor=CENTER)

    # 绘制表格
    dbdisplay()
    Rno_search = ttk.Entry(window, show=None, width=15)
    Rno_search.place(x=130, y=540)

    Pno_search = ttk.Entry(window, show=None, width=15)
    Pno_search.place(x=400, y=540)
    change = ttk.Button(text='按房号查找', command=searchroom).place(x=10, y=540)
    add = ttk.Button(text='按病人编号查找', command=searchno).place(x=280, y=540)
    window.mainloop()


def tests():
    tkinter.messagebox.showerror(message="error")

def searchroom():
    records = tree1.get_children()
    for element in records:
        tree1.delete(element)
    Rno_get = Rno_search.get()  # 获取输入的信息
    query = "select * from server where Rno='%s'" % (Rno_get)
    params = ()
    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()
        db_rows = conn.execute(query, params)
        conn.commit()
    # 填充表格
    for row in db_rows:
        tree1.insert("", 'end', value=row)
    return


def searchno():
    records = tree1.get_children()
    for element in records:
        tree1.delete(element)
    Pno_get = Pno_search.get()  # 获取输入的信息
    query = "select * from server where Pno='%s'" % (Pno_get)
    params = ()
    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()
        db_rows = conn.execute(query, params)
        conn.commit()
    # 填充表格
    for row in db_rows:
        tree1.insert("", 'end', value=row)
    return


def dbdisplay():
    records = tree.get_children()
    for element in records:
        tree.delete(element)
    query = "select * from server order by data"
    params = ()
    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()
        db_rows = conn.execute(query, params)
        conn.commit()
    # db_rows = run_query(query)
    # 填充表格
    for row in db_rows:
        tree.insert("", 'end', value=row)


def tcp_recieve(port, delay):
    global data_recieve_process
    print(1)
    # 1. 买个手机(创建套接字 socket)
    tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    print(2)
    # 2. 插入手机卡(绑定本地信息 bind)
    tcp_server_socket.bind(("", port))

    print(3)
    # 3. 将手机设置为正常的 响铃模式(让默认的套接字由主动变为被动 listen)
    tcp_server_socket.listen(128)

    print("-----1----")
    # 4. 等待别人的电话到来(等待客户端的链接 accept)
    new_client_socket, client_addr = tcp_server_socket.accept()
    print("-----2----")

    print(client_addr)

    while True:
        # print(info)
        # 接收客户端发送过来的请求
        recv_data = new_client_socket.recv(1024)
        # sprint(recv_data)
        data = recv_data
        data_recieve_process = data.split()
        # print("recieve")
        # print(type(data_recieve_process))
        # print(data_recieve_process)
        process_global()
        data_recieve_process = []
        # 回送一部分数据给客户端
        new_client_socket.send("hahahghai-----ok-----".encode("utf-8"))
        time.sleep(delay)

    # 关闭套接字
    new_client_socket.close()
    tcp_server_socket.close()


def process_global():
    global data_recieve_process
    temp = []
    # print(data_recieve_process)
    if data_recieve_process:
        for i in data_recieve_process:
            i = i.decode('unicode-escape')
            temp.append(i)
        print(temp)

    if temp:
        if temp[0] == '502' and temp[-1] == '345':
            data_get = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            query = "insert into server values('502','%s','%s','%s','%s','%s','%s','%s','%s')" % (
                temp[1], temp[2], temp[3], temp[4], temp[5], data_get, temp[6], temp[7])
            params = ()
            with sqlite3.connect(db_name) as conn:
                cursor = conn.cursor()
                db_rows = conn.execute(query, params)
                conn.commit()
            dbdisplay()


def tcp_recieve1(port, delay):
    global data_recieve_process1
    print(1)
    # 1. 买个手机(创建套接字 socket)
    tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    print(2)
    # 2. 插入手机卡(绑定本地信息 bind)
    tcp_server_socket.bind(("", port))

    print(3)
    # 3. 将手机设置为正常的 响铃模式(让默认的套接字由主动变为被动 listen)
    tcp_server_socket.listen(128)

    print("-----1----")
    # 4. 等待别人的电话到来(等待客户端的链接 accept)
    new_client_socket, client_addr = tcp_server_socket.accept()
    print("-----2----")

    print(client_addr)

    while True:
        # print(info)
        # 接收客户端发送过来的请求
        recv_data = new_client_socket.recv(1024)
        # sprint(recv_data)
        data = recv_data
        data_recieve_process1 = data.split()
        # print("recieve")
        # print(type(data_recieve_process1))
        # print(data_recieve_process1)
        process_global1()
        data_recieve_process1 = []
        # 回送一部分数据给客户端
        new_client_socket.send("hahahghai-----ok-----".encode("utf-8"))
        time.sleep(delay)

    # 关闭套接字
    new_client_socket.close()
    tcp_server_socket.close()


def process_global1():
    global data_recieve_process1
    temp = []
    # print(data_recieve_process1)
    if data_recieve_process1:
        for i in data_recieve_process1:
            i = i.decode('utf-8')
            temp.append(i)
        print(temp)
    if temp:
        if temp[0] == '79' and temp[1] == '99' and temp[2] == '80':
            print(1)
            tkinter.messagebox.showerror(message='502病房出现突发状况，请立刻前往查看！！！')


try:
    thread1 = threading.Thread(target=start, args=())
    thread2 = threading.Thread(target=tcp_recieve, args=(7200, 0.2,))
    thread3 = threading.Thread(target=tcp_recieve1, args=(6800, 0.2,))
    thread1.setDaemon(True)
    thread1.start()
    print('STARTING Thread-1')
    thread2.start()
    print('STARTING Thread-2')
    thread3.start()
    print('STARTING Thread-3')

except:
    print('ERROR: 无法启动线程')

thread1.join()
thread2.join()
thread3.join()

print("main process end.")
