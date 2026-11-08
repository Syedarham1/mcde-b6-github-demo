class ReversibleRange:
  
    def __init__(self, start, stop=None, step=1):
        if stop is None:
            stop = start
            start = 0
        if step == 0:
            raise ValueError("Step cannot be zero.")
        self.start = start
        self.stop = stop
        self.step = step

        if (step > 0 and start >= stop) or (step < 0 and start <= stop):
            self._length = 0
        else:
            import math
            self._length = math.ceil((stop - start) / step)

    def __len__(self):
        return self._length

    def __iter__(self):
        current = self.start
        for _ in range(self._length):
            yield current
            current += self.step

    def __reversed__(self):
        if self._length == 0:
            return iter([])
        last_val = self.start + (self._length - 1) * self.step
        current = last_val
        for _ in range(self._length):
            yield current
            current -= self.step

    def __contains__(self, item):
        if self._length == 0:
            return False
        if not isinstance(item, (int, float)):
            return False
        if (item - self.start) % self.step != 0:
            return False
        if self.step > 0:
            return self.start <= item < self.stop
        else:
            return self.stop < item <= self.start

if __name__ == "__main__":
    r = ReversibleRange(2, 11, 3)
    print(list(r))             
    print(list(reversed(r)))
    print(5 in r)              