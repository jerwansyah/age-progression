# Age Progression

## Libraries used

- OpenCV
- Dlib
- Numpy
- Pandas

## How to run

1. Run the following commands

```sh
curl http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2 --output .\data\shape_predictor_68_face_landmarks.dat.bz2
mkdir data
tar -xvzf .\data\shape_predictor_68_face_landmarks.dat.bz2 -C .\data\shape_predictor_68_face_landmarks.dat
```

2. Download face dataset

- Download UTKFace.tar.gz from this [link](https://drive.google.com/drive/folders/0BxYys69jI14kU0I1YUQyY1ZDRUE?usp=sharing) and move the extracted folder to data (final path: `data/UTKFace`)
- Download landmark lists from this [link](https://drive.google.com/open?id=0BxYys69jI14kS1lmbW1jbkFHaW8) and move the txt files to data/landmark_list.

## Filename guide

Label: [age]\_[gender]\_[race]\_[date&time].jpg

- [age] is an integer from 0 to 116, indicating the age
- [gender] is either 0 (male) or 1 (female)
- [race] is an integer from 0 to 4, denoting White, Black, Asian, Indian, and Others (like Hispanic, Latino, Middle Eastern).
- [date&time] is in the format of yyyymmddHHMMSSFFF, showing the date and time an image was collected to UTKFace

## Troubleshooting

- In landmark_list_part3.txt line 123, there should not be a space before .jpg

## References

- https://susanqq.github.io/UTKFace/
