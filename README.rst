======================
Priority Queue Testing
======================

Tests and timings of Python3 Priority Queue implementations

The internet seems to say that the easiest way to implement a Priority Queue in Python is with the
`queue.PriorityQueue` class and the fastest code is made using the `heapq` module.  However, in
thinking about how real-world priority queues are constructed, I realized that some of those are
created with multiple queues behind a single gatekeeper rather than attempting to reorder a single
queue whenever a higher priority entry comes in.

I wrote a few sample implementations to test whether the single queue or multiple queue approach is
faster.


-------
Summary
-------

My timings seem to indicate that size of the queue during operation is the primary factor for
deciding between competing implementations.  A priority queue based around a list and the heapq
module is the fastest algorithm if the priority queue is never going to exceed a few hundred
active entries.  On the other hand, if a priority queue will run into the thousands of active
entries waiting to be popped off of the stack, can be faster if it is implemented by multiple
queues.

A secondary factor is how many priorities will be active at a time.  Priority queues with many
entries at the same priority level will benefit from multiple queue implementations.  Priority
queues where the vast majority of entries are at different priority levels will benefit less.


Implementations
===============

priorityqueue.py
----------------

This is our baseline.  It uses the stdlib's `queue.PriorityQueue` with additions to work honor
insertion-order.  The internet notes that this is slower than custom code based on `heapq` because
it is thread-safe.  That's understandable.  I wish that the stdlib implementation had
insertion-order builtin, though.  If it did, then you could probably use this out of the box in the
majority of code which needed a priority queue.  It doesn't, though, and the code to implement
something based around `heapq` directly is of the same complexity so you end up having to
choose whether you want the speed of `heapq` or the thread-safety of `PriorityQueue`.


heapq1.py
---------

The basic list and `heapq` based priority queue had the fastest times for datasets where the active
entries in the queue stayed small (below 512 entries).  This implementation only adds a little
overhead above what the heapq operations demand.  The implementation is slightly more expensive to
push as it obeys insertion-order when multiple entries have the same priority and has to both pack
and unpack the actual data from the priority on push and pop.

The main overhead to this queue should come from the `heapq` algorithm itself.  `heapq` makes sure
that the underlying list is sorted at all times.  Because of that, pushing an entry may require
moving elements around the underlying list.

heapqdict.py
------------

This is very similar to the implemention of `dictionary4.py`.  Like `dictionary4.py`, this
implementation uses both a dictionary and a list + `heap` to look at the data in different ways.
Unlike dictionary4, the data can be accessed from either the dictionary or the list.  This means
that we still need to enter the data into the lists with the priority as part of the data which
forces us to pack and unpack each entry into tuples.  However, when popping an entry, we do need
that information so the packing and unpacking may balance out with fewer function calls to retrieve
the data.  See the description of `dictionary4.py` for more details of what we're doing here.


dictionary1.py and dictionary2.py
---------------------------------

The primary storage of the queues becomes a dictionary instead of a list + `heapq`. These are much
slower to pop because each pop has to sort the dictionary keys in order to know what the highest
priority is.  I'll explain the concepts i nthe dictionary4.py writeup.


dictionary3.py
--------------

This tracks the highest priority by storing the priority of every active queue in a `heapq`.  This
is slower than `dictionary4.py` because it stores a priority for every entry into the `heapq` list
whereas `dictionary4.py` only stores a priority into the `heapq` list for every queue.
`dictionary3.py` ends up churning the `heapq` list more often than `dictionary4.py` because of this.


dictionary4.py
--------------

`dictionary4.py` (and all of the `dictionary*.py` implementations) use a dictionary instead of
a list as their primary storage of queues.  The dictionary is keyed by priority.  Each entry in the
dictionary is a `deque` (Double-ended queue, a specialized list which is cheaper to operate on both
the left and right ends of the queue than on the normal list class).  Whenever a new entry is added
at a given priority, the new entry is appended to the `deque` for that priority level.  Whenever an
entry is popped, the highest priority is found, then we lookup the `deque` for that priority level and
remove the first element from there.

To avoid having to calculate the highest priority each time, we use `heapq` with a list which
stores the priorities which are active in the dictionary.  That way we can always look at the first
element of the `heapq`-sorted list to know what the highest priority is.

This queue imposes more overhead than `heapq1`.  When an entry with a new priority is added, we have
to add both an entry to a `deque` within the dictionary and to the `heapq`-list of priorities.  We may
end up allocating a new `deque` if that priority had not previously been active within the queue.
When an entry is popped, we have to check whether the `deque` at that priority level is now empty and
if so, both delete the `deque` and remove that priority from the `heapq`-list.

The advantage is that anytime we have multiple entries using the same priority, pushing and popping
will not require searching or re-ordering the `heapq`-list.

All further `dictionary*.py` implementations have tradeoffs compared to `dictionary4.py` which may
increase their speed in some circumstances while decreasing them in others.


dictionary5.py
--------------

`dictionary5.py` does not delete a `deque` for a priority when it is empty.  This leads to more
memory usage but slightly quicker popping.  pushing into a queue which had been previously emptied
should also be sped up a tiny amount because the `deque` does not have to be recreated.

Memory can be reclaimed by manually calling the `compact()` method of `dictionary5.py`.


dictionary6.py
--------------

