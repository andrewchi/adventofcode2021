#!/home/andrew/.envs/venv38/bin/python3

import sys

#from ply import lex
#from ply import yacc

def get_input():
    bit_strings = []
    for line in sys.stdin:
        line = line.strip()
        if len(line) == 0:
            continue
        n_bits = len(line) * 4
        line_bits = ( bin(int(line, 16))[2:] ).zfill(n_bits)
        bit_strings.append(line_bits)
    return bit_strings

# typeIDs
TYPE_INTEGER = 4
LENGTH_TYPE_BITS = 0
LENGTH_TYPE_SUBPACKETS = 1

class BITSPacket(object):
    def __init__(self, bit_string):
        # print("Parsing:", bit_string)
        assert len(bit_string) > 3 + 3
        self.version = int(bit_string[:3], base=2)
        self.typeID = int(bit_string[3:6], base=2)
        pos = 6
        if self.typeID == TYPE_INTEGER:
            self.intval = 0
            last_block_done = False
            while not last_block_done:
                self.intval *= 16
                self.intval += int(bit_string[(pos+1):(pos+5)], base=2)
                last_block_done = (bit_string[pos] == '0')
                pos += 5
        else:
            self.intval = None
            self.subpackets = []
            self.lengthTypeID = int(bit_string[pos], base=2)
            pos += 1
            if self.lengthTypeID == LENGTH_TYPE_BITS:
                self.n_subbits = int(bit_string[pos:pos+15], base=2)
                pos += 15
                used_subbits = 0
                while used_subbits < self.n_subbits:
                    new_subpacket = BITSPacket(bit_string[pos:])
                    self.subpackets.append(new_subpacket)
                    used_subbits += len(new_subpacket)
                    pos += len(new_subpacket)
            else:
                self.n_subpackets = int(bit_string[pos:pos+11], base=2)
                pos += 11
                for i in range(self.n_subpackets):
                    new_subpacket = BITSPacket(bit_string[pos:])
                    self.subpackets.append(new_subpacket)
                    pos += len(new_subpacket)
        self.bits = bit_string[:pos]

    def __len__(self):
        return len(self.bits)

    def is_operator(self):
        return self.intval is None

    def is_literal(self):
        return self.intval is not None

    def __str__(self, nest_level=0):
        indent = "  " * nest_level
        s = indent + "version=%d typeID=%d" % (self.version, self.typeID)
        if self.typeID == TYPE_INTEGER:
            s += " (LITERAL) %d" % self.intval
        else:
            s += " (OPERATOR) lengthTypeID=%d" % self.lengthTypeID
            if self.lengthTypeID == LENGTH_TYPE_BITS:
                s += " total_subpacket_bits=%d" % self.n_subbits
            else:
                s += " number_of_subpackets=%d" % self.n_subpackets
            for sp in self.subpackets:
                s += "\n" + sp.__str__(nest_level=nest_level+1)
        return s


def version_sum(packet):
    vsum = 0
    vsum += packet.version
    if packet.is_operator():
        for sp in packet.subpackets:
            vsum += version_sum(sp)
    return vsum


###############################################################################

bit_strings = get_input()
for bs in bit_strings:
    packet = BITSPacket(bs)
    print("\n" + bs)
    print(packet)
    print("Sum of version numbers:", version_sum(packet))
