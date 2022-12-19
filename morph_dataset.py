import pandas
import re
import cv2
import glob
from delaunay_triangulation import DelaunayTriangulation
import morphing


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

def get_data_num(df, string):
    return df.loc[(df[0].str.startswith(string))].shape[0]

# def count_data(df):
#     temp_m_0 = 0
#     temp_m_1 = 0
#     temp_m_2 = 0
#     temp_m_3 = 0
#     temp_m_4 = 0
#     temp_f_0 = 0
#     temp_f_1 = 0
#     temp_f_2 = 0
#     temp_f_3 = 0
#     temp_f_4 = 0
#     for i in range (0, 1+1):
#         temp_m_0 += get_data_num(df, str(i) + '_0_0')
#         temp_m_1 += get_data_num(df, str(i) + '_0_1')
#         temp_m_2 += get_data_num(df, str(i) + '_0_2')
#         temp_m_3 += get_data_num(df, str(i) + '_0_3')
#         temp_m_4 += get_data_num(df, str(i) + '_0_4')
#         temp_f_0 += get_data_num(df, str(i) + '_1_0')
#         temp_f_1 += get_data_num(df, str(i) + '_1_1')
#         temp_f_2 += get_data_num(df, str(i) + '_1_2')
#         temp_f_3 += get_data_num(df, str(i) + '_1_3')
#         temp_f_4 += get_data_num(df, str(i) + '_1_4')
#     temp_m_0 = 1 / temp_m_0 if temp_m_0 != 0 else 0
#     temp_m_1 = 1 / temp_m_1 if temp_m_1 != 0 else 0
#     temp_m_2 = 1 / temp_m_2 if temp_m_2 != 0 else 0
#     temp_m_3 = 1 / temp_m_3 if temp_m_3 != 0 else 0
#     temp_m_4 = 1 / temp_m_4 if temp_m_4 != 0 else 0
#     temp_f_0 = 1 / temp_f_0 if temp_f_0 != 0 else 0
#     temp_f_1 = 1 / temp_f_1 if temp_f_1 != 0 else 0
#     temp_f_2 = 1 / temp_f_2 if temp_f_2 != 0 else 0
#     temp_f_3 = 1 / temp_f_3 if temp_f_3 != 0 else 0
#     temp_f_4 = 1 / temp_f_4 if temp_f_4 != 0 else 0
#     return (temp_m_0, temp_m_1, temp_m_2, temp_m_3, temp_m_4, temp_f_0, temp_f_1, temp_f_2, temp_f_3, temp_f_4)

def weight_points(string):
    points = []
    temp = []
    pts = data.loc[(data[0].str.startswith(string))]
    if pts.shape[0] == 0:
        return None

    for i in range(1, 137):
        temp.append(pts.iloc[:, i].mean())

    for i in range(0, len(temp), 2):
        points.append((round(temp[i]), round(temp[i+1])))

    return points

def helper(lower, upper, string):
    lower = str(lower)
    temp = weight_points(lower + string)
    k = 0
    for i in range (int(lower)+1, int(upper)+1):
        i = str(i)
        try:
            k += 1
            temp += weight_points(i + string)
        except:
            continue
    temp = pandas.DataFrame(temp).apply(lambda x: round (x / k))
    return temp

def get_weighted_points(lower, upper):
    lower = str(lower)
    upper = str(upper)

    temp_m_0 = helper(lower, upper, '_0_0')
    temp_m_1 = helper(lower, upper, '_0_1')
    temp_m_2 = helper(lower, upper, '_0_2')
    temp_m_3 = helper(lower, upper, '_0_3')
    temp_m_4 = helper(lower, upper, '_0_4')
    temp_f_0 = helper(lower, upper, '_1_0')
    temp_f_1 = helper(lower, upper, '_1_1')
    temp_f_2 = helper(lower, upper, '_1_2')
    temp_f_3 = helper(lower, upper, '_1_3')
    temp_f_4 = helper(lower, upper, '_1_4')

    return (temp_m_0, temp_m_1, temp_m_2, temp_m_3, temp_m_4, temp_f_0, temp_f_1, temp_f_2, temp_f_3, temp_f_4)

