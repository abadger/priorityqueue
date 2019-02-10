#!/usr/bin/python3
# Copyright: (c) 2019, Toshio Kuratomi <a.badger@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

import random
import timeit
from collections import defaultdict
from itertools import islice

import pytest

import dictionary1
import dictionary2
import dictionary3
import dictionary4
import dictionary5
import dictionary6
import dictionary7
import heapqdict
import heapq1
import priorityqueue


# The highest priority to select from (also, the opposite of this is the lowest).
# This is only the potential priorities.  Each entry is selected randomly from this list.
# The more priorities, the less efficient the dictionary-based priority-queues
PRIORITY_MAXIMA = 2**10

# Number of entries into the queue
LARGE_DATASET_LEN = 2**12

# The number of entries that are added to the queue before the entire queue is processed
# If LARGE_DATASET_LEN is larger than this, the queue will be emptied and refilled until
# the entire dataset has been processed.
CHUNKSIZE = LARGE_DATASET_LEN

# Store some junk data in addition to the priority queue's record keeping to be a tad more realistic
DATASIZE = 2**10
DATA = 'a' * DATASIZE

# Data to use when chcking for correctness.  This should include repeated priorities to check for
# insertion order, None and 0 (which the queue should store at the same priority), positive and
# negative priorities, and addition of priorities in both sorted and unsorted order.
DATASET = (
           (80, DATA + '8'),
           (-10, DATA + '1'),
           (None, DATA + '3'),
           (0, DATA + '4'),
           (None, DATA + '5'),
           (10, DATA + '6'),
           (100, DATA + '9'),
           (50, DATA + '7'),
           (-20, DATA + '0'),
           (-10, DATA + '2'),
          )

pytestmark = pytest.mark.usefixtures("create_large_dataset")


@pytest.fixture(scope="module")
def create_large_dataset():
    """
    Populate a large list of data to enter into the queue

    The data has randomized priorities controlled by the constants defined above.
    The data will only be generated once per pytest run so that all the tests in this module will
    get the same dataset.
    """
    global _large_dataset
    priority_values = list(range(-PRIORITY_MAXIMA, PRIORITY_MAXIMA))
    _large_dataset = []
    for seq in range(0, LARGE_DATASET_LEN):
        priority = random.choice(priority_values)
        if priority == 0:
            priority = None
        _large_dataset.append((priority, f'{DATA}:{priority}:{seq}'))


@pytest.fixture
def timingfile():
    """Log the timings of the tests to the file pq-timings.log"""
    with open('pq-timings.log', 'a') as f:
        yield f


def chunk(dataset, chunksize):
    """Return chunks of the data at a time"""
    iterator = iter(dataset)
    def _next_chunk():
        return tuple(islice(iterator, chunksize))
    return iter(_next_chunk, tuple())


def check_priority_queue(QueueClass, dataset):
    queue = QueueClass()
    for priority, value in dataset:
        if priority is None:
            queue.push(value)
        else:
            queue.push(value, priority=priority)

    sorted_data = []
    while queue:
        sorted_data.append(queue.pop())

    for idx, value in enumerate(sorted_data):
        assert value.endswith(f'{idx}')


def run_priority_queue(QueueClass, dataset):
    queue = QueueClass()
    for somedata in chunk(dataset, CHUNKSIZE):
        for priority, value in somedata:
            if priority is None:
                queue.push(value)
            else:
                queue.push(value, priority=priority)

        sorted_data = defaultdict(list)
        prev_priority = -100000
        while queue:
            data = queue.pop()
            dummy, priority, seq = data.split(':')
            if priority == 'None':
                priority = 0
            priority = int(priority)
            seq = int(seq)
            assert priority >= prev_priority
            prev_priority = priority

            sorted_data[priority].append(seq)

    for insertion_order in sorted_data.values():
        assert sorted(insertion_order) == insertion_order


@pytest.mark.parametrize('QueueClass', [priorityqueue.PriorityQueue,
                                        heapq1.PriorityQueue,
                                        heapqdict.PriorityQueue,
                                        dictionary1.PriorityQueue,
                                        dictionary2.PriorityQueue,
                                        dictionary3.PriorityQueue,
                                        dictionary4.PriorityQueue,
                                        dictionary5.PriorityQueue,
                                        dictionary6.PriorityQueue,
                                        dictionary7.PriorityQueue,
                                        ])
def test_priority_queue_correctness(QueueClass, timingfile):
    import test_priority_queues
    test_priority_queues.QueueClass = QueueClass

    timer = timeit.Timer('check_priority_queue(QueueClass, DATASET)', setup='from test_priority_queues import QueueClass, DATASET, check_priority_queue')
    timing = timer.repeat(repeat=3, number=100000)

    timingfile.write(f'{QueueClass}: {timing}\n')


@pytest.mark.parametrize('QueueClass', [priorityqueue.PriorityQueue,
                                        heapq1.PriorityQueue,
                                        heapqdict.PriorityQueue,
                                        dictionary1.PriorityQueue,
                                        dictionary2.PriorityQueue,
                                        dictionary3.PriorityQueue,
                                        dictionary4.PriorityQueue,
                                        dictionary5.PriorityQueue,
                                        dictionary6.PriorityQueue,
                                        dictionary7.PriorityQueue,
                                        ])
def test_priority_queue_speed(QueueClass, timingfile):
    import test_priority_queues
    test_priority_queues.QueueClass = QueueClass

    timer = timeit.Timer('run_priority_queue(QueueClass, _large_dataset)', setup='from test_priority_queues import QueueClass, _large_dataset, run_priority_queue')
    timing = timer.repeat(repeat=3, number=10)

    timingfile.write(f'{QueueClass}: {timing}\n')
