#!/usr/bin/python

from itertools import permutations
import pdb
import sys

def build_cypher_list(cylen=4):
    """
    Build a list of cyphers using cylen characters each. List is all permuations.

    Parameters
    ----------
    cylen - num - number of characters per cypher

    Returns
    -------
    cylist - [] - list of all permutations for that number of characters

    Examples
    --------
    >>> from cypher import *
    >>> ['AB', 'BA'] == build_cypher_list(2)
    True

    """
    # get letters AB... for cylen
    letters = [chr(ord('A')+ix) for ix in range(cylen)]
    letters = ''.join(letters)

    cyphertups = list(permutations(letters))
    cyphers = [''.join(tup) for tup in cyphertups]

    return cyphers

def smash_cyphers(cylist):
    """
    Combine list of strings by overlapping characters of adjacent list items.

    Parameters
    ----------
    cylist - [] - list of cyphers to smash together

    Returns
    -------
    cystr - str - one big string of all cyphers overlapping

    Examples
    --------
    >>> from cypher import *
    >>> cylist = ['ABC', 'BCA', 'ACB']
    >>> 'ABCACB' == smash_cyphers(cylist)
    True

    """
    if not cylist:
        return ''

    cystr = cylist[0]
    for cypher in cylist[1:]:
        overlap = get_overlap(cystr, cypher)
        cystr = cystr + cypher[overlap:]

    return cystr

def get_overlap(first, second):
    """
    Determine how many character from the beginning of second match the ending characters
    of first.

    Parameters
    ----------
    first - str - a string of characters
    second - str - another string of characters

    Returns
    -------
    overlap - num - number of characters at the end of first also found at the beginning
                    of second

    Examples
    --------
    >>> from cypher import *
    >>> 3 == get_overlap('ABCD', 'BCDA')
    True
    >>> 0 == get_overlap('ABCD', 'EFG')
    True

    """
    overlap = 0
    for cap in range(len(second), 0, -1):
        # grab chunks of second cypher in decreasing size
        subcy = second[:cap]
        if first.endswith(subcy):
            overlap = cap
            break
    return overlap

def best_next(cystr, cylist):
    """
    Return the item from cylist whose beginning characters most overlap with the ending
    characters of cystr.

    Parameters
    ----------
    cystr - str - string of characters
    cylist - [] - list of strings

    Returns
    -------
    best - str - item from cylist with most overlap with end of cystr

    Examples
    --------
    >>> from cypher import *
    >>> best = best_next('CAB', ['BAC', 'ABC', 'ABD'])
    >>> best in ['ABC', 'ABD']
    True

    """
    overlaps = [get_overlap(cystr, cy) for cy in cylist]
    bestix = overlaps.index(max(overlaps))
    best = cylist[bestix]
    return best

def break_not_ones(nums):
    r"""

    Parameters
    ----------
    nums - [] - list of numbers

    Returns
    -------
    output - str - numbers joined as string, \n after each num != 1

    Examples
    --------
    >>> from cypher import *
    >>> out = break_not_ones([1, 1, 4, 1, 1, 1, 5, 1, 1])
    >>> out == '114\n1115\n11'
    True

    """
    numset = set(nums)
    numstr = ''.join(map(str, nums))
    numset.remove(1)
    for num in numset:
        numstr = numstr.replace(str(num), '%d\n'%num)
    return numstr

if __name__ == '__main__':
    if len(sys.argv) == 1:
        import doctest
        doctest.testmod()
    if len(sys.argv) == 2:
        cylen = int(sys.argv[1])
        cylist = build_cypher_list(cylen)
        cystr = cylist.pop(0)
        print('\nBuilding the sequence:')
        print(cystr)
        overlaps = []
        for ix in range(len(cylist)):
            oldlen = len(cystr)
            best = best_next(cystr, cylist)
            print(' + %s' % best)
            cylist.remove(best)
            cystr = smash_cyphers([cystr, best])
            newlen = len(cystr)
            overlaps.append(newlen-oldlen)
        print('\nSequence growth analysis:')
        print(break_not_ones(overlaps))
        print('\nEfficient sequence, length')
        print(cystr, len(cystr))
