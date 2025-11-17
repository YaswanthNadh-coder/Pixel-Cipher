from PIL import Image
import random
from crypto import encrypt,decrypt,text_to_bits

#the original format of image won't matter, as pillow decompresses .jpg to give the same pixel data but while saving we'll use .png to perfectly preserve all the pixels

def encode(image_path, message, password):
    try:
        img=Image.open(image_path)
        #img stores an object(instacne of Image class) that holds the meta-data of image and a pointer to the actual image

        img=img.convert("RGB")
        #so that we can uniformly work on every type of image without errors(different modes are RGB, RGBA, L)

        pixels=img.load()
        #.load() returns a pixel access object, basically a 2D grid that is linked with the image object's memory

        img_dim=img.size
        width=img_dim[0]
        height=img_dim[1]
        total_pixels=width*height

        encrypted_message=encrypt(message, password)
        msg_bits=text_to_bits(encrypted_message)
        num_bits=len(msg_bits)

        #METHOD 1: Turned out to be very space inefficient
        #coordinates=[(x,y) for x in range(width) for y in range(height)]
        #gives a list of 2-tuples containing all the possible coordinates in an image

        random.seed(password)
        #as the random number generator is pseudo-random so we can get a deterministic list of every number given we know the starting seed

        if num_bits>total_pixels:
            print("Error: Message is too big to hide in this image, give a higher resolution image.")
            return

        selected_indices=random.sample(range(total_pixels), num_bits)
        #randomly selects "num_bits" indices from the given range

        for i in range(num_bits):
            pass

    except FileNotFoundError:
        print(f"Error: Cannot find file at {image_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

def decode(image_path, password):
    pass

##ONLY FOR TESTING

if __name__ == "__main__":
    test_image = "test.png"
    test_message = "This is a secret"
    test_password = "key"
    encode(test_image, test_message, test_password)