import pandas

# # read the data from the file
# data1 = pandas.read_csv('data/landmark_list/landmark_list_part1.txt', sep=' ', header=None)
# data2 = pandas.read_csv('data/landmark_list/landmark_list_part2.txt', sep=' ', header=None)
# data3 = pandas.read_csv('data/landmark_list/landmark_list_part3.txt', sep=' ', header=None)

# # concatenate the data
# data = pandas.concat([data1, data2, data3])

# # add age column to data
# data['age'] = data[0].apply(lambda x: int(x.split('_')[0]))

# # sort the data
# data.sort_values(by=['age'], inplace=True)
# data.drop('age', axis=1, inplace=True)
# data.drop(columns=[137], axis=1, inplace=True)

# # save the data
# data.to_csv('data/landmark_list/landmark_list.txt', sep=' ', header=False, index=False)

#########

# read the data from the file
data = pandas.read_csv('data/landmark_list/landmark_list.txt', sep=' ', header=None)

data['age'] = data[0].apply(lambda x: int(x.split('_')[0]))
data['gender'] = data[0].apply(lambda x: x.split('_')[1])
# data['gender'] = data['gender'].apply(lambda x: int(x))
data['race'] = data[0].apply(lambda x: x.split('_')[2])
# data['race'] = data['race'].apply(lambda x: int(x))

print(data.head())