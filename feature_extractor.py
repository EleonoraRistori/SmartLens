import cv2
from PIL import Image
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.models import load_model
from tensorflow.keras.utils import img_to_array
from tensorflow.keras.applications import MobileNet  # V1
from tensorflow.keras.applications import MobileNetV2  # V2
from tensorflow.keras.applications import MobileNetV3Small # V3 Small
from tensorflow.keras.applications import MobileNetV3Large # V3 Small


class FeatureExtractor:
    def __init__(self, desc_type='MobileNetV3Small', feat_type='classes'):
        self.desc_type = desc_type
        self.feat_type = feat_type
        if self.feat_type not in ['convolutions', 'classes']:
            raise ValueError('Feature type ' + self.feat_type + ' is not supported')
        self.preprocess = None
        self.extractor = self.__create_extractor()
        self.inW = 224
        self.inH = 224

    def __create_extractor(self):
        if self.desc_type == 'MobileNetV1':
            self.preprocess = tf.keras.applications.mobilenet.preprocess_input
            if self.feat_type == 'convolutions':
                model = MobileNet(weights='imagenet', include_top=False, pooling="avg", input_shape=(224, 224, 3))  # 1024d
                # return Model(inputs=model.input, outputs=model.layers[-4].output)  # 1024d - use [-4] to get from dropout layer, use [-5] to get from ReLu layer as in include_top=False
            if self.feat_type == 'classes':
                model = MobileNet(weights='imagenet', include_top=True, input_shape=(224, 224, 3))  # 1000d
            return model
        if self.desc_type == 'MobileNetV2':
            self.preprocess = tf.keras.applications.mobilenet_v2.preprocess_input
            if self.feat_type == 'convolutions':
                model = MobileNetV2(weights='imagenet', include_top=False, pooling="avg", input_shape=(224, 224, 3))  # 1280d
            if self.feat_type == 'classes':
                model = MobileNetV2(weights='imagenet', include_top=True, input_shape=(224, 224, 3))  # 1000d
            return model
        if self.desc_type == 'MobileNetV3Small':
            self.preprocess = tf.keras.applications.mobilenet_v3.preprocess_input
            model = MobileNetV3Small(weights='imagenet', include_top=True, input_shape=(224, 224, 3))
            if self.feat_type == 'convolutions':
                # XXX using include_top=False, pooling="avg" leads to a 960d descriptor
                return Model(inputs=model.input, outputs=model.layers[-4].output)  # 1024d
            if self.feat_type == 'classes':
                return model  # 1000d
        if self.desc_type == 'MobileNetV3Large':
            self.preprocess = tf.keras.applications.mobilenet_v3.preprocess_input
            model = MobileNetV3Large(weights='imagenet', include_top=True, input_shape=(224, 224, 3))
            if self.feat_type == 'convolutions':
                # XXX using include_top=False, pooling="avg" leads to a 960d descriptor
                return Model(inputs=model.input, outputs=model.layers[-4].output)  # 1024d
            if self.feat_type == 'classes':
                return model  # 1000d
        raise ValueError('Feature name unknown: ' + self.desc_type)

    @staticmethod
    def prepare_opencv_image(opencv_image):
        # convert the color from BGR to RGB then convert to PIL array
        cvt_image = cv2.cvtColor(opencv_image, cv2.COLOR_BGR2RGB)
        im_pil = Image.fromarray(cvt_image)

        # resize the array (image) then PIL image
        im_resized = im_pil.resize((224, 224))
        img_array = img_to_array(im_resized)  # from PIL to Numpy
        image_array_expanded = np.expand_dims(img_array, axis=0)
        return image_array_expanded

    @staticmethod
    def prepare_keras_image(keras_image):
        img_array = img_to_array(keras_image)
        image_array_expanded = np.expand_dims(img_array, axis=0)
        return image_array_expanded

    def extract(self, prepared_image):
        preprocessed_image = self.preprocess(prepared_image)
        return self.extractor.predict(preprocessed_image)[0].flatten()
