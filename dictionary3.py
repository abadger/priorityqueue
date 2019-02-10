# Copyright: (c) 2019, Toshio Kuratomi <a.badger@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
import heapq
from collections import defaultdict, deque

class PriorityQueue:
    def __init__(self):
        self.store = defaultdict(deque)
        self.priorities = []

    def push(self, value, priority=None):
        if priority is None:
            priority = 0
        self.store[priority].append(value)
        heapq.heappush(self.priorities, priority)

    def pop(self):
        priority = heapq.heappop(self.priorities)
        value = self.store[priority].popleft()
        if not self.store[priority]:
            del self.store[priority]
        return value

    def __len__(self):
        return len(self.store)

    def __bool__(self):
        return True if self.priorities else False
