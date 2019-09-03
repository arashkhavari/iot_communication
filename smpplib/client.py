"""SMPP client module"""

import socket
import select
import struct
import logging
import os.path
import binascii
from . import smpp
from . import exceptions
from . import consts
import pymysql.cursors
import codecs
import re
from time import localtime , strftime
from datetime import datetime


logger = logging.getLogger('smpplib.client')

class SimpleSequenceGenerator(object):

    MIN_SEQUENCE = 0x00000001
    MAX_SEQUENCE = 0x7FFFFFFF

    def __init__(self):
        self._sequence = self.MIN_SEQUENCE

    @property
    def sequence(self):
        return self._sequence

    def next_sequence(self):
        if self._sequence == self.MAX_SEQUENCE:
            self._sequence = self.MIN_SEQUENCE
        else:
            self._sequence += 1
        return self._sequence

class Client(object):
    """SMPP client class"""

    state = consts.SMPP_CLIENT_STATE_CLOSED

    host = None
    port = None
    vendor = None
    _socket = None
    sequence_generator = None

    def __init__(self, host, port, timeout=5, sequence_generator=None):
        """Initialize"""

        self.host = host
        self.port = int(port)
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.settimeout(timeout)
        self.receiver_mode = False
        if sequence_generator is None:
            sequence_generator = SimpleSequenceGenerator()
        self.sequence_generator = sequence_generator

    def __del__(self):
        """Disconnect when client object is destroyed"""
        if self._socket is not None:
            try:
                self.unbind()
            except (exceptions.PDUError, exceptions.ConnectionError) as e:
                if len(getattr(e, 'args', tuple())) > 1:
                    logger.warning('(%d) %s. Ignored', e.args[1], e.args[0])
                else:
                    logger.warning('%s. Ignored', e)
            self.disconnect()

    @property
    def sequence(self):
        return self.sequence_generator.sequence

    def next_sequence(self):
        return self.sequence_generator.next_sequence()

    def connect(self):
        """Connect to SMSC"""

        logger.info('Connecting to %s:%s...', self.host, self.port)

        try:
            if self._socket is None:
                self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._socket.connect((self.host, self.port))
            self.state = consts.SMPP_CLIENT_STATE_OPEN
        except socket.error:
            raise exceptions.ConnectionError("Connection refused")

    def disconnect(self):
        """Disconnect from the SMSC"""
        logger.info('Disconnecting...')

        if self._socket is not None:
            self._socket.close()
            self._socket = None
        self.state = consts.SMPP_CLIENT_STATE_CLOSED

    def _bind(self, command_name, **kwargs):
        """Send bind_transmitter command to the SMSC"""

        if command_name in ('bind_receiver', 'bind_transceiver'):
            logger.debug('Receiver mode')
            self.receiver_mode = True

        #smppinst = smpp.get_instance()
        p = smpp.make_pdu(command_name, client=self, **kwargs)

        self.send_pdu(p)
        try:
            resp = self.read_pdu()
        except socket.timeout:
            raise exceptions.ConnectionError()
        if resp.is_error():
            raise exceptions.PDUError(
                '({}) {}: {}'.format(resp.status, resp.command,
                consts.DESCRIPTIONS.get(resp.status, 'Unknown code')), int(resp.status))
        return resp

    def bind_transmitter(self, **kwargs):
        """Bind as a transmitter"""
        return self._bind('bind_transmitter', **kwargs)

    def bind_receiver(self, **kwargs):
        """Bind as a receiver"""
        return self._bind('bind_receiver', **kwargs)

    def bind_transceiver(self, **kwargs):
        """Bind as a transmitter and receiver at once"""
        return self._bind('bind_transceiver', **kwargs)

    def unbind(self):
        """Unbind from the SMSC"""

        p = smpp.make_pdu('unbind', client=self)

        self.send_pdu(p)
        try:
            return self.read_pdu()
        except socket.timeout:
            raise exceptions.ConnectionError()

    def send_pdu(self, p):
        """Send PDU to the SMSC"""

        if not self.state in consts.COMMAND_STATES[p.command]:
            raise exceptions.PDUError("Command %s failed: %s" %
                (p.command, consts.DESCRIPTIONS[consts.SMPP_ESME_RINVBNDSTS]))

        logger.debug('Sending %s PDU', p.command)

        generated = p.generate()

        logger.debug('>>%s (%d bytes)', binascii.b2a_hex(generated),
            len(generated))

        sent = 0

        while sent < len(generated):
            sent_last = 0
            try:
                sent_last = self._socket.send(generated[sent:])
            except socket.error as e:
                logger.warning(e)
                raise exceptions.ConnectionError()
            if sent_last == 0:
                raise exceptions.ConnectionError()
            sent += sent_last

        return True

    def read_pdu(self):
        """Read PDU from the SMSC"""
        logger.debug('Waiting for PDU...')

        try:
            raw_len = self._socket.recv(4)
        except socket.timeout:
            raise
        except socket.error as e:
            logger.warning(e)
            raise exceptions.ConnectionError()
        if not raw_len:
            raise exceptions.ConnectionError()

        try:
            length = struct.unpack('>L', raw_len)[0]
        except struct.error:
            logger.warning('Receive broken pdu... %s', repr(raw_len))
            raise exceptions.PDUError('Broken PDU')

        raw_pdu = self._socket.recv(length - 4)
        raw_pdu = raw_len + raw_pdu
        print(raw_pdu)
        print(raw_len, '\n')
        if 400 > len(raw_pdu) > 200 :
            print('200')
            #for decode
            #print('1', raw_pdu)
            #decode_hex = codecs.getdecoder("hex_codec")
            _string = str(raw_pdu)
            print(_string)
            #print('2', _string)
            #_string = str(decode_hex(_string))
            #print('3', _string)
            #for get data
            y = str(re.findall(r'[#T]\S*', _string)).split(':')[1].split(',')[0:11]
            print(y)
            #y = y[0]+','+y[1]+','+y[2]+','+y[3]+','+y[4]+','+y[5]+','+y[6]+','+y[7]+','+y[8]+','+y[9]+','+y[10]
            #for get shortcode and Thuraya phone
            z = str(re.findall(r'[88]\S*', _string)).split('\\')[0:10]
            print(z)
            x = z[0].split('"')[1]
            print(x)
            m = z[6]
            print(m)
            m = re.findall( r'[88]\d{8}',m)[0]
            print(m)
            current_time = strftime("%Y-%m-%d %H:%M:%S", localtime())
            #print(current_time)
            #current_time=str(current_time)
            #result
            #cl =','
            #b =y+cl+x+cl+m
            #b=b.split(',')
            #print(b)
            b0=y[0]
            b1=y[1]
            b2=y[2]
            b3=y[3]
            b4=y[4]
            b5=y[5]
            b6=y[6]
            b7=y[7]
            b8=y[8]
            b9=y[9]
            b10=y[10]
            b11=x
            b12=m
            #print('4', b)
            #print(b[4])
            #_lat=int(b[6]) * 0.000001
            #print('5', _lat)
            #_lon=int(b[5]) * 0.000001
            #print('6', _lon)
            _devdate=datetime.strptime(b4, '%Y%m%d%H%M%S').strftime('%Y-%m-%d %H:%M:%S')
            #print(_devdate)
            #_devdate= str(_devdate)
            connection = pymysql.connect(host='localhost',user='root',password='!QAZ1qaz1qaz',db='t2m',charset='utf8',cursorclass=pymysql.cursors.DictCursor,autocommit=True)
            print('connect to DB')
            _cursor = connection.cursor()
            print('cusor is ok')
            sql = "INSERT INTO `parsing`(`unit`, `carrier`, `param2`, `param3`, `adate`, `lon`, `lat`, `speed`, `param5`, `param6`, `param7`, `devSIM`, `shortcode`, `currentTime`, `astatus`) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
            _cursor.execute(sql, [b0,b1,b2,b3,_devdate,b6,b5,b7,b8,b9,b10,b11,b12,current_time,'input'])
            print('query is send')
        elif 170 > len(raw_pdu) > 140 :
            print('100')
            #for decode
            #print('1', raw_pdu)
            #decode_hex = codecs.getdecoder("hex_codec")
            _string = str(raw_pdu)
            print(_string)
            #print('2', _string)
            #_string = str(decode_hex(_string))
            #print('3', _string)
            #for get data
            y = str(re.findall(r'[#T]\S*', _string)).split(':')[1].split(',')[0:11]
            print(y)
            #y = y[0]+','+y[1]+','+y[2]+','+y[3]+','+y[4]+','+y[5]+','+y[6]+','+y[7]+','+y[8]+','+y[9]+','+y[10]
            #for get shortcode and Thuraya phone
            z = str(re.findall(r'[88]\S*', _string)).split('\\')[0:10]
            print(z)
            x = z[0].split('"')[1]
            print(x)
            m = z[6]
            print(m)
            m = re.findall( r'[88]\d{8}',m)[0]
            print(m)
            current_time = strftime("%Y-%m-%d %H:%M:%S", localtime())
            #print(current_time)
            #current_time=str(current_time)
            #result
            #cl =','
            #b =y+cl+x+cl+m
            #b=b.split(',')
            #print(b)
            b0=y[0]
            b1=y[1]
            b2=y[2]
            b3=y[3]
            b4=y[4]
            b5=y[5]
            b6=y[6]
            b7=y[7]
            b8=y[8]
            b9=y[9]
            b10=y[10]
            b11=x
            b12=m
            #print('4', b)
            #print(b[4])
            #_lat=int(b[6]) * 0.000001
            #print('5', _lat)
            #_lon=int(b[5]) * 0.000001
            #print('6', _lon)
            _devdate=datetime.strptime(b3, '%Y%m%d%H%M%S').strftime('%Y-%m-%d %H:%M:%S')
            #print(_devdate)
            #_devdate= str(_devdate)
            connection = pymysql.connect(host='localhost',user='root',password='!QAZ1qaz1qaz',db='t2m',charset='utf8',cursorclass=pymysql.cursors.DictCursor,autocommit=True)
            print('connect to DB')
            _cursor = connection.cursor()
            print('cusor is ok')
            sql = "INSERT INTO `parsing`(`unit`, `carrier`, `param2`, `param3`, `adate`, `lon`, `lat`, `speed`, `param5`, `param6`, `param7`, `devSIM`, `shortcode`, `currentTime`, `astatus`) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
            _cursor.execute(sql, [b0,b1,b2,b3,_devdate,b4,b5,b6,b8,b9,b7,b11,b12,current_time,'input'])
            print('query is send')

        else:
            print(raw_pdu)
        logger.debug('<<%s (%d bytes)', binascii.b2a_hex(raw_pdu), len(raw_pdu))

        p = smpp.parse_pdu(raw_pdu, client=self)

        logger.debug('Read %s PDU', p.command)

        if p.is_error():
            return p

        elif p.command in consts.STATE_SETTERS:
            self.state = consts.STATE_SETTERS[p.command]

        return p

    def accept(self, obj):
        """Accept an object"""
        raise NotImplementedError('not implemented')

    def _message_received(self, p):
        """Handler for received message event"""
        status = self.message_received_handler(pdu=p)
        if status is None:
            status = consts.SMPP_ESME_ROK
        dsmr = smpp.make_pdu('deliver_sm_resp', client=self, status=status)
        #, message_id=args['pdu'].sm_default_msg_id)
        dsmr.sequence = p.sequence
        self.send_pdu(dsmr)

    def _enquire_link_received(self):
        """Response to enquire_link"""
        ler = smpp.make_pdu('enquire_link_resp', client=self)
        #, message_id=args['pdu'].sm_default_msg_id)
        self.send_pdu(ler)
        logger.debug("Link Enquiry...")

    def _alert_notification(self, p):
        """Handler for alert notifiction event"""
        self.message_received_handler(pdu=p)

    def set_message_received_handler(self, func):
        """Set new function to handle message receive event"""
        self.message_received_handler = func

    def set_message_sent_handler(self, func):
        """Set new function to handle message sent event"""
        self.message_sent_handler = func

    @staticmethod
    def message_received_handler(pdu, **kwargs):
        """Custom handler to process received message. May be overridden"""

        logger.warning('Message received handler (Override me)')

    @staticmethod
    def message_sent_handler(pdu, **kwargs):
        """Called when SMPP server accept message (SUBMIT_SM_RESP).
        May be overridden"""
        logger.warning('Message sent handler (Override me)')


    def read_once(self, ignore_error_codes=None):
        """Read a PDU and act"""
        try:
            try:
                p = self.read_pdu()
            except socket.timeout:
                logger.debug('Socket timeout, listening again')
                p = smpp.make_pdu('enquire_link', client=self)
                self.send_pdu(p)
                return

            if p.is_error():
                raise exceptions.PDUError(
                    '({}) {}: {}'.format(p.status, p.command,
                    consts.DESCRIPTIONS.get(p.status, 'Unknown status')), int(p.status))

            if p.command == 'unbind':  # unbind_res
                logger.info('Unbind command received')
                return
            elif p.command == 'submit_sm_resp':
                self.message_sent_handler(pdu=p)
            elif p.command == 'deliver_sm':
                self._message_received(p)
            elif p.command == 'enquire_link':
                self._enquire_link_received()
            elif p.command == 'enquire_link_resp':
                pass
            elif p.command == 'alert_notification':
                self._alert_notification(p)
            else:
                logger.warning('Unhandled SMPP command "%s"', p.command)
        except exceptions.PDUError as e:
            if ignore_error_codes \
                    and len(e.args) > 1 \
                    and e.args[1] in ignore_error_codes:
                logging.warning('(%d) %s. Ignored.' %
                    (e.args[1], e.args[0]))
            else:
                raise

    def poll(self, ignore_error_codes=None):
        '''Act on available PDUs and return'''
        while True:
            readable, writable, exceptional = select.select([self._socket], [], [], 0)
            if not readable:
                break
            self.read_once(ignore_error_codes)

    def listen(self, ignore_error_codes=None):
        """Listen for PDUs and act"""
        while True:
            self.read_once(ignore_error_codes)

    def send_message(self, **kwargs):
        """Send message
        Required Arguments:
            source_addr_ton -- Source address TON
            source_addr -- Source address (string)
            dest_addr_ton -- Destination address TON
            destination_addr -- Destination address (string)
            short_message -- Message text (string)
        """

        ssm = smpp.make_pdu('submit_sm', client=self, **kwargs)
        self.send_pdu(ssm)
        return ssm
