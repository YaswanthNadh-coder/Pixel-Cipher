from stego import encode, decode
import os

def main():
    print("="*40)
    print("      Welcome to Pixel-Cipher      ")
    print("  The Secure Image Steganography Tool  ")
    print("="*40)

    while True:
        print("\nWhat would you like to do?")
        print("1. Encode (Hide a message)")
        print("2. Decode (Read a message)")
        print("3. Exit")
        
        choice = input("\nEnter your choice (1/2/3): ").strip()

        if choice == '1':
            print("\n--- ENCODE MODE ---")
            image_path = input("Enter the path to the image: ").strip().strip('"')
            
            if not os.path.exists(image_path):
                print(f"Error: The file '{image_path}' was not found.")
                continue

            message = input("Enter the message to hide: ")
            password = input("Enter a password: ")
            
            encode(image_path, message, password)

        elif choice == '2':
            print("\n--- DECODE MODE ---")
            image_path = input("Enter the path to the image: ").strip().strip('"')
            
            if not os.path.exists(image_path):
                print(f"Error: The file '{image_path}' was not found.")
                continue
                
            password = input("Enter the password: ")
            
            # Call the function from stego.py
            result = decode(image_path, password)
            
            if result:
                print("\n" + "-"*30)
                print(f"MESSAGE: {result}")
                print("-"*30)
            else:
                print("\nFailed to retrieve message.")

        elif choice == '3':
            print("\nExiting Pixel-Cipher. Goodbye!")
            break
        
        else:
            print("Invalid choice. Please type 1, 2, or 3.")

if __name__ == "__main__":
    main()