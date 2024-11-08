import os
import base64
import argparse

BLACKLIST = {"based64.py"}
FILE_EXT = "based64"

def encode_file_to_base64(file_path):
    save_to = f"{file_path}.{FILE_EXT}"

    with open(file_path, "rb") as file:
        with open(save_to, "wb") as f64:
            for chunk in iter(lambda: file.read(), b""):
                f64.write(base64.b64encode(chunk))

def decode_base64_file(file_path: str):
    if not file_path.endswith(FILE_EXT):
        raise Exception("wtf")

    save_to = ".".join(file_path.split(".")[:-1])

    with open(file_path, "rb") as f64:
        for chunk in iter(lambda: f64.read(), b""):
            with open(save_to, "ab") as file:
                file.write(base64.b64decode(chunk))

def main():
    working_dir = os.path.dirname(os.path.realpath(__file__))
    files = []

    for root, dirs, filenames in os.walk(working_dir):
        for filename in filenames:
            if filename not in BLACKLIST:
                files.append(os.path.join(root, filename))

    base64_action = decode_base64_file if args.decode else encode_file_to_base64

    for file_path in files:
        try:
            base64_action(file_path)
            os.remove(file_path)

        except Exception as e:
            if str(e) == "wtf":
                print( f"we only work with '.{FILE_EXT}' files here, fam: {e}.")
                exit(1)

            print(f"error processing '{file_path}': {e}.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="encode or decode files present in this very same FUCKING directory and its children.")
    parser.add_argument("-d", "--decode", action="store_true")
    args = parser.parse_args()

    main()