import websocket

# websocket.enableTrace(True)
# ws = websocket.create_connection("ws://127.0.0.1:5000/echo")
ws = websocket.create_connection("ws://localhost:8002/")

while True:
    original_text_to_send = input("") + '\n'
    if(original_text_to_send == "exit\n"):
        ws.close()
        break
    else:
        ws.send(original_text_to_send)
        result = ws.recv()
        print(result)


# ws.send("ls\n")
# print("Sent")
# print("Receiving...")
# result = ws.recv()
# print("Received", result)
# ws.close()

# import docker
# client = docker.APIClient()

# container = 'b8dd765b750e5b930b7fa3c97394230c626679ca7a425607630579963fc45c6d'

# exec_id = client.exec_create(container=container, cmd='/bin/sh', tty=True, stdin=True)['Id']
# terminal_socket = client.exec_start(exec_id=exec_id, tty=True, socket=True)._sock

# print(terminal_socket)

# terminal_socket.send(b"ls\n")

# while 1:
#     data = terminal_socket.recv(16384)
#     if not data: 
#         break
#     print(data.decode('utf8'))

# terminal_socket.send(bytes('ls\n', encoding='utf-8'))
# dockerStreamStdout = terminal_socket.recv(2048)

# print(dockerStreamStdout.decode())
