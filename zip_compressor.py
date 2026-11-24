
import os
import zipfile
import argparse
import tempfile
import shutil
import copy
from pathlib import Path



COMPRESSION_METHODS = {
    "DEFLATE": {
        "method": zipfile.ZIP_DEFLATED,
        "levels": list(range(1, 10))
    },

    "BZIP2": {
        "method": zipfile.ZIP_BZIP2,
        "levels": list(range(1, 10))
    },

    "LZMA": {
        "method": zipfile.ZIP_LZMA,
        "levels": [None]
    }
}


ALREADY_COMPRESSED = {
    ".jpg", ".jpeg", ".png", ".gif", ".webp",
    ".avif", ".heic", ".mp3", ".mp4", ".m4a",
    ".aac", ".ogg", ".flac", ".mov", ".mkv",
    ".avi", ".webm", ".zip", ".rar", ".7z",
    ".gz", ".bz2", ".xz", ".zst"
}


def format_size(size):

    if size >= 1024 ** 3:
        return f"{size / (1024 ** 3):.2f} GB"

    if size >= 1024 ** 2:
        return f"{size / (1024 ** 2):.2f} MB"

    if size >= 1024:
        return f"{size / 1024:.2f} KB"

    return f"{size} bytes"


def get_folder_size(folder):

    total = 0

    for root, _, files in os.walk(folder):

        for file in files:

            path = Path(root) / file

            if path.is_file():
                total += path.stat().st_size

    return total


def get_output_path(input_path, mode):

    if mode == "folder":
        name = input_path.name
    else:
        name = input_path.stem

    output = input_path.parent / f"{name}_compressed.zip"

    # Never overwrite an existing archive.
    counter = 2

    while output.exists():

        output = input_path.parent / (
            f"{name}_compressed_{counter}.zip"
        )

        counter += 1

    return output


def verify_zip(zip_path):

    with zipfile.ZipFile(zip_path, "r") as archive:

        bad_file = archive.testzip()

        if bad_file:
            raise RuntimeError(
                f"ZIP integrity failed: {bad_file}"
            )

        return len(archive.namelist())


def is_already_compressed(filename):

    return Path(filename).suffix.lower() in ALREADY_COMPRESSED


def create_folder_zip(folder, output, method, level):

    folder = Path(folder).resolve()

    with zipfile.ZipFile(
        output,
        "w",
        compression=method,
        compresslevel=level
    ) as archive:

        # Preserve empty directories too.
        for root, dirs, files in os.walk(folder):

            relative_root = Path(root).relative_to(folder.parent)

            if not dirs and not files:
                archive.writestr(
                    relative_root.as_posix() + "/",
                    b""
                )

            for file in files:

                file_path = Path(root) / file

                if not file_path.is_file():
                    continue

                relative_path = file_path.relative_to(
                    folder.parent
                )

                if is_already_compressed(file):

                    archive.write(
                        file_path,
                        relative_path,
                        compress_type=zipfile.ZIP_STORED
                    )

                else:

                    archive.write(
                        file_path,
                        relative_path,
                        compress_type=method
                    )

def create_zip_from_zip(
    input_zip,
    output_zip,
    method,
    level
):

    with zipfile.ZipFile(input_zip, "r") as source:

        with zipfile.ZipFile(
            output_zip,
            "w",
            compression=method,
            compresslevel=level
        ) as destination:

            destination.comment = source.comment

            for item in source.infolist():

                
                if item.is_dir():

                    destination.writestr(
                        item,
                        b""
                    )

                    continue

                
                data = source.read(item)

               
                new_item = copy.copy(item)

                
                if is_already_compressed(item.filename):

                    new_item.compress_type = zipfile.ZIP_STORED

                    destination.writestr(
                        new_item,
                        data,
                        compress_type=zipfile.ZIP_STORED
                    )

                else:

                    new_item.compress_type = method

                    destination.writestr(
                        new_item,
                        data,
                        compress_type=method,
                        compresslevel=level
                    )




