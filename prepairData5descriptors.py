import cv2
import os

src_directory = 'C:/Users/eleri/PycharmProjects/SmartLens - v2/data/'
db_directory = 'C:/Users/eleri/PycharmProjects/SmartLens - v2/Particolari immagini/'
ind = 0
for dir in os.listdir(src_directory):
    for filename in os.listdir(src_directory + dir):
        if filename == 'seed_000.png':
            img = cv2.imread(src_directory + dir + '/' + filename)
            artwork_path = os.path.join(db_directory, dir)
            if not os.path.isdir(artwork_path):
                os.mkdir(artwork_path)

            os.chdir(artwork_path)
            cv2.imwrite("original.png", img)
            for i in range(0, 2):
                # Cropping an image
                for j in range(0, 2):
                    cropped_image = img[i*img.shape[0]//3:(i+1)*img.shape[0]//3*2, j*img.shape[1]//3:(j+1)*img.shape[1]//3*2]

                    cv2.imwrite(str(i) + "_" + str(j) + ".png", cropped_image)
            ind += 1
            central_img = img[img.shape[0]//6:img.shape[0]*5//6, img.shape[1]//6:img.shape[1]*5//6]
            cv2.imwrite("central.png", central_img)
