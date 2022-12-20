#!/usr/bin/env python

import numpy as np
import cv2
import sys
import pandas
import glob
from delaunay_triangulation import DelaunayTriangulation

# Read filename from text file
def read_filename(path):
    filenames = pandas.read_csv(path, header=None, sep=' ')
    filenames = filenames[0].tolist()
    return filenames

# Read points from text file
def read_points(path, oneline=True):
    # Create an array of points
    points = []

    # Read in the points from a text file
    with open(path) as file:
        if oneline:
            for line in file:
                coordinates = line.split(' ')
                # remove filename
                coordinates.pop(0)
                temp = []
                for i in range(0, len(coordinates), 2):
                    x = coordinates[i]
                    y = coordinates[i+1]
                    temp.append((int(x), int(y)))
                points.append(temp)
        else:
            for line in file:
                line = line.split(' ')
                x = line[0]
                y = line[1]
                points.append((int(float(x)), int(float(y))))

    return points

# Apply affine transform calculated using srcTri and dstTri to src and
# output an image of size.
def apply_affine_transform(src, src_tri, dst_tri, size):
    # Given a pair of triangles, find the affine transform.
    warp_mat = cv2.getAffineTransform(np.float32(src_tri), np.float32(dst_tri))

    # Apply the Affine Transform just found to the src image
    dst = cv2.warpAffine(src, warp_mat, (size[0], size[1]), None, flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT_101)

    return dst


# Warps and alpha blends triangular regions from img1 and img2 to img
def morph_triangle(img1, img2, img, t1, t2, t, alpha, bulk=False):
    # Find bounding rectangle for each triangle
    r1 = cv2.boundingRect(np.float32([t1]))
    r2 = cv2.boundingRect(np.float32([t2]))
    r = cv2.boundingRect(np.float32([t]))

    # Offset points by left top corner of the respective rectangles
    t1_rect = []
    t2_rect = []
    t_rect = []

    for i in range(0, 3):
        t_rect.append(((t[i][0] - r[0]),(t[i][1] - r[1])))
        t1_rect.append(((t1[i][0] - r1[0]),(t1[i][1] - r1[1])))
        t2_rect.append(((t2[i][0] - r2[0]),(t2[i][1] - r2[1])))

    # Get mask by filling triangle
    mask = np.zeros((r[3], r[2], 3), dtype = np.float32)
    cv2.fillConvexPoly(mask, np.int32(t_rect), (1.0, 1.0, 1.0), 16, 0)

    # Apply warpImage to small rectangular patches
    img1_rect = img1[r1[1]:r1[1] + r1[3], r1[0]:r1[0] + r1[2]]
    img2_rect = img2[r2[1]:r2[1] + r2[3], r2[0]:r2[0] + r2[2]]

    size = (r[2], r[3])
    warp_img1 = apply_affine_transform(img1_rect, t1_rect, t_rect, size)
    warp_img2 = apply_affine_transform(img2_rect, t2_rect, t_rect, size)

    # Alpha blend rectangular patches
    img_rect = (1.0 - alpha) * warp_img1 + alpha * warp_img2
    if bulk:
        img_rect = alpha * warp_img1 + warp_img2

    # Copy triangular region of the rectangular patch to the output image
    img[r[1]:r[1]+r[3], r[0]:r[0]+r[2]] = img[r[1]:r[1]+r[3], r[0]:r[0]+r[2]] * ( 1 - mask ) + img_rect * mask

