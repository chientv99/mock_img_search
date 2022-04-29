import sys
from PIL import Image
from image_search import autofaiss_img_search


def main(filename):
    img = Image.open(filename)
    scores = autofaiss_img_search(filename)
    print(len(scores))
    print(scores)

if __name__ == '__main__' :
    # if len(sys.argv) < 2: 
    #     print("Input a image test file: python3 test.py <filename>");
    #     exit(1)
    filename = '../Mock data/Ảnh chụp/Chateau-Marojallia-Label.jpg'
    main(filename)

