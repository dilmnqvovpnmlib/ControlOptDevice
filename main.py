import matplotlib.pyplot as plt
import numpy as np
from math import sqrt, erfc
import random
import pyvisa
import sys, codecs
import io


class Sender:
    def __init__(self):
        self.send_signal = []

    def main(self):
        self.create_signal()
        self.send()
        return self.send_signal

    def make_PRBS(self, initial_binary):
        initial = int(initial_binary, 2)
        tail = initial & 0b1
        initial = initial >> 1
        tmp = tail ^ (initial & 0b1)
        tmp = tmp << 14
        return bin(tmp + initial)[2:]

    def create_signal(self):
        signal = '0' * 112
        m = 50
        for _ in range(m):
            value = random.randrange(65535)
            binary = bin(value)
            prbs = self.make_PRBS(binary)
            signal += prbs
        self.send_signal = [np.uint8(int(i) * (2 ** 7 - 1)) for i in signal]
        return self.send_signal


    def send(self):
        rm = pyvisa.ResourceManager()
        visa_list = rm.list_resources()
        print('Hello', visa_list)
        
        # 波形生成器のアドレス
        oci_id = 'USB0::0x0699::0x0346::C033375::INSTR'
        if oci_id in visa_list:
            usb = oci_id
        else:
            print('Error.')
        inst = rm.open_resource(usb)
        print(usb, inst)

        # Read
        # inst.timeout = 250000000
        # values = inst.query_ascii_values('CURV?')
        # print(values)

        
        inst.timeout = 25000
        
        # print(inst.query('DATA:COPY EMEMory,USER1'))
        # inst.query('MMEMory:CATalog?')
        
        # 読み込んで書き出すから、タイムアウトを設定しておかないとタイムアウトする
        # res = inst.write('SOURce1:FREQuency:FIXed 700kHz')
        # # ? を付けると読み出しになる
        # res1 = inst.query('SOURce1:FREQuency:FIXed?')
        # print(res, res1)
        print('Hello')

        # データポイント数
        # # print(inst.query('DATA:POIN? EMEM'))

        # Read
        # res2 = inst.query_binary_values('DATA:DATA? EMEMory', datatype='H') # H
        # plt.plot([i for i in range(len(res2))], res2)
        # plt.show()

        # Write
        # print(send_signal)
        res2 = inst.write_binary_values('DATA:DATA EMEMory,', self.send_signal, datatype='h')
        print('res2', res2, 'send_signal length', len(self.send_signal))

        inst.close()

if __name__ == '__main__':
    signal = '0' * 1
    m = 50
    for _ in range(m):
        value = random.randrange(65535)
        binary = bin(value)
        prbs = makePRBS(binary)
        signal += prbs
    send_signal = [np.uint8(int(i) * (2 ** 7 - 1)) for i in signal]
    print(send_signal)

    rm = pyvisa.ResourceManager()
    visa_list = rm.list_resources()
    print('Hello', visa_list)
    
    # 波形生成器のアドレス
    oci_id = 'USB0::0x0699::0x0346::C033375::INSTR'
    if oci_id in visa_list:
        usb = oci_id
    else:
        print('Error.')
    inst = rm.open_resource(usb)
    print(usb, inst)

    # Read
    # inst.timeout = 250000000
    # values = inst.query_ascii_values('CURV?')
    # print(values)

    
    inst.timeout = 25000
    
    # print(inst.query('DATA:COPY EMEMory,USER1'))
    # inst.query('MMEMory:CATalog?')
    
    # 読み込んで書き出すから、タイムアウトを設定しておかないとタイムアウトする
    # res = inst.write('SOURce1:FREQuency:FIXed 700kHz')
    # # ? を付けると読み出しになる
    # res1 = inst.query('SOURce1:FREQuency:FIXed?')
    # print(res, res1)
    print('Hello')

    # データポイント数
    # # print(inst.query('DATA:POIN? EMEM'))

    # Read
    # res2 = inst.query_binary_values('DATA:DATA? EMEMory', datatype='H') # H
    # plt.plot([i for i in range(len(res2))], res2)
    # plt.show()

    # Write
    # print(send_signal)
    res2 = inst.write_binary_values('DATA:DATA EMEMory,', send_signal, datatype='h')
    print(res2)

    inst.close()
