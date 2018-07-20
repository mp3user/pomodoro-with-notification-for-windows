import threading
import argparse
import itertools
from datetime import datetime, timedelta
from collections import namedtuple
from baloon import WindowsBalloonTip

NOW = datetime.now


class State(namedtuple('State', 'length activity')):
    def notify_start(self):
        self._notify(
                'Started. End time: {:%H:%M}'
                .format(NOW() + timedelta(minutes=self.length)))

    def notify_end(self):
        self._notify('Ended')

    def _notify(self, status):
        message = '[{:%H:%M}] {}'.format(NOW(), status)
        w = WindowsBalloonTip()
        w.ShowWindow(self.activity, message)        

def pomodoro_cycle(work_time, s_break_time, l_break_time):
    if None in (work_time, s_break_time, l_break_time):
        raise ValueError('No time provided')

    work = State(work_time, 'Work Period')
    s_break = State(s_break_time, 'Short Break')
    l_break = State(l_break_time, 'Long Break')

    cycle = itertools.chain(
            itertools.chain.from_iterable(
                itertools.repeat((work, s_break), 4)),
            (l_break,))

    milestone = timedelta(0)
    for activity in cycle:
        threading.Timer(milestone.total_seconds(),
                        activity.notify_start).start()
        milestone += timedelta(minutes=activity.length)
        last_task = threading.Timer(milestone.total_seconds(),
                                    activity.notify_end)
        last_task.start()
    last_task.join()


def main():
    parser = argparse.ArgumentParser('Pomodoro clock')
    parser.add_argument('--work_time', type=int, default=1)
    parser.add_argument('--short_break', type=int, default=1)
    parser.add_argument('--long_break', type=int, default=1)

    args = parser.parse_args()

    while True:
        pomodoro_cycle(args.work_time, args.short_break, args.long_break)

if __name__ == '__main__':
    main()