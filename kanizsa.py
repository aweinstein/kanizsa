import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

def wedge(xy, theta, r=0.1):
    """Creates a PacMan like wedge.

    Parameters
    ----------
    xy : tuple
        (x,y) position of the center of the wedge.
    theta: float
        Orientation, in degrees, of the wedge.
    r : float, optional
        Radius of the wedge. Default to 0.1.

    Returns
    -------
    (Wedge, Rectangle)
        Matplotlib wedge object, and the bounding rectangle of the wedge.
    """
    wedge = mpatches.Wedge(xy, r, theta + 60, theta+360, ec='none', fc='white')
    pad = 3*r
    r = rectangle(xy[0] - 2*r, xy[1] - 2*r, 2*r + pad, 2*r + pad)
    return (wedge, r)


def triangle(xy, length, r=0.1, fake_kanizsa=False):
    """Creates kanizsa figure.

    Parameters
    ----------
    xy : tuple
        (x,y) position of the lower left vertice of the triangle.
    length : tuple
        Lenght of the triangle.
    r : float, optional
        Radius for the wedges.
    fake_kanizsa : bool
        If True, the wedges do not form a triangle.

    Returns
    -------
    ((w1, w2, w3), rect)
        A triplet with the wedges of the kanizsa figure, and the bounding box of
    the kaniza figure.

    """
    angs = np.array([0., 120, -120])
    if fake_kanizsa:
        angs += np.random.uniform(0, 360, 3)
    x, y = xy
    w1, _ = wedge(xy, angs[0], r)
    w2, _ = wedge((x+length, y), angs[1], r)
    factor = np.sin(np.degrees(60))
    x += length / 2
    y += length * factor
    w3, _ = wedge((x,y), angs[2], r)
    rect  = rectangle(xy[0]-2*r, xy[1]-2*r, length + 4*r, length*factor + 4*r)
    return ((w1, w2, w3), rect)


class rectangle(object):
    """Basic rectangle object."""
    def __init__(self, x, y, w, h):
        """Creates a rectangle.

        Parameters
        ----------
        x, y : float
            Left lower corner of the rectangle.
        w, h : float
            Width and height of the rectangle
        """
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def point_not_in_rectangle(self, x, y):
        """Check if a point is inside of the rectangle.

        Parameters
        ----------
        x, y: float
            (x,y) coordinates of the point.

        Returns
        -------
        bool
            True if the point is outside the rectangle
        """
        if ((self.x <= x <= (self.x + self.w)) and
            (self.y <= y <= (self.y + self.h))):
            not_in_rectangle = False
        else:
            not_in_rectangle = True
        return not_in_rectangle

def get_random_point(x_min, x_max, y_min, y_max, rectangles):
    """Get a random point outside the list of rectangles.

    If after 100 iterations the function does not find a point outside the
    rectangles, the program exits.

    Parameters
    ----------
    x_min, x_max, y_min, y_max: float
        Coordinates of the rectangular sample space area.
    rectangles: list
        List of rectangles with the rejection areas.

    """
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

def make_figure(fig_type='illusion', file_name='kanizsa.png'):
    """Make a kanizsa figure and save it as a PNG file.

    Parameters
    ----------
    fig_type: string
        Type of figure. Valid options are
        ['illusion', 'fake', 'triangle'].
        Default is 'illusion'.
    file_name: string
        Name of the PNG file
    """
    plt.figure()
    plt.axes()
    ax = plt.gca()
    canvas_width, canvas_height = 10, 7
    triang_len = 1.5
    wedge_r = 0.2

    ws, rectangles = [], []

    # Add triangle at random position around the middle
    delta = 0.2
    x = np.random.uniform(canvas_width / 2 - triang_len/2 - delta,
                          canvas_width / 2 - triang_len/2 + delta)
    y = np.random.uniform(canvas_height / 2 - triang_len/2 - delta,
                          canvas_height / 2 - triang_len/2 + delta)
    ws_triang, r = triangle((x,y), triang_len, wedge_r,
                            fake_kanizsa=(fig_type == 'fake'))
    if fig_type == 'triangle':
        xs = [x,x+triang_len, x + triang_len/2, x]
        ys = [y, y, y + triang_len * np.sin(np.degrees(60)), y]
        ax.plot(xs, ys, color='white')
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

    ax.set_axis_bgcolor('black')
    ax.set_xticks([])
    ax.set_yticks([])
    plt.axis('scaled')
    ax.set_xlim(0, canvas_width)
    ax.set_ylim(0, canvas_height)
    plt.savefig(file_name, bbox_inches = 'tight', pad_inches=0,
                facecolor='black')
    plt.close()


if __name__ == '__main__':
    n_images = 3
    for n in range(n_images):
        fn = 'kanizsa_{:02d}.png'.format(n)
        print('Making figure', fn)
        make_figure('illusion', fn)
        fn = 'kanizsa_false_{:02d}.png'.format(n)
        print('Making figure', fn)
        make_figure('fake', fn)
        fn = 'kanizsa_triangle_{:02d}.png'.format(n)
        print('Making figure', fn)
        make_figure('triangle', fn)
