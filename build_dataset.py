import os
import csv
import glob
import argparse
import progressbar

# Lo script prepara il file .csv utilizzato da MobileNet per l'estrazione delle features dalle immagini

ap = argparse.ArgumentParser()
ap.add_argument('-i', '--images', help='path of images')
args = vars(ap.parse_args())

# load images
imagePath = glob.glob('./Particolari immagini/*/*.png')

outputPath = './outputs/result_set.csv'

# loop over sets

print('[INFO]: Building {} ...')
# create file if necessary
if not os.path.isfile(outputPath):
    with open(outputPath, 'w') as file:
        writer = csv.writer(file)
        writer.writerow(['path', 'artwork', 'detail'])
# progress bar
widgets = [
    "Writing ...", progressbar.Percentage(), " ",
    progressbar.Bar(), " ", progressbar.ETA()
]
pbar = progressbar.ProgressBar(
    maxval=len(imagePath), widgets=widgets
).start()
for (i, path) in enumerate(imagePath):
    with open(outputPath, 'a+', newline='') as file:
        writer = csv.writer(file)
        rows = path.split(os.path.sep)
        artwork = rows[-2]
        detail = rows[-1]
        writer.writerow([path, artwork, detail])
    pbar.update(i)
pbar.finish()

