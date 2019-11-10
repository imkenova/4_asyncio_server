import socket
import threading

def update_chat():
    global username
    while True:
        answer = sock.recv(1024)	
        if '@'+username in answer.decode().split():	
            print("Вас упомянули в сообщении")
            print(f'\n',answer.decode())
        else:	
            print(f'\n',answer.decode())


host = input('Введите имя хоста: ')
if host == 'localhost':
    pass
else:
    if any(c.isalpha() for c in host) == True:
        print('Введено некорректное имя хоста.По умолчанию выбран локальный хост')
        host = 'localhost'
    else:
        host_lst = host.split('.')           
        for i in host_lst:
            if 0 <= int(i) <= 255:
                pass
            else:
                host = 'localhost'
                print('Введено некорректное имя хоста.По умолчанию выбран локальный хост')

try:
    port = int(input('Введите номер порта: '))
    if 0 <= port <= 65535:
        pass
    else:
        print('Введен некорректный номер порта.Номер порта по умолчанию 9090')
        port = 9090
        
except ValueError:
    print("Некорректный номер порта. Номер порта по умолчанию 9090")
    port = 9090  

sock = socket.socket()
sock.connect((host,port))

username = ''
password = ''

while not username:     
    username = input('Введите Ваше имя: ')

sock.send(username.encode())		
answer = sock.recv(1024)


if answer.decode() == 'registration':
    print('Вы еще не зарегистрированы.')
    print(f'Регистрируемое имя: {username}')
    while not password:	
        password = input('Придумайте пароль:')
    sock.send(password.encode())	
    answer = sock.recv(1024)
    if answer.decode() == 'completed':	
        print('Регистрация завершена. Пожалуйста,перезапустите программу')
else:
    password = input('Введите пароль: ')
    sock.send(password.encode())
    answer = sock.recv(1024)
    if answer.decode() == 'valid':     
        print("Для упоминания пользователя используйте формат @имя")
        print("Для выхода из чата введите exit")
        threading.Thread(target=update_chat,args=()).start()
        while True:	
            msg = input('')
            if msg == 'exit':
                sock.send('exit'.encode())
                break
            sock.send(msg.encode())
    else:
        print('Неправильный пароль')

sock.close()
print("Работа с сервером завершена.")		
