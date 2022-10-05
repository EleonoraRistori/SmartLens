import cv2
import os

# Script che consente la partizione delle immagini in 4 parti per il retrieval.

src_directory = 'C:/Users/eleri/PycharmProjects/SmartLens/data/'
db_directory = 'C:/Users/eleri/PycharmProjects/SmartLens/Particolari immagini/'

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
                    cropped_image = img[i * img.shape[0] // 2:(i + 1) * img.shape[0] // 2,
                                    j * img.shape[1] // 2:(j + 1) * img.shape[1] // 2]
                    cv2.imwrite(str(i) + "_" + str(j) + ".png", cropped_image)
