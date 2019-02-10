# Copyright: (c) 2019, Toshio Kuratomi <a.badger@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
import heapq
from collections import deque

class PriorityQueue:
    def __init__(self):
        self.ordered_store = []
        self.lookup_store = {}

    def push(self, value, priority=None):
        if priority is None:
            priority = 0

        if priority not in self.lookup_store:
            store = deque()
            heapq.heappush(self.ordered_store, (priority, store))
            self.lookup_store[priority] = store
        self.lookup_store[priority].append(value)

    def pop(self):
        value = self.ordered_store[0][-1].popleft()

        if not self.ordered_store[0][-1]:
            del self.lookup_store[self.ordered_store[0][0]]
            heapq.heappop(self.ordered_store)

        return value

    def __len__(self):
        total_len = 0
        for value in self.lookup_store.values():
            total_len += len(value[-1])
        return total_len

    def __bool__(self):
        return True if self.ordered_store else False
