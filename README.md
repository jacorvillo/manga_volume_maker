# 📚 E-Reader Manga Volume Maker

If you're like me, you probably love reading manga from the comfort and distraction-less environment of your e-reader...but managing multiple chapters at a time can be a hassle.

This simple Python script takes any manga chapters that you acquired through your trusted sources, and organizes them neatly into volumes in a .cbz file for your e-reader. You can set a custom cover image as well!

## 📋 Prerequisites

- Python 3.6 or higher. That's it!

## 📥 Installation & Usage

Download the Python script and place it in your manga directory structure. Your directory should look something like this: 
```
📁 Your Manga Directory/
├── 📄 volume_maker.py
├── 📁 Chapter 01 - [uuid]/
│   ├── 🖼️ 01.jpg
│   ├── 🖼️ 02.jpg
│   └── 🖼️ ...
├── 📁 Chapter 02 - [uuid]/
│   ├── 🖼️ 01.jpg
│   ├── 🖼️ 02.jpg
│   └── 🖼️ ...
└── 📁 Chapter 03 - [uuid]/
    ├── 🖼️ 01.jpg
    ├── 🖼️ 02.jpg
    └── 🖼️ ...
```

Open a terminal in the manga directory and run:

```bash
python volume_maker.py 01 03 "Volume_1"
```

- With Custom Cover

```bash
python volume_maker.py "cover.jpg" 01 03
```

The resulting .cbz file will be named "Volume_1.cbz", containing all pages from Chapter 01 to Chapter 03, with the specified cover image. Multiple formats are supported besides .jpg (.png, .jpeg, etc.).

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. If you encounter any issues or have questions, please [open an issue](https://github.com/yourusername/manga-chapter-merger/issues) on GitHub.

---