# Menu OCR Example

This project contains a simple script to extract menu items from a photo. It uses Tesseract OCR via `pytesseract` and stores results in an SQLite database.

## Requirements

- Python 3.8+
- Tesseract OCR installed on the system
- Python packages from `requirements.txt`

On Debian/Ubuntu Tesseract can be installed with:

```bash
sudo apt-get install tesseract-ocr
sudo apt-get install tesseract-ocr-rus  # add languages as needed
```

Verify the installation with:

```bash
tesseract --version
```

Then install Python dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Run the script providing an image with a restaurant menu and a restaurant name:

```bash
python extract_menu.py path/to/photo.jpg "Restaurant Name"
```

Recognized dishes will be printed to stdout and stored in `menu.db`.
