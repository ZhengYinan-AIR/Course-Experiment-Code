import threading
from tkinter import *
#from demo_tcp_recieve import tcp_recieve
import time
import socket
import os

info_title = ['编号: ', '姓名: ', '性别: ', '年龄: ', '体温: ', '心率: ', '血压: ']
info = [['1', '张三', '男', '21', '37.2', '63', '70/122'],
        ['2', '李四', '女', '23', '37.9', '62', '50/123'],
        ['3', '王五', '男', '26', '39.5', '61', '60/124']]
data_recieve = ''
data_recieve_process = []
data_transmit_process = []


def show_client(delay):
    print('show_client')
    global root
    global cv
    root = Tk()
    root.title("病房监控")
    cv = Canvas(root, width=900, height=500)
    cv.pack(fill=BOTH, expand=YES) 

    def print_info_case():
        global info
        k = 0
        for info_i in info:
            pos_x = 40*(k+1) + 250*k
            pos_y = 180
            j = 0
            for i in info_i:
                text1 = cv.create_text(
                        pos_x + 20, pos_y + 40*j,
                        text = info_title[j] + i,
                        font = ('Consolas', 20),
                        anchor = W
                        )
                j += 1
                #print(text1)
            k += 1


    # outline
    outline = cv.create_rectangle(
            0, 0, 900, 600,
            outline = 'lightyellow',
            fill = 'skyblue',
            width = 4
            )
    
    # door number and background
    oval1 = cv.create_oval(
            300, 30, 600, 130,
            outline = 'lightyellow',
            fill = 'paleturquoise',
            width = 4
            )
    
    door_number = cv.create_text(
            390, 80,
            text = "502",
            font = ('Consolas', 50),
            anchor = W
            )
    
    def print_case_info_background():
        global flag
        # case_information
        for i in range(3):
            pos_x = 40*(i+1) + 250*i
            pos_y = 180
            rectangle1 = cv.create_rectangle(
                    33*(i+1) + 250*i, 150, 33*(i+1) + 250*i + 270, 460,
                    width = 4,
                    outline = 'turquoise',
                    fill = 'lemonchiffon'
                    )
        #    print(33*(i+1) + 250*i)
        print_info_case()
        root.after(10, print_case_info_background)
    print_case_info_background()
    change = Button(text='上传', command=changescreen).place(x=790, y=50)
    root.mainloop()

def changescreen():
    # outline
    # global flag
    # flag=1
    # outline = cv.create_rectangle(
    #     0, 0, 900, 600,
    #     outline='#F0F8FF',
    #     fill='#F0F8FF',
    #     width=4
    # )

    # # door number and background
    # oval1 = cv.create_oval(
    #     300, 30, 600, 130,
    #     outline='#F0F8FF',
    #     fill='#F0F8FF',
    #     width=4
    # )
    # print(oval1)
    #
    # for i in range(3):
    #     pos_x = 40 * (i + 1) + 250 * i
    #     pos_y = 180
    #     rectangle1 = cv.create_rectangle(
    #         33 * (i + 1) + 250 * i, 150, 33 * (i + 1) + 250 * i + 270, 460,
    #         width=4,
    #         outline='#F0F8FF',
    #         fill='#F0F8FF'
    #     )
    #     #    print(33*(i+1) + 250*i)
    #     print(rectangle1)


    # root2 = Tk()
    # Smartward.Smart_ward(root2)
    # root2.mainloop()
    os.popen('python3 D:\study\嵌入式arm\嵌入式实习\智能病房\Smartward.py')
    time.sleep(5)
    root.destroy()
    return

def tcp_recieve(port, data_recieve, delay):
    global data_recieve_process
    global info
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
        
        #print(info)
        # 接收客户端发送过来的请求
        recv_data = new_client_socket.recv(1024)
        print(recv_data)
        data = recv_data
        data_recieve_process = data.split()
        #print("recieve")
        #print(type(data_recieve_process))
        #print(data_recieve_process)
        
        # 回送一部分数据给客户端
        new_client_socket.send("hahahghai-----ok-----".encode("utf-8"))
        time.sleep(delay)
    
    # 关闭套接字
    new_client_socket.close()
    tcp_server_socket.close()


def tcp_transmit(ip, port, data,delay):

    # 1. 创建tcp的套接字
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 2. 链接服务器
    # tcp_socket.connect(("192.168.33.11", 7890))
    server_ip = ip
    server_port = port
    server_addr = (server_ip, server_port)
    tcp_socket.connect(server_addr)

    while True:
        # 3. 发送数据/接收数据
        #send_data = input("请输入要发送的数据:")
        tcp_socket.send(data.encode("utf-8"))

        time.sleep(delay)

    # 4. 关闭套接字
    tcp_socket.close()


def process_global(delay):
    global data_recieve_process
    global info
    temp = []
    while True:
        temp.clear()

        #temp = str(data_recieve_process, 'utf-8')
        #print(type(data_recieve_process[0]))
        #print(temp)

        if data_recieve_process:
            for i in data_recieve_process:
                i = str(i, 'utf-8')
                temp.append(i)
            #print(temp)

        if temp:
            if temp[0] == '204' and temp[5] == '255':
                for i in range(2, 5):
                    info[int(temp[1])-1][i+2] = temp[i]
            
        time.sleep(delay)


try:
    thread1 = threading.Thread(target=show_client, args=(0.1,))
    #thread2 = threading.Thread(target=tcp_transmit, args=('127.0.0.1', 7890, Smartward.transmitlist, 0.1,))
    thread3 = threading.Thread(target=tcp_recieve, args=(7890, data_recieve, 0.2,))
    thread4 = threading.Thread(target=process_global, args=(0.1,))
    thread1.setDaemon(True)
    thread1.start()
    print('STARTING Thread-1')
    #thread2.start()
    #print('STARTING Thread-2')
    thread3.start()
    print('STARTING Thread-3')
    thread4.start()
    print('STARTING Thread-4')
except:
    print('ERROR: 无法启动线程')

thread1.join()
#thread2.join()
thread3.join()
thread4.join()

print("main process end.")
