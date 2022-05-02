import cv2
import numpy as np
import threading
import colorsys


class Point(object):
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


rw = 2
p = 0
start = Point()
end = Point()

dir4 = [Point(0, -1), Point(0, 1), Point(1, 0), Point(-1, 0)]


def BFS(s, e):

    global img, h, w
    v = [[0 for _ in range(w)] for _ in range(h)]
    parent = [[Point() for _ in range(w)] for _ in range(h)]

    q = [s]
    v[s.y][s.x] = 1
    const = 2000
    found = False
    while q:
        p = q.pop(0)

        for d in dir4:
            cell = p + d
            if (cell.x >= 0 and cell.x < w and cell.y >= 0 and cell.y < h
                    and v[cell.y][cell.x] == 0 and
                (img[cell.y][cell.x][0] != 0 or img[cell.y][cell.x][1] != 0
                    or img[cell.y][cell.x][2] != 0)):

                q.append(cell)
                v[cell.y][cell.x] = v[p.y][p.x] + 1

                img[cell.y][cell.x] = list(
                    reversed([
                        i * 255
                        for i in (colorsys.hsv_to_rgb(
                            v[cell.y][cell.x] / const, 1, 1))
                    ]))

                parent[cell.y][cell.x] = p

                if cell == e:
                    found = True
                    del q[:]
                    break

    if found:
        p = e
        path = []
        while p != s:
            path.append(p)
            p = parent[p.y][p.x]
        path.append(p)
        path.reverse()

        for p in path:
            img[p.y][p.x] = [0, 0, 0]
        print('path found')

    else:
        print('path not found')


def mouse_event(event, pX, pY, flags, param):

    global img, start, end, p

    if event == cv2.EVENT_LBUTTONUP:
        if p == 0:
            cv2.rectangle(img, (pX - rw, pY - rw), (pX + rw, pY + rw),
                          (0, 0, 255), -1)
            start = Point(pX, pY)
            print('Start = ', start.x, start.y)
            p += 1

        elif p == 1:
            cv2.rectangle(img, (pX - rw, pY - rw), (pX + rw, pY + rw),
                          (0, 255, 0), -1)
            end = Point(pX, pY)
            print('end = ', end.x, end.y)
            p += 1


def disp():

    global img
    cv2.imshow("Image", img)
    cv2.setMouseCallback('Image', mouse_event)

    while True:
        cv2.imshow('Image', img)
        k = cv2.waitKey(30) & 0xFF
        if k == 27:
           break


img = cv2.imread('img/maze2.png', cv2.IMREAD_GRAYSCALE)
_, img = cv2.threshold(img, 120, 255, cv2.THRESH_BINARY)

img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
h, w = img.shape[:2]

print("select start and end points: ")

t = threading.Thread(target=disp, args=())
t.daemon = True
t.start()

while p < 2:
    pass

BFS(start, end)

cv2.waitKey(0)

