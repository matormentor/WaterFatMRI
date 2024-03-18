import matplotlib.pyplot as plt
import matplotlib
matplotlib.interactive(True)


class IndexTracker:

    def __init__(self, ax, data):
        self.ax = ax
        self.data = data
        _, _, self.slices = data.shape
        self.ind = self.slices // 2

        self.im = ax.imshow(self.data[:, :, self.ind], cmap="gray")

        self.update()

    def on_scroll(self, event):
        print("%s %s" % (event.button, event.step))
        if event.button == 'up':
            self.ind = (self.ind + 1) % self.slices
        elif event.button == 'down':
            self.ind = (self.ind - 1) % self.slices
        self.update()

    def update(self):
        im_data = self.im.to_rgba(self.data[:, :, self.ind])
        self.im.set_data(im_data)
        self.ax.set_ylabel('slice %s' % self.ind)
        self.im.axes.figure.canvas.draw()


def plot3d(image):
    fig, ax = plt.subplots(1, 1)
    tracker = IndexTracker(ax, image)
    fig.canvas.mpl_connect('scroll_event', tracker.on_scroll)
    plt.show(block=True)
