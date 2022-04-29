import os
from pathlib import Path

import faiss
import numpy as np

from PIL import Image

from pyretri.config import get_defaults_cfg, setup_cfg
from pyretri.datasets import build_transformers
from pyretri.models import build_model
from pyretri.extract import build_extract_helper
from pyretri.index import build_index_helper, feature_loader
from pyretri.evaluate import build_evaluate_helper

from feature_extractor import FeatureExtractor
import pickle
import sys
# Read image features
fe = FeatureExtractor()
features = []
img_paths = []
autofaiss_img_paths = []

autofaiss_model = faiss.read_index('feature/knn.index')

autofaiss_idx2path = {}
with open("idx2path.pkl", "rb") as f:
    autofaiss_idx2path = pickle.load(f)
print(len(autofaiss_idx2path))
def autofaiss_img_search(img_path):
    img = Image.open(img_path)  # PIL image
    query_vector = fe.extract(img)
    distances, indices = autofaiss_model.search(query_vector.reshape(1, -1), 5)
    print(distances, indices)
    result_paths = []
    for idx in indices[0]:
        if idx != -1:
            result_paths.append(str(autofaiss_idx2path[idx]))
    # print(result_paths)
    return result_paths

def image_paths_to_product_list(image_paths):
    """
    From list of product images, get 10 products from this list
    Note: one product may have more than 1 image
    """
    product_list = []
    for image_path in image_paths:
        name = image_path.split("/")[-1]
        product_id = name.split("-")[0]
        image_path = "/".join(image_path.split("/")[1:])
        if product_id not in product_list:
            product_list.append({"product_id": product_id, "image": image_path})
    return product_list[:10]

if __name__ == "__main__":
    # paths = pyretrive_img_search("images/chao/54625005-0.jpg")
    # print(image_paths_to_product_list(paths))
    paths = autofaiss_img_search("/home/chientv/Downloads/Mock data-20220325T091641Z-001/Mock data/Ảnh chụp/Chateau-Marojallia-Label.jpg")
    print(paths)
    # for i in paths:
    #     print(i)
