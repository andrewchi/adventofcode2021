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
TYPE_SUM = 0
TYPE_PRODUCT = 1
TYPE_MINIMUM = 2
TYPE_MAXIMUM = 3
TYPE_LITERAL = 4
TYPE_GREATER_THAN = 5
TYPE_LESS_THAN = 6
TYPE_EQUAL_TO = 7
LENGTH_TYPE_BITS = 0
LENGTH_TYPE_SUBPACKETS = 1

class BITSPacket(object):
    def __init__(self, bit_string):
        # print("Parsing:", bit_string)
        assert len(bit_string) > 3 + 3
        self.version = int(bit_string[:3], base=2)
        self.typeID = int(bit_string[3:6], base=2)
        pos = 6
        if self.typeID == TYPE_LITERAL:
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
        if self.typeID == TYPE_LITERAL:
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

    def evaluate(self):
        if self.typeID == TYPE_LITERAL:
            return self.intval
        elif self.typeID == TYPE_SUM:
            return sum(sp.evaluate() for sp in self.subpackets)
        elif self.typeID == TYPE_PRODUCT:
            prod = 1
            for sp in self.subpackets:
                prod *= sp.evaluate()
            return prod
        elif self.typeID == TYPE_MINIMUM:
            return min(sp.evaluate() for sp in self.subpackets)
        elif self.typeID == TYPE_MAXIMUM:
            return max(sp.evaluate() for sp in self.subpackets)
        elif self.typeID == TYPE_GREATER_THAN:
            assert len(self.subpackets) == 2
            ssp = self.subpackets
            return int(ssp[0].evaluate() > ssp[1].evaluate())
        elif self.typeID == TYPE_LESS_THAN:
            assert len(self.subpackets) == 2
            ssp = self.subpackets
            return int(ssp[0].evaluate() < ssp[1].evaluate())
        elif self.typeID == TYPE_EQUAL_TO:
            assert len(self.subpackets) == 2
            ssp = self.subpackets
            return int(ssp[0].evaluate() == ssp[1].evaluate())
        else:
            raise NotImplementedError("Unknown typeID: " + str(self.typeID))


###############################################################################

bit_strings = get_input()
for bs in bit_strings:
    packet = BITSPacket(bs)
    print("\n" + bs)
    print(packet)
    print("Packet evaluation:", packet.evaluate())
