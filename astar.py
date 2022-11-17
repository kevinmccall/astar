import heapq

def hueristic(a, b):
    xdiff = abs(a[0] - b[0])
    ydiff = abs(a[1] - b[1])
    return min(xdiff, ydiff) * 14 + 10 * abs(ydiff - xdiff)

def astar(start,end,hueristic):
    

if __name__ == "__main__":
    # a = (0,1)
    # b = (2,2)
    # print(hueristic(a, b))
    # print(hueristic(b,a))

