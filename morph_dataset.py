import pandas
import re
import cv2
import glob
from delaunay_triangulation import DelaunayTriangulation
import morphing


def save_list(triangulation, df):
    for i in range(len(df.index)):
        filename = df.iloc[i, 0]
        img = cv2.imread("./data\\UTKFace\\" + filename + ".jpg.chip.jpg")
        pts = df.values[i, 1:-3].tolist()

        points = []
        for i in range(0, len(pts), 2):
            x = pts[i]
            y = pts[i+1]
            points.append((int(x), int(y)))

        try:
            rect = (0, 0, img.shape[1], img.shape[0])
            tris = triangulation.get_triangle_list(img, points)
            # print(filename)
            triangulation.save_triangle_list(tris, rect, points, filename)
        except:
            print("Error ", filename)
            # pass

def weight_points(string):
    points = []
    temp = []
    pts = data.loc[(data[0].str.startswith(string))]
    if pts.shape[0] == 0:
        # print("No data found for " + string)
        return None

    for i in range(1, 137):
        temp.append(pts.iloc[:, i].mean())

    for i in range(0, len(temp), 2):
        points.append((round(temp[i]), round(temp[i+1])))
    return points

def helper(lower, upper, string):
    lower = str(lower)
    temp = weight_points(lower + string)
    temp = pandas.DataFrame(temp)
    k = 1
    for i in range (int(lower)+1, int(upper)+1):
        i = str(i)
        try:
            k += 1
            temp1 = weight_points(i + string)
            temp1 = pandas.DataFrame(temp1)
            temp = temp.add(temp1)
        except:
            continue
    temp = pandas.DataFrame(temp)
    try:
        temp[0] = temp[0].apply(lambda x: round (x / k))
        temp[1] = temp[1].apply(lambda x: round (x / k))
    except:
        return None

    return temp

def get_weighted_points(lower, upper):
    lower = str(lower)
    upper = str(upper)

    temp_m_0 = helper(lower, upper, '_0_0_')
    temp_m_1 = helper(lower, upper, '_0_1_')
    temp_m_2 = helper(lower, upper, '_0_2_')
    temp_m_3 = helper(lower, upper, '_0_3_')
    temp_m_4 = helper(lower, upper, '_0_4_')
    temp_f_0 = helper(lower, upper, '_1_0_')
    temp_f_1 = helper(lower, upper, '_1_1_')
    temp_f_2 = helper(lower, upper, '_1_2_')
    temp_f_3 = helper(lower, upper, '_1_3_')
    temp_f_4 = helper(lower, upper, '_1_4_')

    return (temp_m_0, temp_m_1, temp_m_2, temp_m_3, temp_m_4, temp_f_0, temp_f_1, temp_f_2, temp_f_3, temp_f_4)

def save_point(df_points, lower, upper):
    lower = str(lower)
    upper = str(upper)
    temp_m_0, temp_m_1, temp_m_2, temp_m_3, temp_m_4, temp_f_0, temp_f_1, temp_f_2, temp_f_3, temp_f_4 = df_points
    try:
        temp_m_0.to_csv('data/morphed_data/points/' + lower + '_' + upper + '_0_0.txt', sep=' ', header=None, index=None)
    except:
        pass
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
            points.append((int(round(float(line[0]))), int(round(float(line[1])))))
    return points


if __name__ == '__main__':
    # create triangle list
    # # read data
    data = pandas.read_csv('data/landmark_list/landmark_list.txt', sep=' ', header=None)

    data[0] = data[0].apply(lambda x: re.sub(r'.jpg', '', x))
    data['age'] = data[0].apply(lambda x: int(x.split('_')[0]))
    data['gender'] = data[0].apply(lambda x: x.split('_')[1])
    data['race'] = data[0].apply(lambda x: x.split('_')[2])

    # get triangles lists
    print("Get triangle lists...")
    triangulation = DelaunayTriangulation()
    save_list(triangulation, data)
    print()

    # splitting data
    gender = {0: 'male', 1: 'female'}
    race = {0: 'white', 1: 'black', 2: 'asian', 3: 'indian', 4: 'others'}

    filepaths = glob.glob("./data/triangle_list/*.txt")
    filenames = []
    for filepath in filepaths:
        filenames.append(filepath.split('\\')[1].split('.')[0])

    files = pandas.DataFrame(data=filenames)
    files['age'] = files[0].copy().apply(lambda x: int(x.split('_')[0]))
    files['gender'] = files[0].copy().apply(lambda x: int(x.split('_')[1]))
    files['race'] = files[0].copy().apply(lambda x: int(x.split('_')[2]))

    # filter data with files
    data = data.loc[data[0].isin(files[0])]
    # split data into groups
    data_0_1 = data.loc[(data['age'] < 2)].sort_values(by=['gender'])
    data_2_3 = data.loc[(data['age'] >= 2) & (data['age'] < 3)].sort_values(by=['gender'])
    data_7_9 = data.loc[(data['age'] >= 7) & (data['age'] <= 9)].sort_values(by=['gender'])
    data_13_15 = data.loc[(data['age'] >= 13) & (data['age'] <= 15)].sort_values(by=['gender'])
    data_25_34 = data.loc[(data['age'] >= 25) & (data['age'] <= 34)].sort_values(by=['gender'])
    data_35_46 = data.loc[(data['age'] >= 35) & (data['age'] <= 46)].sort_values(by=['gender'])
    data_68_80 = data.loc[(data['age'] >= 68) & (data['age'] <= 116)].sort_values(by=['gender'])

    # morphing data
    print("Get morphed points...")
    save_point(get_weighted_points(1, 1), 1, 1)
    save_point(get_weighted_points(2, 3), 2, 3)
    save_point(get_weighted_points(7, 9), 7, 9)
    save_point(get_weighted_points(13, 15), 13, 15)
    save_point(get_weighted_points(25, 34), 25, 34)
    save_point(get_weighted_points(35, 46), 35, 46)
    save_point(get_weighted_points(68, 80), 68, 80)
    print()

    def morph(df, lower, upper):
        for i in range(0, 5):
            data_m = df.loc[(df['gender'] == '0') & (df['race'] == str(i))]
            data_f = df.loc[(df['gender'] == '1') & (df['race'] == str(i))]
            # print(lower, upper, i)
            # print(data_m.shape, data_f.shape)
            # print(df)
            try:
                morphing.bulk_morph(lower, upper, ('0_' + str(i)), data_m)
            except:
                pass
            try:
                morphing.bulk_morph(lower, upper, ('1_' + str(i)), data_f)
            except:
                pass

    print("Morphing data...")
    morph(data_0_1, 1, 1)
    morph(data_2_3, 2, 3)
    morph(data_7_9, 7, 9)
    morph(data_13_15, 13, 15)
    morph(data_25_34, 25, 34)
    morph(data_35_46, 35, 46)
    morph(data_68_80, 68, 80)
    print("Done")