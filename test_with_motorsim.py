import caproto as ca
import socket


CA_REPEATER_PORT = 5065
CA_SERVER_PORT = 5064
pv1 = "XF:31IDA-OP{Tbl-Ax:X1}Mtr"


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
send_bcast = lambda msg: sock.sendto(bytes(msg), ('', CA_REPEATER_PORT))
recv_bcast = lambda: sock.recvfrom(4096)

# Send data
ip = socket.gethostbyname(socket.gethostname())
print('our ip', ip)
reg_command = ca.RepeaterRegisterRequest(ip)
print("Sending", reg_command)
send_bcast(bytes(reg_command))

# Receive response
print('waiting to receive')
data, address = recv_bcast()
print('received "%s"' % data)


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
send_bcast = lambda msg: sock.sendto(bytes(msg), ('', CA_SERVER_PORT))
recv_bcast = lambda: sock.recvfrom(4096)

 
cli = ca.Connections(our_role=ca.CLIENT)
chan1 = cli.new_channel(pv1)
bytes_to_send = cli.send_broadcast(ca.VersionRequest(0, 13))
bytes_to_send += cli.send_broadcast(ca.SearchRequest(pv1, 0, 13))
print('searching for %s' % pv1)
send_bcast(bytes_to_send)
bytes_received, address = recv_bcast()
cli.recv_broadcast(bytes_received, address)
command = cli.next_command()
print('received', command)
command = cli.next_command()
print('received', command)
