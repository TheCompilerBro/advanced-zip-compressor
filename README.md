# 📦 Advanced ZIP Compressor

A Python-based ZIP compression utility designed to compress files and folders efficiently while preserving the original data without any loss.

## ✨ Features

- **File Compression:** Compress individual files into ZIP archives.
- **Folder Compression:** Compress entire folders while maintaining their directory structure.
- **Multiple Compression Methods:** Supports different ZIP compression algorithms.
- **Lossless Compression:** Preserves the original file data.
- **Integrity Checking:** Verifies the generated ZIP archive.
- **Original File Protection:** Does not modify or delete the original files.
- **Simple Interface:** Easy to use and lightweight.

## 🛠️ Technologies Used

- Python 3
- ZIP File Handling (`zipfile`)
- Operating System Module (`os`)
- Path Management (`pathlib`)

## 📋 Requirements

- Python 3.8 or higher
- No external Python packages required (if using only Python standard libraries).

## 🚀 Installation

**1. Clone the repository**

```bash
git clone https://github.com/YOUR_USERNAME/zip-compressor.git
```

**2. Navigate to the project directory**

```bash
cd zip-compressor
```

**3. Run the program**

```bash
python3 zip_compressor.py
```

## 💻 Usage

1. Run the Python script.
2. Select the compression mode.
3. Enter the file or folder path.
4. Choose the required compression method if prompted.
5. Let the program create the ZIP archive.
6. Verify the generated archive.

## 📁 Project Structure

```text
zip-compressor/
│
├── zip_compressor.py
├── README.md
├── LICENSE
└── .gitignore
```

## 🔒 Data Safety

- Original files remain unchanged.
- Compression is lossless.
- The generated ZIP archive can be extracted to recover the original files.

## 🔮 Future Improvements

- [ ] Add a graphical user interface (GUI).
- [ ] Add drag-and-drop file support.
- [ ] Display real-time compression progress.
- [ ] Show compression ratio and file size statistics.
- [ ] Support password-protected ZIP archives.
- [ ] Add batch compression.
- [ ] Add a compression history feature.

## 📜 License

This project is licensed under the [MIT License](LICENSE).

## 👨‍💻 Author

**Puspendu Mallick**

- GitHub: [@TheCompilerBro](https://github.com/TheCompilerBro)

---

⭐ If you find this project useful, consider giving it a star on GitHub!