
import sys
from new_reader import reader


def b2i(bites):
    """
    b2i big endian bytes to int
    """
    return sum([ (b << (idx<<3)) for idx, b in enumerate(reversed(bites))])


class BoxHeader:
     def __init__(self,idx,bites):
        self.idx = idx
        self.bites = bites
        self.size = b2i(bites[:4])
        self.name = bites[4:]


class Box:
    def __init__(self,header):
        self.header = header
        self.payload_size= self.header.size - 8

    def decode(self,r):
        r.read(self.payload_size)
        print(f"{self.header.name} size: {self.header.size} @{self.header.idx}")


if __name__ == '__main__':
    with  reader(sys.argv[1]) as r:
        while r:
            idx = r.tell()
            eight_bites = r.read(8)
            if not eight_bites:
                break
            header =BoxHeader(idx,eight_bites)
            box =Box(header)
            box.decode(r)