`dictionary6.py` does not use a `defaultdict` or a `deque`.  This should speed up pushing by a minor
amount because the list literal syntax will be faster than calling the list or `deque` function as
a constructor.  However, popping will be slower because `pop(0)` on a list will be slower than
`popleft()` on a `deque`.  This is probably a bad tradeoff but the numbers are small enough that it
is hard to tell at this point.


dictionary7.py
--------------

`dictionary7.py` uses a `deque` but not a `defaultdict`.  The theory here is that we have to have
a conditional in our code to add the priority to the list + `heapq` when the `deque` doesn't
exist already.  So creating the `deque` in our code should be less overhead than also having
a hidden conditional inside of the `defaultdict` implementation.

This may not be faster than `dictionary5.py`, though, as it ends up recreating empty `deques`
instead of re-using them.


------------------------------
Description of Implementations
------------------------------

-----------
Raw timings
-----------

These timings are generated by using pytest to run the test cases in
test_priority_queues.py.  The correctness tests are always run.  The small,
medium, and large priority tests are run by varying the number of
priority_values to select from in the ```create_large_dataset()``` fixture.


Very small correctness test
===========================

* 10 entries
* 7 priorities used in the range -20::80

.. code-block::

    <class 'priorityqueue.PriorityQueue'>: [6.9144796947948635, 6.984554157126695, 6.812578503973782]
    <class 'heapq1.PriorityQueue'>: [1.4143773941323161, 1.411599649116397, 1.393806123174727]
    <class 'heapqdict.PriorityQueue'>: [1.6279728161171079, 1.6371804689988494, 1.6638120491988957]
    <class 'dictionary1.PriorityQueue'>: [1.8275236771441996, 1.838889586739242, 1.8275918406434357]
    <class 'dictionary2.PriorityQueue'>: [1.7242899108678102, 1.7195152430795133, 1.7204458420164883]
    <class 'dictionary3.PriorityQueue'>: [1.6169357378967106, 1.6101316949352622, 1.7187733710743487]
    <class 'dictionary4.PriorityQueue'>: [1.6595132849179208, 1.584283689968288, 1.5904550510458648]
    <class 'dictionary5.PriorityQueue'>: [1.5416011442430317, 1.5483587980270386, 1.5300904200412333]
    <class 'dictionary6.PriorityQueue'>: [1.4555647065863013, 1.4703867179341614, 1.4719321434386075]
    <class 'dictionary7.PriorityQueue'>: [1.5206656926311553, 1.5218001534231007, 1.6270989580079913]

The simple heapq based implementation is the winner here.  From my testing, the list + heapq wins
whenever the number of active entries in the queue remains small.


Large number of entries, few priorities
=======================================
* 2**16 entries
* 2**3 + 1 possible priorities in the range -4::4
* 2**16 chunksize

.. code-block::

    <class 'priorityqueue.PriorityQueue'>: [5.9570200820453465, 6.040737457107753, 6.037866178900003]
    <class 'heapq1.PriorityQueue'>: [2.756810828112066, 2.817298252135515, 2.7387360259890556]
    <class 'heapqdict.PriorityQueue'>: [1.4160102768801153, 1.4227407942526042, 1.414424885995686]
    <class 'dictionary1.PriorityQueue'>: [2.3133664540946484, 2.2975933281704783, 2.293232004158199]
    <class 'dictionary2.PriorityQueue'>: [1.7214486692100763, 1.7298582550138235, 1.7267649839632213]
    <class 'dictionary3.PriorityQueue'>: [1.8106810739263892, 1.8282991610467434, 1.8354365080595016]
    <class 'dictionary4.PriorityQueue'>: [1.4327944931574166, 1.4162718397565186, 1.4461636180058122]
    <class 'dictionary5.PriorityQueue'>: [1.4465915127657354, 1.4224484460428357, 1.4488836601376534]
    <class 'dictionary6.PriorityQueue'>: [1.9581143110990524, 1.954190818592906, 1.989499479997903]
    <class 'dictionary7.PriorityQueue'>: [1.4231822085566819, 1.4679390941746533, 1.434176113922149]

We can see here how a high number of active entries and low number of priorities combine to make the
`heapq` + list implementation less desirable.

The true winner is hard to tell, though.  `heapqdict` has the best times on this run but
`dictionary4`, `dictionary5`, and `dictionary7` are also in the ballpark.


Large number of entries, moderate priorities
============================================
* 2**12 entries
* 2**12 + 1 possible priorities in the range -4096::4096
* 2**12 chunksize

Large number of entries, many priorities
========================================
* 2**12 entries
* 2**16 + 1 possible priorities in the range -65536::65536
* 2**12 chunksize

Large number of entries, few priorities, small chunk size
=========================================================
* 2**12 entries
* 2**3 + 1 possible priorities in the range -4::4
* 2**7 chunksize

Large number of entries, few priorities, moderate chunk size
=============================================================
* 2**12 entries
* 2**3 + 1 possible priorities in the range -4::4
* 2**8 chunksize

Large number of entries, few priorities, large chunk size
=========================================================
* 2**12 entries
* 2**3 + 1 possible priorities in the range -4::4
* 2**9 chunksize

Large number of entries, many priorities, moderate chunk size
=============================================================
* 2**12 entries
* 2**16 + 1 possible priorities in the range -65536::65536
* 2**8 chunksize
