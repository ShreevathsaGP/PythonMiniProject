import random

heap = []
last = -1

# LEGB: Local Enclosing Global Builtin

# child = 2(parent) + 1 and 2(parent) + 2
# parent = (child - 1) // 2

# trickle up
def trickle_up(pos):
    global heap
    global last
    if pos == 0:
        return

    parent = (pos - 1) // 2
    if heap[pos] > heap[parent]:
        swap(pos, parent)

        return trickle_up(parent)

# trickle down
def trickle_down(parent = 0):
    global heap
    global last

    left = (2 * parent) + 1
    right = (2 * parent) + 2

    # check leaf (has no children)
    if left > last and right > last:
        return

    # right child does not exist
    if right > last and heap[parent] < heap[left]:
        swap(parent, left)
        return trickle_down(left)

    # has both children
    if heap[parent] < heap[left] or heap[parent] < heap[right]:

        if heap[left] > heap[right]:
            swap(parent, left)
            trickle_down(left)
        else:
            swap(parent, right)
            trickle_down(right)

# swap 2 nodes
def swap(x1, x2):
    global heap
    global last
    heap[x1], heap[x2] = heap[x2], heap[x1]

# remove from heap
def remove():
    global heap
    global last
    if last == -1:
        return None

    return_value = heap[0]
    swap(0, last)
    heap[last] = -1
    last -= 1

    trickle_down()

    return return_value

# add to heap
def add(x):
    global heap
    global last
    last += 1
    heap[last] = x
    trickle_up(last)


if __name__ == "__main__":

    for size in range(100):
        array = [i for i in range(size)]
        random.shuffle(array)
        heap = [-1] * size
        last = -1
        for x in array:
            add(x)
        removed = [remove() for _ in range(size)]

        if removed != sorted(array, reverse = True):
            print(True)

    # l = [855.0, 315.0, 495.0, 900.0, 585.0, 225.0, 765.0, 450.0, 180.0, 405.0, 720.0, 45.0, 90.0, 540.0, 270.0, 810.0, 360.0, 630.0, 135.0, 675.0]
    # size = len(l)
    # heap = [-1] * size
    # last = -1
    # for x in l:
    #     add(x)

    # removed = [remove() for _ in range(size)]

    # print(removed)
    # s = sorted(l, reverse = True)
    # print(s) 
    # print(s == removed)

# [900, 855, 720, 810, 765, 540, 405, 495, 630, 585, 675, 450, 45, 360, 270, 90, 225, 180, 315, 135]
# [[900.0, None], [855.0, None], [720.0, None], [810.0, None], [765.0, None], [540.0, None], [405.0, None], 
# [495.0, None], [630.0, None], [585.0, None], [675.0, None], [450.0, None], [45.0, None], [360.0, None], 
# [270.0, None], [90.0, None], [225.0, None], [180.0, None], [315.0, None], [135.0, None]]
