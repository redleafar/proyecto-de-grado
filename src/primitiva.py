import argparse
import random
import numpy as np
from PIL import Image

# Workshop “Maleabilidad del one-time-pad”
# Author: Rafael Bermúdez


def create_key(file_name):
    print("Creating key...")
    size = 1024
    image_tensor = np.zeros((size, size, 3), dtype=np.uint8)
    m, i, j = 0, 0, 0
    for m in range(3):
        for i in range(size):
            for j in range(size):
                image_tensor[i][j][m] = random.randint(0, 255)
            j = 0
        i = 0

    img = Image.fromarray(image_tensor, 'RGB')
    img.save(file_name)
    print("Key successfully created and saved!!")
    print("Showing key image...")
    img.show()


def encrypt(image_name, key_name, output_image):
    print("Encrypting image...")

    image = Image.open(image_name)
    image_tensor = np.array(image)

    key = Image.open(key_name)
    key_tensor = np.array(key)

    size = 1024
    ciphered_image_tensor = np.zeros((size, size, 3), dtype=np.uint8)
    m, i, j = 0, 0, 0
    for m in range(3):
        for i in range(size):
            for j in range(size):
                ciphered_image_tensor[i][j][m] = image_tensor[i][j][m] ^ key_tensor[i][j][m]
            j = 0
        i = 0

    img = Image.fromarray(ciphered_image_tensor, 'RGB')
    img.save(output_image)

    print("Image successfully encrypted and saved!!")
    print("Showing encrypted image...")
    img.show()


def find_key(image_name, ciphered_image_name, key_name):
    print("Finding key...")

    image = Image.open(image_name)
    image_tensor = np.array(image)

    ciphered_image = Image.open(ciphered_image_name)
    ciphered_image_tensor = np.array(ciphered_image)

    size = 1024
    key_tensor = np.zeros((size, size, 3), dtype=np.uint8)
    m, i, j = 0, 0, 0
    for m in range(3):
        for i in range(size):
            for j in range(size):
                key_tensor[i][j][m] = image_tensor[i][j][m] ^ ciphered_image_tensor[i][j][m]
            j = 0
        i = 0

    img = Image.fromarray(key_tensor, 'RGB')
    img.save(key_name)

    print("Key successfully found and saved!!")

    print("Checking that the xor result between the key and the plain text image is the encrypted image...")
    same_image = True

    for m in range(3):
        for i in range(size):
            for j in range(size):
                same_image = ((image_tensor[i][j][m] ^ key_tensor[i][j][m]) == ciphered_image_tensor[i][j][
                    m]) and same_image
            j = 0
        i = 0

    if same_image:
        print("It is the encrypted image!!")
    else:
        print("It is not the encrypted image!!")

    print("Showing found key...")
    img.show()


def main():
    output_image = "output.bmp"

    parser = argparse.ArgumentParser(description='Tools for image encryption.')
    group = parser.add_mutually_exclusive_group()

    group.add_argument("-cK", "--create_key", help="Creates a key", action="store_true")
    group.add_argument("-e", "--encrypt", help="Encrypts an image", action="store_true")
    group.add_argument("-fK", "--find_key", help="Finds the key from a ciphered image and a plain text image",
                       action="store_true")
    parser.add_argument("input_image", help="Input images", nargs="?")
    parser.add_argument("key_or_cipher", help="Key or ciphered image", nargs="?")
    parser.add_argument("-o", "--output_image", help="Specifies an output image")
    args = parser.parse_args()

    if args.output_image:
        output_image = args.output_image

    if args.create_key:
        create_key(output_image)
    elif args.encrypt:
        if args.input_image and args.key_or_cipher:
            encrypt(args.input_image, args.key_or_cipher, output_image)
        else:
            parser.error('--encrypt requires an input image and a key')
    elif args.find_key:
        if args.input_image and args.key_or_cipher:
            find_key(args.input_image, args.key_or_cipher, output_image)
        else:
            parser.error('--find_key requires an input image and a ciphered image')


main()
