import socket
import sys
import time

AddressPort = (socket.getaddrinfo(sys.argv[1], None)[0][4][0], 50000)
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
    SocketRx.bind((str(socket.INADDR_ANY), 50000))
except socket.error as binderr:
    print('Nie udalo sie powiazac adresu i portu do gniazda: ' + str(binderr))
SocketRx.settimeout(3)

TTL = 1


while True:
    SocketTx.setsockopt(socket.SOL_IP, socket.IP_TTL, TTL)
    SocketTx.sendto(bytes(str(time.clock()), 'utf-8'), AddressPort)
    try:
        Reply = SocketRx.recvmsg(1024)
        Info = socket.gethostbyaddr((Reply[3][0]))
        print(time.clock())
        print(bytes(Reply[0]))
        print(str(TTL) + ': ' + Info[0] + '/' + Info[2][0])
    except socket.timeout:
        print(str(TTL) + ': ' + '*** No reply :( ***')
    except socket.herror as err:
        print(str(TTL) + ': ' + Reply[3][0])

    TTL += 1
    if TTL > 30:
        break

try:
    SocketTx.close()
    SocketRx.close()
except socket.error as err:
    print('Zamkniecie gniazd nie powiodlo sie: ' + str(err))

exit()
