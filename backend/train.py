from pathlib import Path
import os

import numpy as np
from PIL import Image, ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

from feature_extractor import FeatureExtractor
import pickle

if __name__ == '__main__':
    fe = FeatureExtractor()

    arr = None
    batch_size = 128
    count = 0
    batch_count = 0
    idx2path = {}

    img_dir = "../Mock data/Ảnh nhãn - cropped"
    for path in sorted(os.listdir(img_dir)):
        img_path = os.path.join(img_dir, path)
        feature = fe.extract(img=Image.open(img_path))
        feature_path = Path("./feature/all") / (path[0:-4] + ".npy")  # e.g., ./static/feature/xxx.npy
        # save to feature/all
        np.save(feature_path, feature) # for normal search

        # save to feature/batch
        if arr is not None:
            arr = np.append(arr, feature, axis=0)
            count += 1
        else:
            arr = feature
            count = 0

        idx2path[batch_size * batch_count + count] = img_path
        print(batch_size * batch_count + count, img_path)
        if count + 1 == batch_size:
            np.save(f"feature/batch/{batch_count}.npy", arr)
            batch_count += 1
            arr = None
            count = 0
    print(count)
    print(idx2path)
    np.save(f"feature/batch/{batch_count}.npy", arr)
    pickle.dump(idx2path, open("idx2path.pkl", "wb"))
