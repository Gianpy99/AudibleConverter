# aaxToM4b Converter

## Overview
This is a simple bash script designed to convert Audible's `.aax` files to `.m4b` format, which can then be imported into Apple's Books program. The script is a response to the introduction of what I consider 'advertising' in the Audible app after Amazon's acquisition of Audible. The script utilizes the `activation_bytes` unique to your Audible account to decrypt and convert the files.

## Background
I have been using this script for a while as a workaround for the increased advertising content in the Audible app. The `.aax` files from Audible are essentially standard audio files with added DRM protection. Once the `activation_bytes` for your account are known (beyond the scope of this page), these files can be converted into a more standard and versatile format (`m4b`), making them compatible with Apple Books, which I find to have less intrusive advertising.

## Requirements
- **ffmpeg**: A robust tool for processing multimedia files.
- **AtomicParsley**: A tool for embedding metadata and artwork into audio files.

## Installation Instructions
### macOS
- ffmpeg: Install via Homebrew with `brew install ffmpeg`.
- AtomicParsley: Install via Homebrew with `brew install AtomicParsley`.

### Windows
- ffmpeg: Download from [FFmpeg Official Site](https://ffmpeg.org/download.html) or install via Chocolatey with `choco install ffmpeg`.
- AtomicParsley: Download from [AtomicParsley GitHub](https://github.com/wez/atomicparsley) or install via Chocolatey with `choco install atomicparsley`.

### Linux
- ffmpeg: Install via package manager, e.g., `sudo apt-get install ffmpeg` (Debian/Ubuntu).
- AtomicParsley: Install via package manager, e.g., `sudo apt-get install atomicparsley` (Debian/Ubuntu).

## Configuration
Before running the script, you need to set the following variables:
- `AUDIBLE_ACTIVATION_BYTES`: Your unique Audible activation bytes. If not set in the script, the script will use the value from the corresponding environment variable.
- `AUDIBLE_ARCHIVED_DIR`: Directory where the original AAX files will be moved after processing.
- `AUDIBLE_OUTPUT_DIR`: Directory where the converted M4B files will be copied.

## Usage
Run the script with one or more AAX files as arguments. For example:
```bash
./audibleDecrypt book1.aax book2.aax
```

## Disclaimer
This script is intended for personal use. Users should ensure they comply with Audible's terms of service and applicable laws regarding the use of DRM-protected content.
