"""
Run speedtest at a certain interval
"""

import sys
import time

import pyspeedtest
import pandas as pd
import matplotlib.pyplot as plt


class Tester(object):
    def __init__(self, interval, fname):
        self.interval = interval # [s]
        self.fname = fname

        print('[Saving to "{}" every {} seconds]'.format(self.fname, self.interval))

    def _get_dw(self):
        try:
            return pyspeedtest.SpeedTest().download()
        except:
            return -1

    def _store_dw(self, val):
        ts = pd.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.fname, 'a') as fd:
            fd.write('{},{}\n'.format(ts, val))

    def _do_action(self):
        cur_dw = self._get_dw()
        self._store_dw(cur_dw)
        return cur_dw

    def run(self):
        while True:
            start = time.time()
            val = self._do_action()
            dur = time.time() - start
            time.sleep(max(self.interval - dur, 0))

def plot(fname):
    df = pd.read_csv(fname, header=None, names=('timestamp', 'rate'))
    df.timestamp = pd.to_datetime(df.timestamp)

    df.rate /= 1e6
    df.plot(x='timestamp', y='rate')

    plt.title('Mbit/s')
    plt.show()

def main():
    if len(sys.argv) == 1:
        t = Tester(60*60, 'log.csv')
        t.run()
    else:
        plot(sys.argv[1])

if __name__ == '__main__':
    main()
