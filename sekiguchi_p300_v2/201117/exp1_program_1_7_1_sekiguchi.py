import random
import ctypes
from psychopy import visual, monitors, event, core
import serial
import time
import pickle

class exp1:
    def __init__(self, target_word, port_name):
        print('data loading...')
        self.target = target_word
        self.ser = serial.Serial(port_name, 1200, bytesize=serial.FIVEBITS, timeout=0, write_timeout=0)  # デバイス名とボーレートを設定しポートをオープン
        self.light_data = []
        self.marker_data = 0
        self.img = []

        self.timer = core.MonotonicClock()
        self.time_list = []

        import warnings
        warnings.simplefilter('ignore')

        import psutil
        p = psutil.Process()
        p.nice(psutil.REALTIME_PRIORITY_CLASS)
        del p

        fullscr_size=(ctypes.windll.user32.GetSystemMetrics(0), ctypes.windll.user32.GetSystemMetrics(1))
        mon = monitors.Monitor('screen')
        self.win = visual.Window(size=fullscr_size, fullscr=True, monitor=mon, winType='pyglet')
        event.Mouse(visible=False, newPos=None, win=None)
        core.checkPygletDuringWait = False

        self.exp_explain = visual.ImageStim(self.win, image='P300-Speller_exp/P300-Speller_image/exp_start_image/origin_image/exp_explain.png')
        self.start_1 = visual.ImageStim(self.win, image='P300-Speller_exp/P300-Speller_image/exp_start_image/origin_image/exp_start_count1.png')
        self.start_2 = visual.ImageStim(self.win, image='P300-Speller_exp/P300-Speller_image/exp_start_image/origin_image/exp_start_count2.png')
        self.start_3 = visual.ImageStim(self.win, image='P300-Speller_exp/P300-Speller_image/exp_start_image/origin_image/exp_start_count3.png')
        self.img0 = visual.ImageStim(self.win, image='P300-Speller_exp/P300-Speller_image/P300Speller_ver1.0/exp1_image0.png')

        for i in range(1,13):
            self.img.append(visual.ImageStim(self.win, image='P300-Speller_exp/P300-Speller_image/P300Speller_ver1.0/exp1_image'+str(i)+'.png'))
        r = random.randint(0,99)
        with open("P300-Speller_exp/P300-Speller_image/P300Speller_image_show_list_v1/exp_img_random_show"+str(r), 'rb') as f:
            self.light_list = pickle.load(f)
        self.light_count = len(self.light_list)
        print('load finished')

    def send_marker(self, marker):
        self.ser.write(bytes([marker]))

    def img_show(self, image, marker= 255, wait_sec=1):
        image.draw()
        self.win.flip(False)
        if not marker == 255:
            self.send_marker(marker)
        core.wait(wait_sec, wait_sec)

    def start_exp(self):
        self.img_show(self.exp_explain, wait_sec=2)
        self.img_show(self.start_3)
        self.img_show(self.start_2)
        self.img_show(self.start_1)
        self.img_show(self.img0)

        # begin_time = time.perf_counter()
        for i in range(self.light_count):
            random_num = self.light_list[i]
            self.time_list.append(self.timer.getTime())
            self.img_show(self.img[random_num], random_num, 11/60 - 0.00377777777777777777777777777777)               # 175ミリ秒間表示
            self.time_list.append(self.timer.getTime())
            self.img_show(self.img0, marker=255, wait_sec=11/60 - 0.00377777777777777777777777777777)                 # 175ミリ秒間非刺激時間表示
        
        # end_time = time.perf_counter()
        # print(str(end_time - begin_time) + "s")
        import numpy as np
        self.time_list = np.diff(np.array(self.time_list)).tolist()
        print("平均間隔", round(sum(self.time_list) / len(self.time_list), 4), 's')
        print("min", round(min(self.time_list), 4), 's')
        print('max', round(max(self.time_list), 4), 's')

        self.ser.close()
        print('finish!!')

if __name__ == '__main__':
    exp = exp1('R', 'COM5')
    exp.start_exp()
