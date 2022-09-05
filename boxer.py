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
        self.idx= header.idx
        self.size = header.size
        self.name = header.name
        self.payload_size= header.size - 8
        print(f"{self.name} size: {self.size}  @{self.idx}")

    def decode(self,r):
        r.read(self.payload_size)

        
class Ftyp(Box):
    def __init__(self,header):
        super().__init__(header)
        self.major_brand = None
        self.minor_version = None
        self.compatible_brands=[]

    def decode(self,r):
        pay = r.read(self.payload_size)
        self.major_brand = pay[:4]
        self.minor_version = b2i(pay[4:8])
        pay = pay[8:]
        self.compatible_brands=[pay[i:i+4] for i in range(0,len(pay),4)]
        print(self.__dict__)

        
boxes = {
    b"ftyp": Ftyp,
    }


if __name__ == '__main__':
    with  reader(sys.argv[1]) as r:
        while r:
            idx = r.tell()
            eight_bites = r.read(8)
            if not eight_bites:
                break
            header =BoxHeader(idx,eight_bites)
            if header.name in boxes:
                box = boxes[header.name](header)
            else:
                box =Box(header)
            box.decode(r)
