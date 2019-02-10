# Copyright: (c) 2019, Toshio Kuratomi <a.badger@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
import heapq

class PriorityQueue:
    def __init__(self):
        self.store = []
        self.seq = 0

    def push(self, value, priority=None):
        if priority is None:
            priority = 0
        heapq.heappush(self.store, (priority, self.seq, value))
        self.seq += 1

    def pop(self):
        return heapq.heappop(self.store)[-1]

    def __len__(self):
        return len(self.store)

    def __bool__(self):
        return True if self.store else False
