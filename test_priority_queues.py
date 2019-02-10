#!/usr/bin/python3
# Copyright: (c) 2019, Toshio Kuratomi <a.badger@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

import random
import timeit
from collections import defaultdict

import pytest

import dictionary1
import dictionary2
import dictionary3
import dictionary4
import heapqdict
import heapq1
import priorityqueue


LARGE_DATASET_LEN = 2**12
DATASIZE = 2**10
DATA = 'a' * DATASIZE
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
    global _large_dataset
    # The more priorities, the less efficient the dictionary-based priority-queues
    #priority_values = list(range(-2**10, 2**10))
    priority_values = list(range(-2**2, 2**2))
    _large_dataset = []
    for seq in range(0, LARGE_DATASET_LEN):
        priority = random.choice(priority_values)
        if priority == 0:
            priority = None
        _large_dataset.append((priority, f'{DATA}:{priority}:{seq}'))


@pytest.fixture
def timingfile():
    with open('pq-timings.log', 'a') as f:
        yield f


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
    for priority, value in dataset:
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
                                        ])
def test_priority_queue_speed(QueueClass, timingfile):
    import test_priority_queues
    test_priority_queues.QueueClass = QueueClass

    timer = timeit.Timer('run_priority_queue(QueueClass, _large_dataset)', setup='from test_priority_queues import QueueClass, _large_dataset, run_priority_queue')
    timing = timer.repeat(repeat=3, number=10)

    timingfile.write(f'{QueueClass}: {timing}\n')
