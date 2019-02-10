# Copyright: (c) 2019, Toshio Kuratomi <a.badger@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from collections import defaultdict, deque

class PriorityQueue:
    def __init__(self):
        self.store = defaultdict(deque)

    def push(self, value, priority=None):
        if priority is None:
            priority = 0
        self.store[priority].append(value)

    def pop(self):
        priorities = sorted(self.store.keys())
        if not priorities:
            raise IndexError('Queue is empty')
        priority = priorities[0]
        value = self.store[priority].popleft()
        if not self.store[priority]:
            del self.store[priority]
        return value

    def __len__(self):
        return len(self.store)

    def __bool__(self):
        return True if self.store else False
