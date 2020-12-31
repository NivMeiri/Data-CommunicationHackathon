import random
import socket
import time
import struct
from _thread import *

#Due to a serious problem connecting and checking the project in the ssh Server , this is our final code.
# we want to note that  We spent a lot of time and thinking in trying to make this code perfect, we did not succeed but we are proud of the outcome
#I believe it shuold be noted that one of the team mates is 7 months  pregnent ,and had some real pain during the early evening
#therefore only one teammate was able to work on the assignment for most of the time (an email was sent to Yossi about it)
# thank you in advance


# ----------creating udp server-----------------
serverUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

# ---------------creating theServer socket for tcp
ServerSideSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
print("this is the host name: " + str(host))
OurPort = 2028

time_out_time=1
ThreadCount = 0
local_ip = socket.gethostbyname(host)
ServerSideSocket.bind(("", OurPort))
ServerSideSocket.listen(time_out_time)

# -------- starting to send meassages via udp
serverUDP.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
serverUDP.settimeout(time_out_time)
print("Server started, listening on IP address :" + str(local_ip))
message = struct.pack("I b h", 0xfeedbeef, 0X2, OurPort)
x = time.time()
while time.time() < x + 10:
    serverUDP.sendto(message, ('<broadcast>', 13117))
    print("message sent!")
    time.sleep(1)


# --------the function is excute thread for every client----------
def multi_threaded_client(connection):
    try:
        connection.send(str.encode('Server is working:'))
        while True:
            port_1=1024
            data = connection.recv(port_1)
            message = "this is message from server after tcp connection"
            answer = data.decode('utf-8')
            if not data:
                break
            print(answer)
            if(answer=="gameover"):
                calculate_result(2,1)
            connection.sendall(str.encode(message))
        connection.close()
    except:
        time.sleep(4)
        print("trying to connect to other clients")


x = time.time()
team1 = []
team2 = []
while True:
    print('\u001b[32m Server is listening..\u001b[0m')
    while time.time() < x + 10:
        Client, address = ServerSideSocket.accept()
        print('Connected to: ' + address[0] + ':' + str(address[1]))
        start_new_thread(multi_threaded_client, (Client,))
        ThreadCount += 1
        print('Thread Number: ' + str(ThreadCount))
ServerSideSocket.close()

# this function is responsible for the competion calculation
def playing_game(socket, team1, team2):
    if (len(team1) == len(team2)):
        x=random.randint(0, 1)
        if (x):
            team1.append(socket)
        else:
            team2.append(socket)
    if (len(team1) > len(team2)):
        team1.append(socket)
    else:
        team2.append(socket)


def  calculate_result(team1score,team2score):
    if(team1-team2>0):
        print("team1 won!")
    else:
        print("team 2 won")






