import socket
import struct
import time
import keyboard

#Due to a serious problem connecting and checking this in the ssh Server , this is our final code.
# we want to note that  We spent a lot of time and thinking in trying to make this code perfect, we did not succeed but we are proud of the outcome
#I believe it shuold be noted that one of the team mate is 7 month  pregnent ,and had some real pain during the early evening
#therefore only one teammate was able to work on the assignment for most of the time(email was sent to Yossi about it)
# thank you in advance

# --------------------waiting to connect------------stage 1
# initate the UDP SOCKET and starting to send broadcasts
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

port_for_udp=13117
ip_to_udp="0.0.0.0"
client.bind((ip_to_udp, port_for_udp))
print("Client started, listening for offer requests... ")
# --------------------succefully connected to server------------stage 2
print(" this is the client ip  :    " + str(socket.gethostname()))
flag = True
adrr = None
data = None
while flag:
    data, adrr = client.recvfrom(1024)
    if (len(data) == 8):
        data_after_unpack = struct.unpack("Ibh", data)
        print("this is data  " + str(data_after_unpack))
        port = data_after_unpack[2]
        if (int(data_after_unpack[0]) == 0xfeedbeef and int(data_after_unpack[1] == 0x2) and port == 2028):
            flag = False
            print(" going on to the next stage-playing game!")
            print(" this is good meassge received message: %s" % data_after_unpack[0])

# --------------------connect to tcp and playing------------stage 3

# defining the tcp socket for client
BUFFER_SIZE = 20
host = socket.gethostname()
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
if (adrr != None):
    s.connect((adrr[0], port))
group_num=1
#connection with the server
while True:
    try:
        s.sendall(str.encode('this team group number : '+str(group_num)+" \n"))
        data = (s.recv(1024))
        group_num += 1
        if data:
            print(data)
            print("Welcome to Keyboard Spamming Battle Royale\n Group "+str(group_num))
            x = time.time()
            char = ""
            print("press as many keys ass you can and then press enter")
            x = time.time()
            while x + 10 > time.time():
                key = keyboard.read_key()
                if key:
                    char+=key
            print(char)
            print("The number of keys you pressed " + str(len(char)))
            try:
                s.sendall(str.encode(char))
                s.sendall(str.encode(str(len(char))))
                if group_num==2:
                    s.sendall(str.encode("gameover"))

            except Exception :
                    print("server disconnected.......! ")
    except:
        print("try to connect to server again!")
        time.sleep(4)
s.close()





