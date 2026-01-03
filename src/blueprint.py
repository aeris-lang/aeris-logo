# /// script
# dependencies = ["sympy"]
# ///

from enum import Enum
from argparse import ArgumentParser
from sympy import sqrt, Rational, Point, Line, Triangle

class PaddingType(Enum):
  NONE = "none"
  RECTANGULAR = "rectangular"
  CIRCULAR = "circular"

  def __str__(self):
    return self.value

def get_args():
  parser = ArgumentParser(description="AERIS Logo Coordinate Calculator")
  parser.add_argument("-p", "--padding", type=PaddingType, choices=list(PaddingType), default=PaddingType.NONE)
  parser.add_argument("-s", "--scale", type=int, default=100)
  return parser.parse_args()

def shift_line(base_line, shift):
  p1, p2 = base_line.p1, base_line.p2
  direction = p2 - p1
  normal = Point(-direction.y, direction.x)
  unit_normal = normal / normal.distance(Point(0, 0))
  new_point = p1 + (unit_normal * shift)
  return base_line.parallel_line(new_point)

def calculate_paths():
  phi = (1 + sqrt(5)) / 2
  weight = (phi - 1) / (phi * 2)
  split = weight / 4

  p_left = Point(0, 0)
  p_right = Point(1, 0)
  p_top = Point(Rational(1, 2), 1)

  out1 = Line(p_left, p_top)
  out2 = Line(p_right, p_top)
  out3 = Line(p_left, p_right)
  in1 = shift_line(out1, -weight)
  in2 = shift_line(out2, weight)
  in3 = shift_line(out3, weight)
  sp1 = shift_line(in1, -split)
  sp2 = shift_line(in2, split)

  path1 = [
    out2.intersection(out1)[0],
    out1.intersection(out3)[0],
    out3.intersection(sp2)[0],
    sp2.intersection(in3)[0],
    in3.intersection(in1)[0],
    in1.intersection(out2)[0],
  ]
  path2 = [
    out2.intersection(sp1)[0],
    sp1.intersection(in2)[0],
    in2.intersection(out3)[0],
    out3.intersection(out2)[0],
  ]
  return [path1, path2]

def apply_transformations(paths, padding_type):
  phi = (1 + sqrt(5)) / 2

  if padding_type == PaddingType.RECTANGULAR:
    offset_val = (1 - 1 / phi) / 2
    offset = Point(offset_val, offset_val)
    return [[p / phi + offset for p in path] for path in paths]

  if padding_type == PaddingType.CIRCULAR:
    tri = Triangle(paths[0][0], paths[0][1], paths[1][3])
    scale_factor = 1 / (tri.circumradius * 2) / phi
    paths = [[p * scale_factor for p in path] for path in paths]

    tri = Triangle(paths[0][0], paths[0][1], paths[1][3])
    center = Point(Rational(1, 2), Rational(1, 2))
    offset = center - tri.circumcenter.midpoint(scale_factor * center)
    return [[p + offset for p in path] for path in paths]

  return paths

def print_svg_path(paths, scale):
  for path in paths:
    commands = []
    for i, p in enumerate(path):
      x_val = (p.x * scale).evalf()
      y_val = (scale - p.y * scale).evalf()
      modifier = "M" if i == 0 else "L"
      commands.append(f"{modifier} {x_val} {y_val}")
    print("\n".join(commands) + "\nZ\n")

def main():
  args = get_args()
  paths = calculate_paths()
  paths = apply_transformations(paths, args.padding)
  print_svg_path(paths, args.scale)

if __name__ == "__main__":
  main()
