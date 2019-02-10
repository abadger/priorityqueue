# Copyright: (c) 2019, Toshio Kuratomi <a.badger@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
import heapq
from collections import defaultdict, deque

class PriorityQueue:
    def __init__(self):
        self.ordered_store = []
        self.lookup_store = defaultdict(deque)

    def push(self, value, priority=None):
        if priority is None:
            priority = 0

        if priority not in self.lookup_store:
            heapq.heappush(self.ordered_store, priority)

        self.lookup_store[priority].append(value)

    def pop(self):
        priority = self.ordered_store[0]
        value = self.lookup_store[priority].popleft()

        if not self.lookup_store[priority]:
            del self.lookup_store[priority]
            heapq.heappop(self.ordered_store)

        return value

    def __len__(self):
        total_len = 0
        for queue in self.lookup_store.values():
            total_len += len(queue)
        return total_len

    def __bool__(self):
        return True if self.ordered_store else False
