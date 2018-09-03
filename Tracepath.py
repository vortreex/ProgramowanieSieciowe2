import socket
import sys
Timeout = 1
Port = 50000
TTL = 1
TTLlimit = 30


AddressPort = (socket.getaddrinfo(sys.argv[1], None)[0][4][0], Port)
try:
    SocketTx = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    SocketRx = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
except socket.error as sckterr:
    print('Utworzenie gniazd nie powiodlo sie: ' + str(sckterr))
    exit()

try:
    SocketRx.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
except socket.error as opterr:
    print('Nie udalo sie ustawic opcji gniazd: ' + str(opterr))
try:
    SocketRx.bind((str(socket.INADDR_ANY), Port))
except socket.error as binderr:
    print('Nie udalo sie powiazac adresu i portu do gniazda: ' + str(binderr))
SocketRx.settimeout(1)

while True:
    SocketTx.setsockopt(socket.SOL_IP, socket.IP_TTL, TTL)
    NoReply = ''
    for PacketsSend in range(3):
        SocketTx.sendto(bytes('01010101', 'utf-8'), AddressPort)
        try:
            Reply = SocketRx.recvmsg(1024)
            Info = socket.gethostbyaddr((Reply[3][0]))
            print(str(TTL) + ': ' + Info[0] + '/' + Info[2][0])
        except socket.timeout:
            NoReply += ' *'
        except socket.herror as err:
            print(str(TTL) + ': ' + Reply[3][0])
        finally:
            if not NoReply:
                break
            if PacketsSend == 2:
                print(str(TTL) + ': ' + NoReply)

    TTL += 1
    if TTL > TTLlimit:
        break

try:
    SocketTx.close()
    SocketRx.close()
except socket.error as err:
    print('Zamkniecie gniazd nie powiodlo sie: ' + str(err))

exit()
