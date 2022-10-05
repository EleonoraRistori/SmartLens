import os
import cv2
import pickle
import progressbar
import numpy as np
import pandas as pd

from feature_extractor import FeatureExtractor

# Consente l'estrazione delle features dalle immagini il cui path è riportato in result_set.csv

result_set = pd.read_csv('./outputs/result_set.csv')
feature_names = ['MobileNetV1', 'MobileNetV2', 'MobileNetV3Small', 'MobileNetV3Large']
feature_name = feature_names[2]
feature_types = ['classes', 'convolutions']
feature_type = feature_types[1]

if __name__ == '__main__':
    print(f'Creating DB of {feature_name} features (type: {feature_type}) DB.')
    extractor = FeatureExtractor(feature_name, feature_type)
    db = []
    widgets = [
        "Extract features: ", progressbar.Percentage(), " ",
        progressbar.Bar(), " ", progressbar.ETA()
    ]
    pbar = progressbar.ProgressBar(maxval=len(result_set), widgets=widgets).start()
    num_processed_images = 0
    for index, row in result_set.iterrows():
        if not os.path.isfile(row.path):
            print(f"Can't find image: {row.path}")
            continue
        # preprocessing
        opencv_image = cv2.imread(row.path)
        prepared_image = FeatureExtractor.prepare_opencv_image(opencv_image)
        features = extractor.extract(prepared_image)
        if isinstance(features, np.ndarray):
            db.append([features, row.path])
            num_processed_images += 1
        pbar.update(index)
    pbar.finish()

    with open('./features/' + feature_name + '_' + feature_type + '_features.pck', 'wb') as fp:
        pickle.dump(db, fp)
    print(f'Extraction finished: {num_processed_images} processed images. DB saved.')
