#!/usr/bin/env python3

import sys
import socket
import ctypes
import logging

class PacketDHCP(ctypes.LittleEndianStructure):
    _fields_ = [
        ('op', ctypes.c_ubyte),
        ('htype', ctypes.c_ubyte),
        ('hlen', ctypes.c_ubyte),
        ('hops', ctypes.c_ubyte),
        
        ('xid', ctypes.c_uint32, 32),

        ('secs', ctypes.c_ushort),
        ('flags', ctypes.c_ushort),
        
        # ip-адрес клиента
        ('ciaddr', ctypes.c_uint32, 32),
        ('yiaddr', ctypes.c_uint32, 32),
        ('siaddr', ctypes.c_uint32, 32),
        ('giaddr', ctypes.c_uint32, 32),

        ('chaddr', ctypes.c_ubyte * 16),
        ('sname', ctypes.c_ubyte * 64),
        ('file', ctypes.c_ubyte * 128),

        ('options', ctypes.c_ubyte * 128),
    ]




class DiscoverDHCP(PacketDHCP):
    """Обнаружение DHCP.
    """
    pass


class OfferDHCP(PacketDHCP):
    """Предложение
    """
    pass


class RequestDHCP(PacketDHCP):
    """Запрос DHCP
    """
    pass


class PackDHCP(PacketDHCP):
    """Подтверждение DHCP
    """
    pass


# определяем тип пакета и его возвращает его
class MakerRecivePacket:

    DISCOVER_PACKET_TYPE = 0x2
    OFFER_PACKET_TYPE = 0x4
    

    def make(data_buff):

        dhcp_packet_undefined = PacketDHCP.from_buffer_copy(data_buff)

        # если адрес клиента равен нулю, то осуществляется запрос адреса
        if dhcp_packet_undefined.field.ciaddr == 0:
            return DiscoverDHCP.from_buffer_copy(data_buff), self.DISCOVER_PACKET_TYPE
        else:
            return RequestDHCP.from_buffer_copy(data_buff), self.OFFER_PACKET_TYPE



class Application:
    """Главный класс приложения
    """
    _DHCP_DEFAULT_SERVER_PORT = 67
    _DHCP_DEFAULT_CLIENT_PORT = 68

    _DHCP_PACKET_SIZE = ctypes.sizeof(PacketDHCP)


    def __init__(self, *, ip_adress='0.0.0.0'):
        self._IP_ADDRESS = ip_adress

        self._maker_packet = MakerRecivePacket()

        logging.debug('Start simple DHCP server!')


    def _socket_init(self):

        try:
            self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
            self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self._sock.bind((self._IP_ADDRESS, self._DHCP_DEFAULT_SERVER_PORT))

            logging.debug('Host = {0}'.format(self._IP_ADDRESS))
        except PermissionError as e:
            logging.error("Permission denied")
            return False
        else:
            return True

    def run(self):
        
        if self._socket_init() is False:
            self._exit()
        
        while True:
            buffer = self._sock.recv(self._DHCP_PACKET_SIZE)
            
            packet, packet_type = self._maker_packet.make(buffer)

            if MakerRecivePacket.DISCOVER_PACKET_TYPE == packet_type:
                pass
            elif MakerRecivePacket.OFFER_PACKET_TYPE == packet_type:
                pass



                #print(dhcp_packet)

        

    def _exit(self):
        logging.error("Exit")
        sys.exit(-1)


if __name__ == '__main__':

    logging.basicConfig(format='[%(asctime)s] [%(levelname)s] - %(message)s  ', level=logging.DEBUG, datefmt='%H:%M %d.%m.%y')

    app = Application()
    app.run()