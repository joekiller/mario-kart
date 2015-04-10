from watcher import Watcher
import operator
import numpy as np
import cv2
import util
import scipy

templateFiles = ["lap1.jpg", "lap2.jpg", "lap3.jpg"]
templates = []

for filename in templateFiles:
    templates.append(cv2.Canny(cv2.imread("templates/" + filename, cv2.IMREAD_GRAYSCALE), 300, 280))

size = np.max([template.shape[::-1] for template in templates], 0)

class LapWatcher(Watcher):
    predicate = {"raceStatus": "started"}
    debug = True
    topLeft = {"left": (75, 120), "right": (329,120)}

    def __init__(self):
        super(LapWatcher, self).__init__()
        self.verified = 0
        self.lastLap = None
    
    def debugRect(self):
        return (tuple(self.topLeft[self.direction]), tuple(size))

    def update(self):

        gray = cv2.cvtColor(self.window, cv2.COLOR_BGR2GRAY)
        win = gray
        vals = []

        crop = util.crop(win, np.hstack((self.topLeft[self.direction], size)))
        area = cv2.Canny(crop, 400, 300)

        for index, template in enumerate(templates):
            val = np.sum((area - template)**2)
            vals.append(val)

        self.lap = np.argmin(vals) + 1
        if self.lastLap == self.lap:
          self.verified += 1
        else:
          self.verified = 0
          self.lastLap = self.lap
        if self.verified > 2:
          self.manager.state('lap', self.lap);


export = LapWatcher
