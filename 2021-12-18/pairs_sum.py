#!/home/andrew/.envs/venv38/bin/python3


import math
import sys


def get_input():
    pair_list = []
    for line in sys.stdin:
        line = line.strip()
        if len(line) == 0:
            continue
        pair_list.append(eval(line))
    return pair_list


class Pair(object):
    """Snailfish number (pair)"""
    def __init__(self, list_of_len2, parent=None):
        left = list_of_len2[0]
        right = list_of_len2[1]
        if type(left) == list:
            left = Pair(left, parent=self)
        elif type(left) == Pair:
            left.parent = self
        if type(right) == list:
            right = Pair(right, parent=self)
        elif type(right) == Pair:
            right.parent = self
        self.left = left
        self.right = right
        self.parent = parent

    def depth(self):
        depth_count = 0
        p = self
        while p.parent is not None:
            depth_count += 1
            p = p.parent
        return depth_count

    def __str__(self, prefix="", new_line=False):
        if new_line:
            out = "\n"
        else:
            out = ""
        indent = (" " * (self.depth() * 2))
        out += indent + prefix + ("Pair (depth=%d):" % self.depth())
        if type(self.left) == int:
            out += "\n" + indent + "  left: %d" % self.left
        else:
            out += self.left.__str__(prefix="left: ", new_line=True)
        if type(self.right) == int:
            out += "\n" + indent + "  right: %d" % self.right
        else:
            out += self.right.__str__(prefix="right: ", new_line=True)
        return out

    def compact_str(self):
        if type(self.left) == int:
            left_str = str(self.left)
        elif type(self.left) == Pair:
            left_str = self.left.compact_str()
        else:
            assert False
        if type(self.right) == int:
            right_str = str(self.right)
        elif type(self.right) == Pair:
            right_str = self.right.compact_str()
        else:
            assert False
        return "[" + left_str + "," + right_str + "]"

    def __add__(self, other):
        """Link the two pairs together.
        WARNING: this is destructive. It modifies its operands by linking them
        together, modifying the parent pointers of the two operands."""
        p = Pair([self, other])
        p.reduce_fully()
        return p

    def magnitude(self):
        """Compute magnitude of pair as described.

        >>> p = Pair([[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]])
        >>> p.magnitude()
        3488
        """
        mag = 0
        if type(self.left) == int:
            mag += 3 * self.left
        else:
            mag += 3 * self.left.magnitude()
        if type(self.right) == int:
            mag += 2 * self.right
        else:
            mag += 2 * self.right.magnitude()
        return mag

    def reduce_fully(self):
        while self.reduce_once():
            pass

    def reduce_once(self):
        """Run reduction algorithm.  Return whether a modification occurred."""
        # explode pass
        for p, parent, which_child in preorder_traversal(self):
            if type(p) == Pair and p.depth() >= 4:
                p.explode()
                return True
        # split pass
        for p, parent, which_child in preorder_traversal(self):
            if type(p) == int and p >= 10:
                setattr(parent, which_child, Pair(split(p), parent=parent))
                return True
        return False

    def explode(self):
        """To explode a pair, the pair's left value is added to the first
        regular number to the left of the exploding pair (if any), and the
        pair's right value is added to the first regular number to the right of
        the exploding pair (if any). Exploding pairs will always consist of two
        regular numbers. Then, the entire exploding pair is replaced with the
        regular number 0."""
        assert type(self.left) == int
        assert type(self.right) == int
        if self.num_to_left() is not None:
            parent, which_child = self.parent_of_num_to_left()
            setattr(parent, which_child, self.num_to_left() + self.left)
        if self.num_to_right() is not None:
            parent, which_child = self.parent_of_num_to_right()
            setattr(parent, which_child, self.num_to_right() + self.right)
        setattr(self.parent, self.which_child(), 0)

    def which_child(self):
        """Return 'left', 'right', or None (if root)"""
        if self.parent is None:
            return None
        elif id(self) == id(self.parent.left):
            return "left"
        elif id(self) == id(self.parent.right):
            return "right"
        else:
            assert False

    def parent_of_num_to_left(self):
        """Find the number to the left of this pair. Returns the number's parent
        Pair and 'left' or 'right' to indicate which child the number is."""
        # Go up to the least common ancestor (self's ancestor is right child)
        p = self
        while (p.parent is not None) and (p.which_child() == "left"):
            p = p.parent
        if p.which_child() == "right":
            lca = p.parent
        else:
            return None   # No numbers to the left of this pair
        # Go down to the right-most int under LCA.left
        if type(lca.left) == int:
            return lca, "left"
        p = lca.left
        while type(p.right) == Pair:
            p = p.right
        return p, "right"

    def num_to_left(self):
        x = self.parent_of_num_to_left()
        if x is None:
            return None
        num_left_parent, num_left_which_child = x
        return getattr(num_left_parent, num_left_which_child)

    def parent_of_num_to_right(self):
        """Find the number to the right of this pair. Returns the number's parent
        Pair and 'left' or 'right' to indicate which child the number is."""
        # Go up to the least common ancestor (self's ancestor is left child)
        p = self
        while (p.parent is not None) and (p.which_child() == "right"):
            p = p.parent
        if p.which_child() == "left":
            lca = p.parent
        else:
            return None   # No numbers to the right of this pair
        # Go down to the left-most int under LCA.right
        if type(lca.right) == int:
            return lca, "right"
        p = lca.right
        while type(p.left) == Pair:
            p = p.left
        return p, "left"

    def num_to_right(self):
        x = self.parent_of_num_to_right()
        if x is None:
            return None
        num_right_parent, num_right_which_child = x
        return getattr(num_right_parent, num_right_which_child)


def preorder_traversal(pair, parent=None, which_child=None):
    yield (pair, parent, which_child)
    if type(pair.left) == int:
        yield (pair.left, pair, "left")
    else:
        for x in preorder_traversal(pair.left, parent=pair, which_child="left"):
            yield x
    if type(pair.right) == int:
        yield (pair.right, pair, "right")
    else:
        for x in preorder_traversal(pair.right, parent=pair, which_child="right"):
            yield x


def split(n):
    return [math.floor(n/2), math.ceil(n/2)]


##############################################################################
# Main program

all_pairs_raw = get_input()
all_pairs = [Pair(pr) for pr in all_pairs_raw]
for p in all_pairs:
    print(p, "\n")

# Add all of the pairs
sum_pairs = all_pairs[0]
for i in range(1, len(all_pairs)):
    sum_pairs = sum_pairs + all_pairs[i]
    print("Sum so far (i=%d):" % i, sum_pairs.compact_str())
print("Magnitude of sum of all pairs:", sum_pairs.magnitude())

# print("\nTest of preorder traversal:")
# for p, parent, which_child in preorder_traversal(sum_pairs):
#     print("--------------------")
#     print("pair or element:")
#     print(p)
#     print("parent:")
#     print(parent)
#     print("which child:", which_child)
#     if type(p) == Pair:
#         print("Number to the left:", p.num_to_left())
#         print("Number to the right:", p.num_to_right())
