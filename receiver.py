import matplotlib.pyplot as plt
import numpy as np
from math import sqrt, erfc
import random
import pyvisa
import time

from main import Sender

if __name__ == '__main__':
    sender = Sender()
    send_signal = sender.main()
    print(send_signal)

    time.sleep(5)

    rm = pyvisa.ResourceManager()
    visa_list = rm.list_resources()
    print('Hello', visa_list)
    
    # オシロスコープの ID
    oci_id = 'USB0::0x0699::0x03C3::C030420::INSTR'
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
    inst.write('DAT:SOU CH1')
    res_ch1 = inst.query_binary_values('CURV?', datatype='b')
    print("CH1 受信信号点", len(res_ch1))

    # plt.plot(res_ch1)
    # plt.show()

    inst.write('DAT:SOU CH2')
    res_ch2 = inst.query_binary_values('CURV?', datatype='b')
    print("CH2 受信信号点", len(res_ch2))
    first_target_index = 0
    interval_index = 0
    last_target_index = 0
    for index in range(len(res_ch2)):
        if res_ch2[index] > 0:
            first_target_index = index
            break
    print('first_target_index', first_target_index)

    for index in range(first_target_index + 1, len(res_ch2)):
        if res_ch2[index] < 0:
            interval_index = index
            break
    for index in range(interval_index + 1, len(res_ch2)):
        if res_ch2[index] > 0:
            last_target_index = index
            break
    print('last_target_index', last_target_index)

    print('send_signal', len(send_signal))
    points = (last_target_index - first_target_index) // len(send_signal)
    plt.plot(res_ch1[first_target_index:last_target_index:points])
    plt.show()

    print(len(res_ch1[first_target_index:last_target_index:points]))
    res_signal = res_ch1[first_target_index:last_target_index:points]
    counts = len(res_signal)
    correct = 0
    for send, res in zip(send_signal, res_signal):
        tmp = 127 if res > 0 else 0
        if send == tmp:
            correct += 1
    print('correct', correct)
    print('BER', correct / counts * 100)
    plt.plot(send_signal, color='blue')
    plt.plot(res_signal, color='red')
    plt.show()

    # plt.plot(res_ch2)
    # plt.show()
    # plt.plot([i for i in range(len(res))])
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
    # print(res2, len(res2))

    inst.close()
