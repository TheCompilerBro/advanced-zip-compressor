# Advanced ZIP Compressor

A Python command-line tool that tests multiple ZIP compression configurations and saves the smallest **verified** archive it can create.

You can use it to:
- Compress a folder into a ZIP archive.
- Recompress an existing ZIP archive.
- Compare DEFLATE, BZIP2, and LZMA compression.
- Automatically select the smallest valid result from the tested configurations.

The tool uses Python's built-in libraries, so no third-party packages are required.

## Features

- **Two compression modes:** folder-to-ZIP and ZIP-to-ZIP.
- **Automatic compression testing:** tests DEFLATE levels 1–9, BZIP2 levels 1–9, and LZMA with Python's default preset.
- **Smallest-result selection:** keeps the smallest archive among the successful tests.
- **ZIP integrity verification:** checks each candidate archive and verifies the final output.
- **Already-compressed file handling:** stores common image, audio, video, and archive formats without trying to compress them again.
- **Original input protection:** creates a separate output archive and does not modify the source folder or ZIP file.
- **No accidental overwrite:** adds a numbered suffix when an output filename already exists.
- **Final report:** displays the original size, final size, selected algorithm, compression level, and size difference.

## Requirements

- Python 3.7 or newer
- No external Python packages

The script uses only Python standard-library modules.

## Installation

Clone the repository:

```bash
git clone https://github.com/your-username/your-repository.git
```

Move into the project directory:

```bash
cd your-repository
```

Make sure Python is installed:

```bash
python3 --version
```

## Usage

Run the script from your terminal. Choose either `folder` or `zip` mode.

### 1. Compress a folder

```bash
python3 zip_compressor.py folder "/path/to/your/folder"
```

Example:

```bash
python3 zip_compressor.py folder "Documents/Project Files"
```

The output ZIP is created in the same parent directory as the input folder. For example, a folder named `Project Files` produces `Project Files_compressed.zip`.

### 2. Recompress an existing ZIP file

```bash
python3 zip_compressor.py zip "/path/to/your/file.zip"
```

Example:

```bash
python3 zip_compressor.py zip "backup.zip"
```

The original ZIP remains unchanged. The new archive is saved beside it, using a name such as `backup_compressed.zip`.

### 3. View help

```bash
python3 zip_compressor.py --help
```

## How It Works

1. The script validates the input path and calculates the input size.
2. It creates temporary ZIP archives using the supported compression configurations.
3. It tests each generated archive for ZIP integrity.
4. It compares the sizes of the successfully verified archives.
5. It copies the smallest verified archive to the output location.
6. It verifies the final archive again and prints a summary report.

Temporary test archives are stored in a temporary directory and are cleaned up after the run.

## Compression Methods

| Method | Configurations tested | Description |
|---|---:|---|
| DEFLATE | Levels 1–9 | Common ZIP compression method with adjustable compression levels. |
| BZIP2 | Levels 1–9 | Alternative compression method that may produce a smaller archive for some data. |
| LZMA | Default preset | Another compression method; the script uses Python's default ZIP LZMA settings. |

The script automatically chooses the smallest successful result. You do not need to select a method or compression level manually.

## Already-Compressed File Types

Files with extensions such as `.jpg`, `.png`, `.mp3`, `.mp4`, `.zip`, `.rar`, `.7z`, `.gz`, and other configured formats are stored without additional compression. These formats are generally compressed already, so recompressing them may waste processing time without reducing their size.

The exact list is maintained in `ALREADY_COMPRESSED` inside `zip_compressor.py`.

## Output and Important Notes

- The generated archive is saved next to the input.
- Existing output files are not overwritten; a numbered filename is used instead.
- The original folder or ZIP file is left unchanged.
- Compression is lossless: the files' contents are not intentionally altered.
- **A smaller archive is not guaranteed.** Some files are already compressed or do not compress well. The final ZIP can be the same size or larger.
- ZIP tools must support the compression method used by the selected archive. Compatibility with older extraction software may vary, particularly for BZIP2 and LZMA entries.
- Recompressing a ZIP archive requires reading its entries and writing a new archive, so processing time depends on the amount and type of data.

## Project Structure

```text
.
├── zip_compressor.py
└── README.md
```

## Contributing

Suggestions, bug reports, and improvements are welcome. You can open an issue or submit a pull request.

## License

No license file is currently included. Add a `LICENSE` file to the repository before distributing the project under a specific open-source license.
