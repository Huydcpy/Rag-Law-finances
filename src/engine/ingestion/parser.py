from pathlib import Path
import numpy as np
from pdf2image import convert_from_path
from llama_index.core import Document

PROJECT_ROOT = Path(__file__).resolve().parents[3]
RAW_DIR = PROJECT_ROOT / "data" / "raw"

PDF_FILES = sorted(RAW_DIR.glob("*.pdf"))


def _init_reader():
    import easyocr
    return easyocr.Reader(["vi"], gpu=False)


def _ocr_page(reader, image, page_num, file_name):
    img_np = np.array(image)
    result = reader.readtext(img_np, detail=0, paragraph=True)
    text = " ".join(result)
    return Document(
        text=text,
        metadata={
            "file_name": file_name,
            "page_label": str(page_num),
        },
    )


documents = []
reader = None
for pdf_path in PDF_FILES:
    print(f"Processing {pdf_path.name} ...")
    images = convert_from_path(str(pdf_path), dpi=200)
    if reader is None:
        reader = _init_reader()
    for i, img in enumerate(images):
        doc = _ocr_page(reader, img, i + 1, pdf_path.name)
        documents.append(doc)
        if (i + 1) % 20 == 0:
            print(f"  OCR-ed {i + 1}/{len(images)} pages")

print(f"Loaded {len(documents)} documents via OCR")