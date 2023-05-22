class Rectangle:
    def __init__(self, left=0, right=0, lower=0, upper=0):
        self.left = left
        self.right = right
        self.lower = lower
        self.upper = upper

    def contains_point(self, point):
        return self.left <= point[0] <= self.right and self.lower <= point[1] <= self.upper

    def contains_rect(self, other):
        return (self.left <= other.left and self.right >= other.right
                and self.lower <= other.lower and self.upper >= other.upper)

    def intersect(self, other):
        return (min(self.right, other.right) > max(self.left, other.left)
                and min(self.upper, other.upper) > max(self.lower, other.lower))

    def rectangle_intersection(self, other):
        return Rectangle(max(self.left, other.left), min(self.right, other.right), max(self.lower, other.lower), min(self.upper, other.upper))


class KDNode:
    def __init__(self):
        self.left = None
        self.right = None
        self.line = None
        self.point = None
        self.rect = None
        self.count = 0


class KDTree:
    def __init__(self, points):
        self.root = None
        self.points = points

    def build_kd(self):
        def build(x1, x2, y1, y2, x_list, y_list, depth=0):
            node = KDNode()
            node.rect = Rectangle(x1, x2, y1, y2)
            if len(x_list) > 1:
                if depth % 2:
                    m = len(y_list) // 2
                    median = (y_list[m][1] + y_list[m - 1][1]) / 2
                    node.line = median
                    lower_x, upper_x = [], []
                    lower_y, upper_y = [], []
                    for p in x_list:
                        if p[1] < median:
                            lower_x.append(p)
                        else:
                            upper_x.append(p)
                    for p in y_list:
                        if p[1] < median:
                            lower_y.append(p)
                        else:
                            upper_y.append(p)
                    node.left = build(x1, x2, y1, median, lower_x, lower_y, depth + 1)
                    node.right = build(x1, x2, median, y2, upper_x, upper_y, depth + 1)
                    node.count = node.left.count + node.right.count
                else:
                    m = len(x_list) // 2
                    median = (x_list[m][0] + x_list[m-1][0]) / 2
                    node.line = median
                    left_y, right_y = [], []
                    left_x, right_x = [], []
                    for p in y_list:
                        if p[0] < median:
                            left_y.append(p)
                        else:
                            right_y.append(p)
                    for p in y_list:
                        if p[0] < median:
                            left_x.append(p)
                        else:
                            right_x.append(p)
                    node.left = build(x1, median, y1, y2, left_x, left_y, depth + 1)
                    node.right = build(median, x2, y1, y2, right_x, right_y, depth + 1)
                    node.count = node.left.count + node.right.count
            else:
                if x_list:
                    node.point = x_list[0]
                    node.count = 1
                else:
                    node.point = None
                    node.count = 0
            return node

        sort_x = sorted(self.points)
        sort_y = sorted(self.points, key=lambda x: (x[1], x[0]))
        self.root = build(sort_x[0][0], sort_x[-1][0], sort_y[0][1], sort_y[-1][1], sort_x, sort_y)

    def return_points_inside_rect(self, rect):
        def report_subtree(node):
            if node is None:
                return
            if node.point is not None:
                points_inside.append(node.point)
            else:
                report_subtree(node.left)
                report_subtree(node.right)

        def search_kd_tree(node):
            if node is None:
                return
            if node.point is not None:
                if rect.contains_point(node.point):
                    points_inside.append(node.point)
                return
            elif rect.contains_rect(node.rect):
                report_subtree(node)
            elif not rect.intersect(node.rect):
                return
            else:
                search_kd_tree(node.left)
                search_kd_tree(node.right)

        points_inside = []
        search_kd_tree(self.root)
        return points_inside


# points = [(269, 205), (269, 210), (269, 229), (269, 348), (270, 205), (270, 210), (270, 229), (270, 267), (270, 286),
# (270, 348), (270, 353), (270, 513), (293, 245), (293, 413), (293, 526), (294, 223), (294, 245), (294, 255),
# (294, 373), (294, 382), (294, 413), (294, 526), (317, 240), (317, 433), (317, 542), (317, 547), (318, 240),
# (318, 291), (318, 316), (318, 378), (318, 389), (318, 422), (318, 433), (318, 438), (318, 491), (318, 516),
# (318, 542), (318, 547), (341, 184), (341, 230), (341, 361), (341, 479), (341, 618), (341, 623), (342, 184),
# (342, 230), (342, 339), (342, 361), (342, 441), (342, 479), (342, 526), (342, 618), (342, 623)]

# tree = KDTree(points)
# tree.build_kd()
# rect = Rectangle(100, 350, 100, 300)
# inside = tree.return_points_inside_rect(rect)
# print(sorted(inside))
# found = []
# for p in points:
#     if rect.contains_point(p):
#         found.append(p)
# print(sorted(found))
