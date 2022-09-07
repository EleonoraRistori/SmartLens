import mysql.connector
import cv2
import os

mydb = mysql.connector.connect(
    host="localhost",
    user="tesi",
    password="tesi",
    database="tesi"
)


def to_db(filename, detail, path):
    mycursor = mydb.cursor()

    sql = "INSERT INTO  imagesforretrieval VALUES (%s, %s,%s)"
    val = (filename, detail, path)
    mycursor.execute(sql, val)

    mydb.commit()


src_directory = 'C:/Users/eleri/PycharmProjects/SmartLens/data/'
db_directory = 'C:/Users/eleri/Desktop/Università/Tesi/Particolari immagini/'
ind = 0
for dir in os.listdir(src_directory):
    for filename in os.listdir(src_directory + dir):
        img = cv2.imread(src_directory + dir + '/' + filename)
        artwork_path = os.path.join(db_directory, dir)
        if not os.path.isdir(artwork_path):
            os.mkdir(artwork_path)
        path = os.path.join(artwork_path, 'original')
        if not os.path.isdir(path):
            os.mkdir(path)
        os.chdir(path + '/')
        cv2.imwrite(str(ind) + ".png", img)
        to_db(dir, 'original', path + '/' + str(ind) + ".png")
        for i in range(0, 2):
            # Cropping an image
            for j in range(0, 2):
                cropped_image = img[i*img.shape[0]//2:(i+1)*img.shape[0]//2, j*img.shape[1]//2:(j+1)*img.shape[1]//2]
                path = os.path.join(artwork_path, 'detail' + str(i) + "_" + str(j))
                if not os.path.isdir(path):
                    os.mkdir(path)
                os.chdir(path + '/')
                cv2.imwrite(str(ind+i+j) + ".png", cropped_image)
                to_db(dir, 'detail' + str(i) + "_" + str(j), path + '/' + str(ind+i+j) + ".png")
        ind += 1