def bulk_morph(lower, upper, criteria, df):
    filename_output = str(lower) + '_' + str(upper) + '_' + str(criteria)

    files = df[0].tolist()
    n_files = len(files) if len(files) > 0 else 1
    alpha = 1 / n_files

    points = read_points('data/morphed_data/points/' + filename_output + '.txt', oneline=False)
    img1 = cv2.imread('./data/UTKFace/' + files[0] + '.jpg.chip.jpg')
    temp_image = np.zeros(img1.shape, dtype = img1.dtype)
    img_morph = np.zeros(img1.shape, dtype = img1.dtype)
    rect = (0, 0, img_morph.shape[1], img_morph.shape[0])

    triangulation = DelaunayTriangulation()
    tris = triangulation.get_triangle_list(img_morph, points)
    triangulation.save_triangle_list(tris, rect, points, 'temp')
    tris = read_triangles('data/test/triangles_temp.txt')

    for i in range(n_files):
        # Read images
        # img1 = cv2.imread('./data/morphed_data/images/' + filename_data + '.txt')
        file = df.iloc[i].values
        filename = file[0]
        temp = file[1:137].tolist()
        points = []
        for j in range(0, len(temp), 2):
            points.append((temp[j], temp[j+1]))

        img1 = cv2.imread('./data/UTKFace/' + filename + '.jpg.chip.jpg')

        # Convert Mat to float data type
        img1 = np.float32(img1)

        # Read array of corresponding points
        points1 = read_points('data/test/points_img_01.txt')[0]

        # Read triangles
        # tris1 = read_triangles('data/triangle_list/' + filename + '.txt')
        temp_image = img_morph.copy()
        for i in tris:
            x, y, z = i

            x = int(x)
            y = int(y)
            z = int(z)

            t1 = [points1[x], points1[y], points1[z]]
            t = [points[x],  points[y],  points[z]]
            t2 = t

            # Morph one triangle at a time.
            morph_triangle(img1, temp_image, img_morph, t1, t2, t, alpha, bulk=True)
            cv2.imshow("Morphed Face", np.uint8(img_morph))
        cv2.waitKey(1)

    # Display Result
    # cv2.imshow("Morphed Face", np.uint8(img_morph))
    # cv2.waitKey(0)
    # save image
    cv2.imwrite('./data/morphed_data/images/morphed_' + filename_output + '.jpg', np.uint8(img_morph))

def read_triangles(path):
    triangles = []
    with open(path) as file:
        for line in file:
            a, b, c = line.strip().split(' ')
            triangles.append((int(a), int(b), int(c)))
    return triangles


if __name__ == '__main__':
    filename_data = '1_1_0_0'
    filename_input = 'img_01'

    # Read images
    # img1 = cv2.imread('./data/morphed_data/images/' + filename_data + '.txt')
    img1 = cv2.imread('./data/test/' + 'img_01' + '.jpg')
    img2 = cv2.imread('./data/test/' + 'img_02' + '.jpg')

    # Convert Mat to float data type
    img1 = np.float32(img1)
    img2 = np.float32(img2)

    # Read array of corresponding points
    alpha = 0.5
    # points1 = read_points('data/morphed_data/points/' + filename_data + '.txt', oneline=False)
    points1 = read_points('data/test/points_img_01.txt')[0]
    points2 = read_points('data/test/points_img_02.txt')[0]
    points = []

    # Compute weighted average point coordinates
    for i in range(0, len(points1)):
        points1x, points1y = points1[i]
        points2x, points2y = points2[i]
        x = int(round((1 - alpha) * float(points1x) + alpha * float(points2x)))
        y = int(round((1 - alpha) * float(points1y) + alpha * float(points2y)))
        points.append((x,y))

    # Allocate space for final output
    img_morph = np.zeros(img1.shape, dtype = img1.dtype)
    rect = (0, 0, img_morph.shape[1], img_morph.shape[0])

    # Read triangles
    tris1 = read_triangles('data/test/triangles_img_01.txt')
    tris2 = read_triangles('data/test/triangles_img_02.txt')
    triangulation = DelaunayTriangulation()
    tris = triangulation.get_triangle_list(img_morph, points)
    triangulation.save_triangle_list(tris, rect, points, 'temp')
    tris = read_triangles('data/test/triangles_temp.txt')

    for i in tris:
        x, y, z = i

        x = int(x)
        y = int(y)
        z = int(z)

        t1 = [points1[x], points1[y], points1[z]]
        t2 = [points2[x], points2[y], points2[z]]
        t = [points[x],  points[y],  points[z]]

        # Morph one triangle at a time.
        morph_triangle(img1, img2, img_morph, t1, t2, t, alpha)

    # Display Result
    cv2.imshow("Morphed Face", np.uint8(img_morph))
    cv2.waitKey(0)