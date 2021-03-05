#! /usr/bin/env python3
# tab size is 2
#
# Напишите консольную программу которая будет обходить матрицу улиткой начиная с
# левого верхнего угла. На входе, параметрами 2 числа, размерность матрицы IxJ,
# на выходе список текущих координат для каждой посещенной точки. Например:
# visit.py 3x3
# 0,0
# 0,1
# 0,2
# 1,2
# 2,2
# 2,1
# 2,0
# 1,0
# 1,1
#
# Using: python3 visit.py I J
#    or  python3 visit.py IxJ
# , where I and J are two integers
#
# pytest using: pytest-3 -vv visit.py
#

import sys

def processInput():

  def error(reason):
    raise Exception(f'{reason}. ' +
      'Correct using: python3 visit.py I J or python3 visit.py IxJ'
      ', where I and J are integers')

  def getIntegers(strI, strJ):
    try:
      I = int(strI)
    except Exception as E:
      error(f'Invalid type of the I argument')
    try:
      J = int(strJ)
    except Exception as E:
      error(f'Invalid type of the J argument')
    return I, J

  try:

    # more than two arguments
    if (len(sys.argv) > 3) or (len(sys.argv) == 1):
      error('Incorrect number of arguments')

    # two arguments
    if (len(sys.argv) == 3):
      return getIntegers(sys.argv[1], sys.argv[2])

    # single argument
    if (len(sys.argv) == 2):
      if 'x' in sys.argv[1].lower():
        pos = sys.argv[1].lower().index('x')
        return getIntegers(sys.argv[1][:pos], sys.argv[1][pos + 1:])
      else:
        error('Single argument provided')

  except Exception as e:
    sys.exit(print(e))

def snailPath(I, J):

  # small lambda for printing
  point = lambda i, j : f'{i},{j}\n'
  # ranges of indices
  i0, i1 = 0, I
  j0, j1 = 0, J
  # result string
  result = ''
  # until we break it
  while True:

    # the end
    if (i1 - i0 == 1) and (j1 - j0 == 1):
      result += point(i0, j0)
      break

    # from the left top corner to the right top corner
    for j in range(j0, j1): result += point(i0, j)

    # as we have touched the right border
    j1 -= 1

    # right top corner -> right bottom corner. Exclude the start cell
    if (i1 - i0 == 1): break
    for i in range(i0 + 1, i1): result += point(i, j1)

    # as we have touched the bottom border
    i1 -= 1

    # right bottom corner -> left bottom corner. Exclude the start cell
    if (j1 == j0): break
    for j in range(j1 - 1, j0 - 1, -1): result += point(i1, j)

    # left bottom corner -> left top corner. Exclude the start cell and top line
    if (i1 - i0 == 1): break
    for i in range(i1 - 1, i0, -1): result += point(i, j0)

    # as we have touched the left border, but have used the latest line
    if (j1 - j0 == 1): break
    j0 += 1

    # as we have touched the top line
    i0 += 1
  return result

# for pytest-3
# from the task
def test3x3():
  assert snailPath(3, 3) == '0,0\n0,1\n0,2\n1,2\n2,2\n2,1\n2,0\n1,0\n1,1\n'
# one point
def test1x1(): assert snailPath(1, 1) == '0,0\n'
# movement along a line without turns
def test1x5(): assert snailPath(1, 5) == '0,0\n0,1\n0,2\n0,3\n0,4\n'
# one turn and movement along one line
def test5x1(): assert snailPath(5, 1) == '0,0\n1,0\n2,0\n3,0\n4,0\n'
# three lines and two turns
def test2x5():
  assert snailPath(2, 5) == '0,0\n0,1\n0,2\n0,3\n0,4\n1,4\n1,3\n1,2\n1,1\n1,0\n'
# four lines and three turns
def test5x2():
  assert snailPath(5, 2) == '0,0\n0,1\n1,1\n2,1\n3,1\n4,1\n4,0\n3,0\n2,0\n1,0\n'
# first type of inner exit point
def test3x5():
  assert snailPath(3, 5) == \
  '0,0\n0,1\n0,2\n0,3\n0,4\n1,4\n2,4\n2,3\n2,2\n2,1\n2,0\n1,0\n1,1\n1,2\n1,3\n'
# second type of the inner exit point
def test5x3():
  assert snailPath(5, 3) == \
  '0,0\n0,1\n0,2\n1,2\n2,2\n3,2\n4,2\n4,1\n4,0\n3,0\n2,0\n1,0\n1,1\n2,1\n3,1\n'
# third type of the inner exit point
def test4x6():
  assert snailPath(4, 6) == \
  '0,0\n0,1\n0,2\n0,3\n0,4\n0,5\n1,5\n2,5\n3,5\n3,4\n3,3\n3,2\n3,1\n3,0\n2,0\n'\
  '1,0\n1,1\n1,2\n1,3\n1,4\n2,4\n2,3\n2,2\n2,1\n'
# fourth type of the inner exit point
def test5x4():
  assert snailPath(5, 4) == \
  '0,0\n0,1\n0,2\n0,3\n1,3\n2,3\n3,3\n4,3\n4,2\n4,1\n4,0\n3,0\n2,0\n1,0\n1,1\n'\
  '1,2\n2,2\n3,2\n3,1\n2,1\n'
# number of steps done
def testNumberOfSteps():
  for i in range(1,101,8):
    for j in range(1,201,7):
      assert snailPath(i,j).count(',') == i*j
# center of an odd square grid
def testOddSquareCenter():
  for i in range(3,1000,12):
    s = snailPath(i, i)[-9:-1]
    while s.count('\n') > 1: s = s[1:]
    s = s[s.index('\n') + 1:]
    indexRequired = int((i + 1) / 2) - 1
    assert int(s[:s.index(',')]) == indexRequired
    assert int(s[s.index(',') + 1:]) == indexRequired

def main():
  # gets dimensions of the field
  I, J = processInput()
  # builds and prints the path
  sys.stdout.write(snailPath(I, J))

# The end ----------------------------------------------------------------------
if __name__ == '__main__':
  sys.exit( main() )
