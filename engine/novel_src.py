# -*- coding: utf=8 -*-
# @Time: 2023/12/17 
# @Author: Johnson Geng
# @FIle: novel_src.py 
# @Description: Novel家族分类模型

import os
import joblib
import mahotas
import numpy as np
from math import log
import mahotas.features
import engine.novel_strings as strings
import engine.novel_entropy as entropy
from mahotas.features.lbp import lbp
from utils.path_loader import *

# Novel家族分类模型
class NovelFamily:

    def __init__(self):
        self.model = joblib.load(NOVEL_FAMILY_PATH)
        self.scaler = joblib.load(NOVEL_SCALER_PATH)
        self.feature_vector = []
        self.family_map = {'1':'Backdoor', '3':'DoS', '4':'Email', '5':'Exploit', '6':'Worm', '7':'Rootkit'}


    # 1-gram特征：统计每个1-gram字节出现的频率
    def _1gram_feature(self, byte_code):

        OneByte = [0] * 16 ** 2
        for row in byte_code:
            codes = row.strip().split()
            # Convert code to 1byte
            OneByteCode = []
            for i in codes:
                if i != '??':
                    OneByteCode += [int(i, 16)]

            # Calculate the frequency of 1byte
            for i in OneByteCode:
                OneByte[i] += 1
        return OneByte

    # 2.Metadata特征：包括二进制文件的大小以及起始地址
    def metadata_feature(self, file_path, file):

        # 文件大小
        meta_data = []
        stat_info = os.stat(file_path)
        file_size = stat_info.st_size
        meta_data.append(file_size)

        # 起始地址
        first_line = file.readline().split()
        offset = first_line[0]
        dec = int(offset, 16)
        meta_data.append(dec)

        return meta_data

    # 3.Entropy特征：滑动窗口内的信息熵大小
    def entropy_feature(self, file_name):

        ents = entropy.get_feats([entropy.get_entropy_features(file_name)])

        return ents[0]

    # 4.IMAGE1特征：
    def byte_image1(self, byte_code):

        img_feat = []
        img = self.byte_make_image(byte_code)
        features = mahotas.features.haralick(img)
        for i in range(len(features)):
            for j in range(len(features[0])):
                img_feat.append(features[i][j])

        return img_feat

    # 4.IMAGE2特征：
    def byte_image2(self, byte_code):

        img = self.byte_make_image(byte_code)
        spoints = lbp(img, 10, 10, ignore_zeros=False)

        return spoints.tolist()

    def byte_make_image(self, byte_code):

        img_array = []

        for row in byte_code:
            xx = row.split()
            if len(xx) != 16:
                continue
            img_array.append([int(i, 16) if i != '??' else 0 for i in xx])
        img_array = np.array(img_array)
        if img_array.shape[1] != 16:
            assert (False)
        b = int((img_array.shape[0] * 16) ** (0.5))
        b = 2 ** (int(log(b) / log(2)) + 1)
        a = int(img_array.shape[0] * 16 / b)
        img_array = img_array[:int(a * b / 16), :]
        img_array = np.reshape(img_array, (a, b))

        return img_array

    # 5.String Length特征：字符串长度特征
    def string_length_feature(self, byte_data):

        strs_len = strings.extract_length([strings.get_strings(byte_data)])

        return strs_len[0].tolist()



    # 从Bytes文件提取特特征
    def extract(self, bytes_path):


        # 十六进制特征处理
        with open(bytes_path, 'r+') as f:
            raw_data = f.readlines()

        for i in range(len(raw_data)):
            raw_data[i] = raw_data[i][9:]

        self.feature_vector.extend(self._1gram_feature(raw_data))
        self.feature_vector.extend(self.metadata_feature(bytes_path, open(bytes_path, 'r+')))
        self.feature_vector.extend(self.entropy_feature(raw_data))
        self.feature_vector.extend(self.byte_image1(raw_data))
        self.feature_vector.extend(self.byte_image2(raw_data))
        self.feature_vector.extend(self.string_length_feature(raw_data))



    # 读取特征进行分类
    def predict(self):

        feature_scaled = self.scaler(self.feature_vector)

        pred_family = self.model.predict(feature_scaled)
        prob = self.model.y_pred_prob(feature_scaled)

        return self.family_map[pred_family], prob



