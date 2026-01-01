# /// script
# dependencies = ["sympy"]
# ///

import argparse
import sympy as sp
from sympy.geometry import Point, Line

parser = argparse.ArgumentParser(description="AERIS Logo Coordinate Calculator")
parser.add_argument("--margin", action="store_true")
parser.add_argument("--scale", type=int, default=100)
args = parser.parse_args()

margin = args.margin
scale = args.scale

phi = (1 + sp.sqrt(5)) / 2
weight = (phi - 1) / (2*phi) * scale
split = weight / 4

def shift_perpendicular(base_line, shift):
  p1, p2 = base_line.p1, base_line.p2
  dx = p2.x - p1.x
  dy = p2.y - p1.y
  normal_vx = -dy
  normal_vy = dx
  norm = sp.sqrt(normal_vx ** 2 + normal_vy ** 2)
  shift_vx = (normal_vx / norm) * shift
  shift_vy = (normal_vy / norm) * shift
  new_point = Point(p1.x + shift_vx, p1.y + shift_vy)
  return base_line.parallel_line(new_point)

left_bottom = Point(0, 0)
right_bottom = Point(scale, 0)
middle_top = Point(scale / 2, scale)
outline1 = Line(left_bottom, middle_top)
outline2 = Line(right_bottom, middle_top)
outline3 = Line(left_bottom, right_bottom)
inline1 = shift_perpendicular(outline1, -weight)
inline2 = shift_perpendicular(outline2, weight)
inline3 = shift_perpendicular(outline3, weight)
split1 = shift_perpendicular(inline1, -split)
split2 = shift_perpendicular(inline2, split)

points1 = [
  outline2.intersection(outline1)[0],
  outline1.intersection(outline3)[0],
  outline3.intersection(split2)[0],
  split2.intersection(inline3)[0],
  inline3.intersection(inline1)[0],
  inline1.intersection(outline2)[0],
]
points2 = [
  outline2.intersection(split1)[0],
  split1.intersection(inline2)[0],
  inline2.intersection(outline3)[0],
  outline3.intersection(outline2)[0],
]

offset = scale * (1 - 1 / phi) / 2
for points in [points1, points2]:
  for i, point in enumerate(points):
    x = point.x
    y = point.y
    if margin:
      x = x / phi + offset
      y = y / phi + offset
    x = x.evalf()
    y = (scale - y).evalf()
    modifier = "M" if i == 0 else "L"
    print(f"{modifier} {x} {y}")
  print("Z")
  print()
