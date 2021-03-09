#! /usr/bin/env python3
# tab size is 2
#
# In an arbitrary size array stored integers from 1 to 500,000. All numbers are
# unique except for one number that is twice present. Suggest the fastest
# algorithm for non-unique number searching.
#
# Using: python3 unique.py
#

import sys
import numpy
import random
import cProfile
import pstats

def formArray(length=500000):
  """Returns an array of unique integers. Where the doubled item is the last"""

  uniquePart = random.sample(range(1, 500001), length)
  uniquePart.append(uniquePart[random.randint(0, length - 1)])
  return uniquePart

def directMethod(array):
  """The direct way of solving. A loop in the loop and two ifs."""
  for i in range(len(array)):
    for j in range(i + 1,len(array)):
      if array[i] == array[j]:
        return array[i]

def weirdPatience(array):
  """Creating a lot of continuous subsequences and merging them. A lot of
  working with memory"""

  # The piles are sorted in ascending order and represents continuous ranges of
  # integers.
  piles = []
  for x in array:

    flag = True
    # check each pile. Here could be binary search
    for i in range(len(piles)):

      # if we already know something greater
      if (x <= piles[i][-1]):

        # if we already have a continuous range that contains current item
        if (x >= piles[i][0]): return x

        # as we have find a place in a list where current item will be processed
        flag = False
        # if it extends current pile
        if (x + 1 == piles[i][0]):

          piles[i][0] = x
          # if we need to merge two piles
          if (i > 0) and (piles[i - 1][-1] + 1 == x):

            piles[i - 1][-1] == piles[i][-1]
            piles.pop(i)
        # if it is a missed integer that could merge two piles
        elif (i > 0) and (piles[i - 1][-1] + 1 == x):

          piles[i - 1][-1] = x
        # form a new pile, if we did not find a better place for it
        else:

          piles.insert(i, [x, x])
        break

    # in case it is a greatest integer from appeared
    if flag:

      # if it could extend last existing pile
      if (len(piles) > 0) and (piles[-1][-1] + 1 == x):

        piles[-1][-1] = x
      # in other case
      else:

        piles.append([x, x])

def setMethod(array):
  """Slightly faster than using built-in typing methods. But requires memory
  allocation on every check"""
  Set = set()
  for x in array:

    if x not in Set:
      Set.add(x)
    else:
      return x

def sortMethod(array):
  """Faster as it allocates memory once on copying of an array (to not impact on
  the input data)"""
  localArray = sorted(array)
  for i in range(len(localArray) - 1):
    if localArray[i] == localArray[i + 1]:
      return localArray[i]

def lomutoSort(array):
  """Built-in sorting and one for loop"""
  # do not cause on the input data
  arr = array.copy()
  # to be sure that we are not cheating
  i = random.randint(0, len(arr) - 2)
  arr[i], arr[-1] = arr[-1], arr[i]

  # main call
  def quickSort(arr, iLow, iHigh):
    # if sorting is reasonable
    if (iLow + 1 < iHigh):
      # sorting that could find the not unique value
      p, flag = partition(arr, iLow, iHigh)
      # if we did not find it, than sort left side
      if not flag: flag = quickSort(arr, iLow, p)
      # if we did not find it still, than sort right side
      if not flag: flag = quickSort(arr, p + 1, iHigh - 1)
      # returns the result
      return flag

  # sorting part
  def partition(arr, iLow, iHigh):
    # left and right indices. They would be changed
    i, j = iLow, iHigh - 1
    # until swapping of indices
    while True:
      # until we find a place with a value greater than the pivot
      while (arr[i] < arr[iHigh]):
        # in case we are lucky
        if (i != j) and (arr[i] == arr[j]): return -10, arr[i]
        i += 1
      # if we are lucky and our pivot is duplicated value
      if (i != iHigh) and (arr[i] == arr[iHigh]): return -10, arr[i]
      # until we find a place with a value smaller than the pivot
      while (arr[j] > arr[iHigh]):
        # in case we are lucky
        if (i != j) and (arr[i] == arr[j]): return -10, arr[i]
        j -= 1
      # if indices swapped
      if (i >= j): break
      # if we are lucky and our pivot is duplicated value
      if (arr[j] == arr[iHigh]): return -10, arr[j]
      # if we have found the equal values
      if arr[i] == arr[j]: return -10, arr[i]
      # swapping of the values
      arr[i], arr[j] = arr[j], arr[i]
      # next step
      i, j = i + 1, j - 1
    # we sorted up all values relative to the pivot and here is the border
    return j, False

  # main call
  flag = quickSort(arr, 0, len(arr) - 1)
  if flag: return flag
  # in case we are not lucky
  arr.sort()
  for i in range(len(arr) - 1):
    if arr[i] == arr[i + 1]:
      return arr[i]

def main():

  error = lambda string : sys.exit(f"{string} does not work")

  pr = cProfile.Profile()
  i = 0
  while (i < 500000):
    i = min(i + random.randint(1,50000), 500000)
    arr = formArray(i)
    pr.enable()
    # a fifth place. Commented as too computationally expensive
    # if (weirdPatience(arr) != arr[-1]): error('Custom weird patience')
    # a fourth place. Commented as too computationally expensive
    # if (directMethod(arr) != arr[-1]): error('Direct method')
    # a third place
    if (lomutoSort(arr) != arr[-1]):
      error('Modified quick sort method (Lomuto partition scheme)')
    # a second place
    if (setMethod(arr) != arr[-1]): error('Method with a set')
    # a first place
    if (sortMethod(arr) != arr[-1]): error('Method with a sort')
    pr.disable()
    print(f'{i + 1} items array checked. {round(100*(i + 1)/500001,2)}% done')
  pstats.Stats(pr).sort_stats('cumtime','time').print_stats(\
    'directMethod|weirdPatience|setMethod|sortMethod|lomutoSort')

# The end ----------------------------------------------------------------------
if __name__ == '__main__':
  sys.exit( main() )
