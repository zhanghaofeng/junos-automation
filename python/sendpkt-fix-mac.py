
import socket, time, binascii, random

ETH_P_ALL = 3		# To receive all Ethernet protocols
Interface = "ens33"

### Packet field access ###
def randomSrcMAC():
	mac = [ 0x01, 0x01, 0x01,
		random.randint(0x00, 0x7f),
		random.randint(0x00, 0xff),
		random.randint(0x00, 0xff) ]
	src_mac = ''.join(map(lambda x: "%02x" % x, mac))
	return binascii.unhexlify(src_mac)
	
def randomDstMAC():
	mac = [ 0x02, 0x02, 0x02,
		random.randint(0x00, 0x7f),
		random.randint(0x00, 0xff),
		random.randint(0x00, 0xff) ]
	dst_mac = ''.join(map(lambda x: "%02x" % x, mac))
	return binascii.unhexlify(dst_mac)

# Open socket
sock = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(ETH_P_ALL))
sock.bind((Interface, ETH_P_ALL))
sock.setblocking(0)

while True:
	# Contents of packet to send (constant)
	src = randomSrcMAC()
	dst = randomDstMAC()
	
	'''
	for i in range(255):
		for j in range(255):
			hex_i = "%02x" % i
			hex_j = "%02x" % j
			mac = [ 0x01, 0x01, 0x01, 0x01, hex_i, hex_j ]
			srcmac = ''.join(map(lambda x: "%02x" % x, mac))
			src = binascii.unhexlify(srcmac)

			mac = [ 0x02, 0x02, 0x02, 0x02, i, j ]
			dstmac = ''.join(map(lambda x: "%02x" % x, mac))
			src = binascii.unhexlify(dstmac)

			
			i += 1
			j += 1
	'''		
	ip_ver = b'\x45'
	ip_dscp = b'\x00'
	ip_len = b'\x00\x2c'
	ip_id = b'\x11\x11'
	ip_flag = b'\x00\x00'
	ip_ttl = b'\x40'
	ip_proto = b'\x01'
	ip_chksum = b'\x63\xbb'
	ip_src = b'\xc0\xa8\x64\x05'
	ip_dst = b'\xc0\xa8\x64\x06'

	ip_header = ip_ver + ip_dscp + ip_len + ip_id + ip_flag + ip_ttl + ip_proto + ip_chksum + ip_src + ip_dst

	icmp_type = b'\x08'
	icmp_code = b'\x00'
	icmp_chksum = b'\xbe\xbe'
	icmp_id = b'\x00\x00'
	icmp_seq = b'\x01\x01'
	icmp_data = b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f'

	icmp_header = icmp_type + icmp_code + icmp_chksum + icmp_id + icmp_seq + icmp_data
		
	sendPacket = dst + src + b'\x08\x00' + ip_header + icmp_header

	sendBytes = sock.send(sendPacket)
	#print "Send packet with bytes, ", sendBytes
	time.sleep(0.000001)