def compress_input(input_path, mode):

    input_path = Path(input_path).expanduser().resolve()

    if mode == "folder":

        if not input_path.is_dir():
            raise ValueError("Input must be a valid folder.")

        original_size = get_folder_size(input_path)

    elif mode == "zip":

        if not input_path.is_file():
            raise ValueError("ZIP file does not exist.")

        if not zipfile.is_zipfile(input_path):
            raise ValueError("Invalid ZIP file.")

        original_size = input_path.stat().st_size

    else:
        raise ValueError("Invalid compression mode.")

    if original_size == 0:
        raise ValueError("Input is empty.")

    output = get_output_path(input_path, mode)

    print("\n")
    print("=" * 55)
    print("             ZIP COMPRESSOR")
    print("=" * 55)

    print(f"Mode          : {mode.upper()}")
    print(f"Input         : {input_path}")
    print(f"Original size : {format_size(original_size)}")
    print(f"Output        : {output}")

    print("=" * 55)

    best_size = None
    best_temp = None
    best_method = None
    best_level = None
    best_file_count = 0

    total_attempts = sum(
        len(config["levels"])
        for config in COMPRESSION_METHODS.values()
    )

    current_attempt = 0

    with tempfile.TemporaryDirectory() as temp_dir:

        for method_name, config in COMPRESSION_METHODS.items():

            method = config["method"]

            for level in config["levels"]:

                current_attempt += 1

                level_name = (
                    str(level) if level is not None
                    else "default"
                )

                temp_zip = Path(temp_dir) / (
                    f"{method_name}_{level_name}.zip"
                )

                print(
                    f"\n[{current_attempt}/{total_attempts}] "
                    f"Testing {method_name} | Level {level_name}"
                )

                try:

                    # Generate candidate ZIP.
                    if mode == "folder":

                        create_folder_zip(
                            input_path,
                            temp_zip,
                            method,
                            level
                        )

                    else:

                        create_zip_from_zip(
                            input_path,
                            temp_zip,
                            method,
                            level
                        )

                    size = temp_zip.stat().st_size

                    # Verify candidate.
                    file_count = verify_zip(temp_zip)

                    print(
                        f"Result: {format_size(size)}"
                    )

                    # Select smallest verified archive.
                    if best_size is None or size < best_size:

                        best_size = size
                        best_temp = temp_zip
                        best_method = method_name
                        best_level = level_name
                        best_file_count = file_count

                        print(
                            "NEW MINIMUM SIZE FOUND!"
                        )

                except Exception as error:

                    print(f"Skipped: {error}")

        if best_temp is None:

            raise RuntimeError(
                "All compression attempts failed."
            )

        shutil.copy2(best_temp, output)

    final_file_count = verify_zip(output)

    final_size = output.stat().st_size

    saved_size = original_size - final_size

    saved_percentage = (
        saved_size / original_size
    ) * 100

    

    print("\n")
    print("=" * 55)
    print("                FINAL REPORT")
    print("=" * 55)

    print(f"Original size      : {format_size(original_size)}")
    print(f"Minimum ZIP size   : {format_size(best_size)}")
    print(f"Final ZIP size     : {format_size(final_size)}")

    print(f"Best algorithm     : {best_method}")
    print(f"Best level         : {best_level}")

    print(f"Files stored       : {final_file_count}")

    if saved_size >= 0:

        print(f"Space saved        : {format_size(saved_size)}")
        print(f"Size reduction     : {saved_percentage:.2f}%")

    else:

        print(f"Size increased     : {format_size(abs(saved_size))}")
        print(
            f"Size increase      : {abs(saved_percentage):.2f}%"
        )

    print("-" * 55)

    print("Compression        : COMPLETED")
    print("ZIP integrity      : VERIFIED")
    print("Original input     : UNCHANGED")

    print(f"\nSaved location:\n{output}")

    print("=" * 55)

    print("\nSUCCESS: Smallest tested ZIP selected!")


def main():

    parser = argparse.ArgumentParser(
        description="Advanced Lossless ZIP Compressor"
    )

    subparsers = parser.add_subparsers(
        dest="mode",
        required=True
    )

    # Folder mode.
    folder_parser = subparsers.add_parser(
        "folder",
        help="Compress a folder into ZIP"
    )

    folder_parser.add_argument(
        "input",
        help="Input folder path"
    )

    # ZIP mode.
    zip_parser = subparsers.add_parser(
        "zip",
        help="Recompress an existing ZIP"
    )

    zip_parser.add_argument(
        "input",
        help="Input ZIP file path"
    )

    args = parser.parse_args()

    try:

        compress_input(
            args.input,
            args.mode
        )

    except KeyboardInterrupt:

        print("\nCompression cancelled by user.")

    except Exception as error:

        print(f"\nERROR: {error}")


if __name__ == "__main__":
    main()
