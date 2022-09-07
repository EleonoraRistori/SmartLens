# -*- coding: utf-8 -*-
import cv2
import pickle
import argparse
import progressbar
import numpy as np
from scripts import Extractor
from scripts import Retrievor
from preprocessors import AspectAwarePreprocessor
from preprocessors import ImageToArrayPreprocessor

# initialize process
aap = AspectAwarePreprocessor(224, 224)

image = cv2.imread('C:/Users/eleri/Downloads/prova2.jpg')


cv2.imshow("original", image)
cv2.waitKey(0)
image = aap.preprocess(image)

extractor = Extractor("MobileNet")
retrievor = Retrievor('./features/MobileNet_features.pck')

features = extractor.extract(image)

distance = retrievor.search(features, 'euclidean', depth=5)
print(distance)
cv2.imshow("original", image)
cv2.waitKey(0)
