import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

def wedge(xy, theta, r=0.1):
    wedge = mpatches.Wedge(xy, r, theta + 60, theta+360, ec='none', fc='white')
    pad = 3*r
    r = rectangle(xy[0] - 2*r, xy[1] - 2*r, 2*r + pad, 2*r + pad)
    return (wedge, r)


def triangle(xy, length, r=0.1):
    x, y = xy
    w1, _ = wedge(xy, 0, r)
    w2, _ = wedge((x+length, y), 120, r)
    factor = np.sin(np.degrees(60))
    x += length / 2
    y += length * factor # move the sin out of the function to
                         # shave a few microseconds
    w3, _ = wedge((x,y), -120, r)
    rect  = rectangle(xy[0]-2*r, xy[1]-2*r, length + 4*r, length*factor + 4*r)
    return ((w1, w2, w3), rect)


class rectangle():
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def point_not_in_rectangle(self, x, y):
        if ((self.x <= x <= (self.x + self.w)) and
            (self.y <= y <= (self.y + self.h))):
            not_in_rectangle = False
        else:
            not_in_rectangle = True
        return not_in_rectangle

def get_random_point(x_min, x_max, y_min, y_max, rectangles):
    n_max = 100
    n = 0
    while n < n_max:
        n += 1
        x = np.random.uniform(x_min, x_max)
        y = np.random.uniform(y_min, y_max)
        if all([r.point_not_in_rectangle(x, y) for r in rectangles]):
            return x, y

    print("Can't find empty space")
    sys.exit(1)

if __name__ == '__main__':
    canvas_width, canvas_height = 10, 7
    triang_len = 1.5
    wedge_r = 0.2
    plt.close('all')
    plt.axes()
    ax = plt.gca()

    ws, rectangles = [], []

    # Add triangle at random position around the middle
    delta = 0.2
    x = np.random.uniform(canvas_width / 2 - triang_len/2 - delta,
                          canvas_width / 2 - triang_len/2 + delta)
    y = np.random.uniform(canvas_height / 2 - triang_len/2 - delta,
                          canvas_height / 2 - triang_len/2 + delta)
    ws_triang, r = triangle((x,y), triang_len, wedge_r)
    ws.extend(ws_triang)
    rectangles.append(r)

    # Add wedges at random positions
    n_wedges = 40
    for _ in range(n_wedges):
        x, y = get_random_point(2 * wedge_r, canvas_width - 2 * wedge_r,
                                2 * wedge_r, canvas_height - 2 * wedge_r,
                                rectangles)
        theta = np.random.uniform(0, 330)
        w, r = wedge((x, y), theta, wedge_r)
        ws.append(w)
        rectangles.append(r)

    for w in ws:
        ax.add_patch(w)

    # FOR DEBUG
    # for r in rectangles:
    #     rect = mpatches.Rectangle((r.x, r.y), r.w, r.h, ec='red', fc='none')
    #     ax.add_patch(rect)


    ax.set_axis_bgcolor('black')
    ax.set_xticks([])
    ax.set_yticks([])
    plt.axis('scaled')
    plt.xlim(0, canvas_width)
    plt.ylim(0, canvas_height)
    plt.tight_layout(pad=1)
    plt.savefig('kanizsa.pdf')
    plt.savefig('kanizsa.png')
    plt.show()
