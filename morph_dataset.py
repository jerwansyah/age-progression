import pandas
import re
import cv2
from delaunay_triangulation import DelaunayTriangulation


def save_list(triangulation, df):
    for i in range(len(df.index)):
        filename = df.iloc[i, 0]
        img = cv2.imread("data/UTKFace/" + filename + ".jpg.chip.jpg")
        pts = df.values[i, 1:-3].tolist()

        points = []
        for i in range(0, len(pts), 2):
            x = pts[i]
            y = pts[i+1]
            points.append((int(x), int(y)))

        try:
            tris = triangulation.get_triangle_list(img, points)
            triangulation.save_triangle_list(tris, filename)
        except:
            pass


if __name__ == '__main__':
    # read data
    data = pandas.read_csv('data/landmark_list/landmark_list.txt', sep=' ', header=None)

    data[0] = data[0].apply(lambda x: re.sub(r'.jpg', '', x))
    data['age'] = data[0].apply(lambda x: int(x.split('_')[0]))
    data['gender'] = data[0].apply(lambda x: x.split('_')[1])
    data['race'] = data[0].apply(lambda x: x.split('_')[2])

    # get triangles lists
    triangulation = DelaunayTriangulation()
    save_list(triangulation, data)

    age_groups = [0, 2, 4, 7, 10, 13, 16, 20, 25, 35, 46, 57, 68, 116]
    age_groups_labels = [0, 2, 4, 7, 10, 13, 16, 20, 25, 35, 46, 57, 68]
    gender = {0: 'male', 1: 'female'}
    race = {0: 'white', 1: 'black', 2: 'asian', 3: 'indian', 4: 'others'}

    # split data into age groups
    data['age_group'] = pandas.cut(data['age'], bins=age_groups, labels=age_groups_labels, right=False)

    data_0 = data[data['age_group'] == 0].sort_values(by=['gender'])
    data_2 = data[data['age_group'] == 2].sort_values(by=['gender'])
    data_4 = data[data['age_group'] == 4].sort_values(by=['gender'])
    data_7 = data[data['age_group'] == 7].sort_values(by=['gender'])
    data_10 = data[data['age_group'] == 10].sort_values(by=['gender'])
    data_13 = data[data['age_group'] == 13].sort_values(by=['gender'])
    data_16 = data[data['age_group'] == 16].sort_values(by=['gender'])
    data_20 = data[data['age_group'] == 20].sort_values(by=['gender'])
    data_25 = data[data['age_group'] == 25].sort_values(by=['gender'])
    data_35 = data[data['age_group'] == 35].sort_values(by=['gender'])
    data_46 = data[data['age_group'] == 46].sort_values(by=['gender'])
    data_57 = data[data['age_group'] == 57].sort_values(by=['gender'])
    data_68 = data[data['age_group'] == 68].sort_values(by=['gender'])

    # # split data into gender groups
    # data_0_0 = data_0[data_0['gender'] == '0']
    # data_0_1 = data_0[data_0['gender'] == '1']

    # split data into race groups


    # image = cv2.imread('data/UTKFace/12_1_0_20170109204805155.jpg.chip.jpg')
    # # image = cv2.imread('data/UTKFace/12_1_0_20170109204113685.jpg.chip.jpg')
    # shape = detector.detect(image)
    # detector.save_points(shape, 'data/points.txt', '12_1_0_20170109204805155')