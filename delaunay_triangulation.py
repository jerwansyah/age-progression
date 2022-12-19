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
        triangleList = subdiv.getTriangleList()
        size = img.shape
        r = (0, 0, size[1], size[0])

        for t in triangleList:
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


if __name__ == '__main__':
    # Define window names
    win_delaunay = "Delaunay Triangulation"
    win_voronoi = "Voronoi Diagram"

    triangulation = DelaunayTriangulation()

    # Turn on animation while drawing triangles
    animate = False

    # Define colors for drawing.
    delaunay_color = (255, 255, 255)
    points_color = (0, 0, 255)

    # Read in the image.
    img = cv2.imread("data/UTKFace/12_1_0_20170109204805155.jpg.chip.jpg")

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
    with open("data/points.txt") as file:
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
    for p in points:
        subdiv.insert(p)

        # Show animation
        if animate:
            img_copy = img_orig.copy()
            # Draw delaunay triangles
            triangulation.draw_delaunay(img_copy, subdiv, (255, 255, 255))
            cv2.imshow(win_delaunay, img_copy)
            cv2.waitKey(100)

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
    cv2.imshow(win_delaunay,img)
    cv2.imshow(win_voronoi,img_voronoi)
    cv2.waitKey(0)