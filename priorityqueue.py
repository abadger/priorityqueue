# Copyright: (c) 2019, Toshio Kuratomi <a.badger@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from queue import Empty, PriorityQueue as _PQ

class PriorityQueue:
    def __init__(self):
        self.store = _PQ()
        self.seq = 0

    def push(self, value, priority=None):
        if priority is None:
            priority = 0
        self.store.put((priority, self.seq, value))
        self.seq += 1

    def pop(self):
        try:
            return self.store.get(block=False)[-1]
        except Empty:
            raise IndexError('Queue is empty')

    def __len__(self):
        return self.store.qsize()

    def __bool__(self):
        return True if len(self) else False
