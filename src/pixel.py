class Pixel:
    def __init__(self, strip, index):
        self.strip = strip  # Reference to the Strip object
        self.index = index  # Index in the strip data

    @property
    def rgb(self):
        return self.strip.data[self.index, :3]

    @rgb.setter
    def rgb(self, value):
        self.strip.data[self.index, :3] = value

    @property
    def r(self):
        return self.strip.data[self.index, 0]

    @r.setter
    def r(self, value):
        self.strip.data[self.index, 0] = value

    @property
    def g(self):
        return self.strip.data[self.index, 1]

    @g.setter
    def g(self, value):
        self.strip.data[self.index, 1] = value

    @property
    def b(self):
        return self.strip.data[self.index, 2]

    @b.setter
    def b(self, value):
        self.strip.data[self.index, 2] = value

    @property
    def brightness(self):
        return self.strip.data[self.index, 3]

    @brightness.setter
    def brightness(self, value):
        self.strip.data[self.index, 3] = value