def save_point(df_points, lower, upper):
    lower = str(lower)
    upper = str(upper)
    temp_m_0, temp_m_1, temp_m_2, temp_m_3, temp_m_4, temp_f_0, temp_f_1, temp_f_2, temp_f_3, temp_f_4 = df_points
    try:
        temp_m_1.to_csv('data/morphed_data/points/' + lower + '_' + upper + '_0_1.txt', sep=' ', header=None, index=None)
    except:
        pass
    try:
        temp_m_2.to_csv('data/morphed_data/points/' + lower + '_' + upper + '_0_2.txt', sep=' ', header=None, index=None)
    except:
        pass
    try:
        temp_m_3.to_csv('data/morphed_data/points/' + lower + '_' + upper + '_0_3.txt', sep=' ', header=None, index=None)
    except:
        pass
    try:
        temp_m_4.to_csv('data/morphed_data/points/' + lower + '_' + upper + '_0_4.txt', sep=' ', header=None, index=None)
    except:
        pass
    try:
        temp_f_0.to_csv('data/morphed_data/points/' + lower + '_' + upper + '_1_0.txt', sep=' ', header=None, index=None)
    except:
        pass
    try:
        temp_f_1.to_csv('data/morphed_data/points/' + lower + '_' + upper + '_1_1.txt', sep=' ', header=None, index=None)
    except:
        pass
    try:
        temp_f_2.to_csv('data/morphed_data/points/' + lower + '_' + upper + '_1_2.txt', sep=' ', header=None, index=None)
    except:
        pass
    try:
        temp_f_3.to_csv('data/morphed_data/points/' + lower + '_' + upper + '_1_3.txt', sep=' ', header=None, index=None)
    except:
        pass
    try:
        temp_f_4.to_csv('data/morphed_data/points/' + lower + '_' + upper + '_1_4.txt', sep=' ', header=None, index=None)
    except:
        pass

    def read_points(path):
        points = []
        with open(path, 'r') as f:
            for line in f:
                line = line.strip()
                line = line.split(' ')
                points.append((int(line[0]), int(line[1])))
        return points


if __name__ == '__main__':
    # create triangle list
    # # read data
    data = pandas.read_csv('data/landmark_list/landmark_list.txt', sep=' ', header=None)

    data[0] = data[0].apply(lambda x: re.sub(r'.jpg', '', x))
    data['age'] = data[0].apply(lambda x: int(x.split('_')[0]))
    data['gender'] = data[0].apply(lambda x: x.split('_')[1])
    data['race'] = data[0].apply(lambda x: x.split('_')[2])

    # # get triangles lists
    triangulation = DelaunayTriangulation()
    save_list(triangulation, data)

    # splitting data
    gender = {0: 'male', 1: 'female'}
    race = {0: 'white', 1: 'black', 2: 'asian', 3: 'indian', 4: 'others'}

    filepaths = glob.glob("./data/triangle_list/*.txt")
    filenames = []
    for filepath in filepaths:
        filenames.append(filepath.split('\\')[1].split('.')[0])

    files = pandas.DataFrame(data=filenames)
    files['age'] = files[0].apply(lambda x: int(x.split('_')[0]))
    files['gender'] = files[0].apply(lambda x: x.split('_')[1])
    files['race'] = files[0].apply(lambda x: x.split('_')[2])

    # split data into groups
    data_0_1 = files.loc[(files['age'] < 2)].sort_values(by=['gender'])
    data_2_3 = files.loc[(files['age'] >= 2) | (files['age'] <= 3)].sort_values(by=['gender'])
    data_7_9 = files.loc[(files['age'] >= 7) | (files['age'] <= 9)].sort_values(by=['gender'])
    data_13_15 = files.loc[(files['age'] >= 13) | (files['age'] <= 15)].sort_values(by=['gender'])
    data_25_34 = files.loc[(files['age'] >= 25) | (files['age'] <= 34)].sort_values(by=['gender'])
    data_35_46 = files.loc[(files['age'] >= 35) | (files['age'] <= 46)].sort_values(by=['gender'])
    data_68_80 = files.loc[(files['age'] >= 68) | (files['age'] <= 116)].sort_values(by=['gender'])

    # morphing data
    # filter data with files
    data = data.loc[data[0].isin(files[0])]
    save_point(get_weighted_points(1, 1), 1, 1)
    save_point(get_weighted_points(2, 3), 2, 3)
    save_point(get_weighted_points(7, 9), 7, 9)
    save_point(get_weighted_points(13, 15), 13, 15)
    save_point(get_weighted_points(25, 34), 25, 34)
    save_point(get_weighted_points(35, 46), 35, 46)
    save_point(get_weighted_points(68, 80), 68, 80)

    points = read_points('data/morphed_data/points/1_1_0_0.txt')

    bulk_morph(1, 1, '0_0', points, data_0_1)

    # image = cv2.imread('data/UTKFace/12_1_0_20170109204805155.jpg.chip.jpg')
    # # image = cv2.imread('data/UTKFace/12_1_0_20170109204113685.jpg.chip.jpg')
    # shape = detector.detect(image)
    # detector.save_points(shape, 'data/points.txt', '12_1_0_20170109204805155')