import os
import base64
import argparse
from typing import Literal

BLACKLIST = {"based64.py"}
FILE_EXT = "based64"

def process_file(file_path: str, save_to: str, mode_writing: Literal["wb", "ab"] = "wb", action: Literal["encode", "decode"] = "encode") -> None:
    actions = {
        "decode": base64.b64decode,
        "encode": base64.b64encode
    }
    base64_action = actions.get(action)

    with open(file_path, "rb") as file:
        with open(save_to, mode_writing) as f64:
            for chunk in iter(lambda: file.read(), b""):
                f64.write(base64_action(chunk))

def encode_file_to_base64(file_path: str) -> None:
    save_to = f"{file_path}.{FILE_EXT}"

    process_file(file_path, save_to)

def decode_base64_file(file_path: str) -> None:
    if not file_path.endswith(FILE_EXT):
        raise Exception("wtf")

    save_to = ".".join(file_path.split(".")[:-1])

    process_file(file_path, save_to, "ab", "decode")

def main() -> None:
    files = []
    base64_action = decode_base64_file if args.decode else encode_file_to_base64

    if args.files is not None:
        files = args.files

    else:
        working_dir = os.path.dirname(os.path.realpath(__file__))
        
        for root, _, filenames in os.walk(working_dir):
            for filename in filenames:
                if filename not in BLACKLIST:
                    files.append(os.path.join(root, filename))


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
    parser = argparse.ArgumentParser(description="encode or decode files present in this very same FUCKING directory and its subdirectories.")
    parser.add_argument("-f", "--files", nargs="*")
    parser.add_argument("-d", "--decode", action="store_true")
    args = parser.parse_args()

    main()