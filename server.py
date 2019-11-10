import asyncio
import os
import pickle

users_file = 'clients.pickle'      
users = {}
connected_users = []

HOST = 'localhost'
PORT = 9090


async def handle_echo(reader, writer):
    global connected_users		
    username = await reader.read(100)
    if username.decode() in users.keys():      
        password = users[username.decode()]
        writer.write('ask_password'.encode())			
        userpassword = await reader.read(1024)	
        if userpassword.decode() == password:		
            writer.write('valid'.encode())		 
            print(f'{username.decode()} присоединился к чату')		
            connected_users.append(writer)		
            while True:		
                msg = await reader.read(1024)	
                if msg.decode() == 'exit':		
                    print(f'{username.decode()} покинул чат')		
                    leftmsg = f'{username.decode()} покинул чат.'		
                    for user in connected_users:	
                        if user != writer:	
                            user.write(leftmsg.encode())
                    connected_users.remove(writer)
                    break
                msg = f'[{username.decode()}]: ' + msg.decode() + '\n '
                for user in connected_users:
                    if user != writer:
                        user.write(msg.encode())
                        
        else:
            writer.write('invalid'.encode())		
            writer.close()
    else:
        writer.write('registration'.encode())		
        password = await reader.read(1024)
        users.update({username.decode():password.decode()})
        with open(users_file,'wb') as f:
            pickle.dump(users,f)
        writer.write('completed'.encode())
        writer.close()

if os.path.exists(users_file):        
    with open(users_file,'rb') as f:
        users = pickle.load(f)
else:
    users = {}


loop = asyncio.get_event_loop()
coro = asyncio.start_server(handle_echo, HOST, PORT, loop=loop)
server = loop.run_until_complete(coro)

print('Serving on {}'.format(server.sockets[0].getsockname()))		
try:
    loop.run_forever()
except KeyboardInterrupt:
    pass

server.close()
loop.run_until_complete(server.wait_closed())
loop.close()
