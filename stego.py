from PIL import Image
import random
from crypto import vigenere_encrypt,vigenere_decrypt,text_to_bits, bits_to_text

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

        encrypted_message=vigenere_encrypt(message, password)
        msg_bits=text_to_bits(encrypted_message)
        num_bits=len(msg_bits)

        header_bits = format(num_bits, '032b')

        #METHOD 1: Turned out to be very space inefficient especially for high-res images
        #coordinates=[(x,y) for x in range(width) for y in range(height)]
        #gives a list of 2-tuples containing all the possible coordinates in an image

        random.seed(password)
        #as the random number generator is pseudo-random so we can get a deterministic list of every number given we know the starting seed

        if 32+num_bits>total_pixels:
            print("Error: Message is too big to hide in this image, give a higher resolution image.")
            return

        selected_indices=random.sample(range(32,total_pixels), num_bits)
        #randomly selects "num_bits" indices from the given range

        #storing the number of bits in the message in the first 32 pixels so while decoding we know when to stop
        for i in range(32):
            bit = header_bits[i]
            x = i % width
            y = i // width
            
            r, g, b = pixels[x, y]
            if bit == '1':
                new_r = r | 1
            else:    
                new_r = r & 254
            pixels[x, y] = (new_r, g, b)

        for i in range(num_bits):
            bit=msg_bits[i]
            index=selected_indices[i]
            #converting the 1D index to a 2D coordinate
            x=index%width
            y=index//width

            r,g,b=pixels[x,y]
            #get the bit value of each r,g,b of the pixel

            if bit=='1':
                new_r=r | 1
            else:
                new_r=r & 254
            
            pixels[x,y]=(new_r,g,b)

            #FUTURE PLAN: Store the bits into each r, g and b of each pixel

        output_path = "encoded_image.png"
        img.save(output_path)
        print("Successfully encoded message.")

    except FileNotFoundError:
        print(f"Error: Cannot find file at {image_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

def decode(image_path, password):
    try:
        img=Image.open(image_path).convert("RGB")
        pixels = img.load()
        width, height = img.size
        total_pixels = width * height

        header_bits = ""                #first we'll get the number of bits stored in the message
        for i in range(32):
            x = i % width
            y = i // width
            r, g, b = pixels[x, y]
            
            header_bits += str(r & 1)     #extracting the last bit in the red channel
        num_bits = int(header_bits, 2)

        random.seed(password)             #regenerate the pseudo-random pattern
        selected_indices = random.sample(range(32, total_pixels), num_bits)
        
        extracted_bits=""
        for index in selected_indices:
            x=index % width
            y=index // width
            r, g, b=pixels[x, y]
            
            extracted_bits+=str(r & 1)
        encrypted_message=bits_to_text(extracted_bits)

        original_message=vigenere_decrypt(encrypted_message, password)
        print("Success! Message decoded.")
        return original_message
    
    except FileNotFoundError:
        print(f"Error: Cannot find file at {image_path}")
        return None
    except Exception as e:
        print(f"An error occured: {e}")
        return None
