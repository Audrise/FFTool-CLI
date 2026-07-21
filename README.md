<h1 align="center">
    <strong>FFTOOL CLI</strong>
</h1>

<div align=center>
    <strong>Audio Metadata & Cover Art Tool</strong>
</div>
<br>

<div align=center>
    <a href="https://www.python.org/">
        <img src="https://img.shields.io/badge/Python-FFDD00?style=for-the-badge&logo=python&logoColor=blue"/>
    </a>
    <img src="https://img.shields.io/badge/Version-1.0-blue?style=for-the-badge"/>
    <br>
    <img src="https://img.shields.io/badge/Maintained%3F-yes-blue.svg"/>
    <img src="https://img.shields.io/github/stars/Audrise/FFTool-CLI?style=social">
</div>
<br>

<h1 align="center">DISCLAIMER!</h1>

**SIMPLE AUDIO TOOL** is developed strictly for **personal use**, **audio organization**, and **educational purposes**. This tool is designed to **view, edit, and manage audio metadata and cover art** in a **safe environment**.

Any **unauthorized distribution or commercial use** of audio files you do not own may be considered **illegal**. Use this software responsibly and always ensure you have the rights to modify the audio files.

---

## Table of Contents
* **[Description](#description)**
* **[Features](#features)**
* **[Usage](#usage)**
* **[Arguments](#arguments)**
* **[Credits](#credits)**
* **[Updates](#updates)**

---

## Description
**SIMPLE AUDIO TOOL** is a Python tool for **managing audio metadata, cover art, and audio conversion**. It supports multiple formats including **MP3, FLAC, M4A/AAC, and OGG**. Users can:

- List audio files in a directory
- View and edit metadata tags (title, artist, album, etc.)
- Add, replace, or delete cover art
- Convert audio files to different formats, sample rates, and bit depths

The tool provides an **interactive terminal interface** with colorful menus for easy navigation.

---

## Features
- **Metadata Management**:
    - View existing tags for individual or all audio files
    - Add or edit tags for single or multiple files
    - Delete specific tags

- **Cover Art Management**:
    - Add or update cover images (JPEG/PNG)
    - Remove cover art from individual or all audio files

- **Audio Conversion**:
    - Change **sample rates** (44.1 kHz up to 192 kHz)
    - Adjust **bit depth** (8, 16, 24, 32 bits)
    - Convert between **MP3, FLAC, AAC, OGG**
    - Custom output filenames

- **Fully Interactive & Colored CLI**:
    - Dynamic menus with animations
    - Color-coded success/error messages
    - Easily navigate between metadata, cover art, and audio conversion

- **Directory Management**:
    - Change working directory to manage audio files in different folders

- **Batch Operations**:
    - Apply changes to all files in a directory at once

- **Note**:
    - This project requires **FFmpeg** and **FFprobe** to be installed and accessible from your terminal/command prompt.

---

## Arguments

This tool is **interactive**. You do not need to pass command-line arguments; everything is controlled through the terminal menus.

**Options inside menus include**:

| Menu | Options |
|------|---------|
| Metadata | View, Add/Edit, Delete tags |
| Cover Art | Add/Edit, Delete cover images |
| Audio Conversion | Set file, sample rate, bit depth, codec, convert, reset |
| Directory | Change current working directory |
| Main Menu | Navigate to submenus or exit |

---

## Usage

1. Clone this repository to your local machine:
    ```bash
    git clone https://github.com/Audrise/audiotool.git
    ```
    Or download as ZIP:
    ```bash
    https://github.com/Audrise/audiotool/archive/refs/heads/main.zip
    ```
    ```bash
    cd audiotool
    ```

2. Install required Python libraries:
    ```bash
    pip install -r requirements.txt
    ```
    Or manually:
    ```bash
    pip install mutagen pystyle colorama tqdm
    ```

3. Run the editor:
    ```bash
    python main.py
    ```

4. Follow the interactive menu to:
    - List audio files
    - Edit metadata
    - Add/remove cover art
    - Convert audio files

---

## Credits
- **[mutagen](https://mutagen.readthedocs.io/en/latest/)** – For reading and writing audio metadata
- **[pystyle](https://github.com/BillyTheGoat356/pystyle)** – For terminal UI styling and animations
---

## Updates

### **1.0 - Initial Release** 📌
- Added full **metadata editor** functionality
- Implemented **cover art add/remove**
- Added **audio conversion** menu with codec, sample rate, and bit depth options
- Fully interactive CLI with colorized menus and animations
- Supports **MP3, FLAC, M4A/AAC, OGG**
- Batch operations for metadata and cover art

<h1></h1>
<h4 align="center">©AUDRISE</h4>
