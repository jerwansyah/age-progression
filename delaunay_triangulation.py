import cv2
import numpy as np
import random

class DelaunayTriangulation:
    def __init__ (self):
        pass

    # Check if a point is inside a rectangle
    def rect_contains(self, rect, point):
        if point[0] < rect[0]:
            return False
        elif point[1] < rect[1]:
            return False
        elif point[0] > rect[2]:
            return False
        elif point[1] > rect[3]:
            return False
        return True

    # Draw a point
    def draw_point(self, img, p, color):
        cv2.circle(img, p, 2, color, cv2.FILLED, cv2.LINE_AA, 0)

    # Draw delaunay triangles
    def draw_delaunay(self, img, subdiv, delaunay_color):
        triangle_list = subdiv.getTriangleList()
        size = img.shape
        r = (0, 0, size[1], size[0])

        for t in triangle_list:
            pt1 = (int(t[0]), int(t[1]))
            pt2 = (int(t[2]), int(t[3]))
            pt3 = (int(t[4]), int(t[5]))

            if self.rect_contains(r, pt1) and self.rect_contains(r, pt2) and \
                self.rect_contains(r, pt3):
                cv2.line(img, pt1, pt2, delaunay_color, 1, cv2.LINE_AA, 0)
                cv2.line(img, pt2, pt3, delaunay_color, 1, cv2.LINE_AA, 0)
                cv2.line(img, pt3, pt1, delaunay_color, 1, cv2.LINE_AA, 0)

    # Draw voronoi diagram
    def draw_voronoi(self, img, subdiv):
        (facets, centers) = subdiv.getVoronoiFacetList([])

        for i in range(0, len(facets)):
            ifacet_arr = []
            for f in facets[i]:
                ifacet_arr.append(f)

            ifacet = np.array(ifacet_arr, int)
            color = (random.randint(0, 255), random.randint(0, 255),\
                     random.randint(0, 255))

            cv2.fillConvexPoly(img, ifacet, color, cv2.LINE_AA, 0)
            ifacets = np.array([ifacet])
            cv2.polylines(img, ifacets, True, (0, 0, 0), 1, cv2.LINE_AA, 0)
            cv2.circle(img, (int(centers[i][0]), int(centers[i][1])), 3,\
                       (0, 0, 0), cv2.FILLED, cv2.LINE_AA, 0)

    def get_triangle_list(self, img, points):
        # Rectangle to be used with Subdiv2D
        size = img.shape
        rect = (0, 0, size[1], size[0])

        # Create an instance of Subdiv2D
        subdiv = cv2.Subdiv2D(rect)

        # Insert points into subdiv
        for p in points:
            x, y = p
            if x < 0: x = 0
            elif x >= size[1]: x = size[1]-1
            if y < 0: y = 0
            elif y >= size[0]: y = size[0]-1
            subdiv.insert((x, y))
        triangle_list = subdiv.getTriangleList().tolist()
        return triangle_list

    def save_triangle_list(self, tris, rect, points, filename):
        dtris = []
        for t in tris:
            pt = []
            pt.append((t[0], t[1]))
            pt.append((t[2], t[3]))
            pt.append((t[4], t[5]))

            pt1 = (t[0], t[1])
            pt2 = (t[2], t[3])
            pt3 = (t[4], t[5])

            if self.rect_contains(rect, pt1) and self.rect_contains(rect, pt2) \
                and self.rect_contains(rect, pt3):
                ind = []
                for j in range(0, 3):
                    for k in range(0, len(points)):
                        if(abs(pt[j][0] - points[k][0]) < 1.0 and abs(pt[j][1] - points[k][1]) < 1.0):
                            ind.append(k)
                if len(ind) == 3:
                    dtris.append((ind[0], ind[1], ind[2]))

        with open("data/test/triangles_" + filename + ".txt", "w") as file:
        # with open("data/triangle_list/" + filename + ".txt", "w") as file:
            for el in dtris:
                file.write('{:.0f} {:.0f} {:.0f}'.format(el[0], el[1], el[2]))
                file.write("\n")


if __name__ == '__main__':
    # Turn on animation while drawing triangles
    animate = False
    DEBUG = False

    # Define window names
    win_delaunay = "Delaunay Triangulation"
    win_voronoi = "Voronoi Diagram"

    triangulation = DelaunayTriangulation()

    # Define colors for drawing.
    delaunay_color = (255, 255, 255)
    points_color = (0, 0, 255)

    # Read in the image.
    img = cv2.imread("data/test/img_02.jpg")

    # Keep a copy around
    img_orig = img.copy()

    # Rectangle to be used with Subdiv2D
    size = img.shape
    rect = (0, 0, size[1], size[0])

    # Create an instance of Subdiv2D
    subdiv = cv2.Subdiv2D(rect)

    # Create an array of points
    points = []

    # Read in the points from a text file
    with open("data/test/points_img_02.txt") as file:
        line = file.readline()
        coordinates = line.split(' ')
        # remove filename
        coordinates.pop(0)
        for i in range(0, len(coordinates), 2):
            x = coordinates[i]
            y = coordinates[i+1]
            points.append((int(x), int(y)))

    # print(points)

    # Insert points into subdiv
    triangle_list = []
    for p in points:
        subdiv.insert((p[0], p[1]))

        # Show animation
        if animate:
            img_copy = img_orig.copy()
            # Draw delaunay triangles
            triangulation.draw_delaunay(img_copy, subdiv, (255, 255, 255))
            if DEBUG:
                cv2.imshow(win_delaunay, img_copy)
                cv2.waitKey(20)

    triangulation.save_triangle_list(triangulation.get_triangle_list(img, points), rect, points, 'img_02')

    # Draw delaunay triangles
    triangulation.draw_delaunay(img, subdiv, (255, 255, 255))

    # Draw points
    for p in points:
        triangulation.draw_point(img, p, (0,0,255))

    # Allocate space for Voronoi Diagram
    img_voronoi = np.zeros(img.shape, dtype = img.dtype)

    # Draw Voronoi diagram
    triangulation.draw_voronoi(img_voronoi,subdiv)

    # Show results
    if DEBUG:
        cv2.imshow(win_delaunay,img)
        cv2.imshow(win_voronoi,img_voronoi)
        cv2.waitKey(0)