import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import os
import json
from difflib import SequenceMatcher

# ---------- OCR-BASED TITLE EXTRACTION ----------
def extract_title_with_ocr(pdf_path):
    doc = fitz.open(pdf_path)
    pix = doc[0].get_pixmap(dpi=300)
    image_path = "page1.png"
    pix.save(image_path)

    img = Image.open(image_path)
    raw_text = pytesseract.image_to_string(img)

    # Filter and clean top lines
    lines = [line.strip() for line in raw_text.split("\n") if line.strip()]
    title_lines = []

    for line in lines[:6]:
        if len(line.split()) >= 3 and len(line) >= 15:
            title_lines.append(line)

    title = " ".join(title_lines).strip()
    title = " ".join(title.split())  # Normalize spaces
    return title

# ---------- HEADING DETECTION USING FONT SIZE ----------
def extract_headings(pdf_path):
    doc = fitz.open(pdf_path)
    all_headings = []
    font_sizes = set()

    for page_num in range(len(doc)):
        page = doc[page_num]
        blocks = page.get_text("dict")["blocks"]

        for block in blocks:
            if "lines" not in block:
                continue

            for line in block["lines"]:
                spans = line.get("spans", [])
                if not spans:
                    continue

                line_text = "".join(span["text"] for span in spans).replace("  ", " ").strip()
                line_text = " ".join(line_text.split())

                if not line_text or len(line_text) < 3:
                    continue

                avg_size = round(sum(span["size"] for span in spans) / len(spans), 2)
                font_sizes.add(avg_size)

                all_headings.append({
                    "text": line_text,
                    "size": avg_size,
                    "page": page_num + 1
                })

    # Rank font sizes
    ranked_sizes = sorted(list(font_sizes), reverse=True)
    size_to_level = {}
    if len(ranked_sizes) >= 1:
        size_to_level[ranked_sizes[0]] = "H1"
    if len(ranked_sizes) >= 2:
        size_to_level[ranked_sizes[1]] = "H2"
    if len(ranked_sizes) >= 3:
        size_to_level[ranked_sizes[2]] = "H3"
    if len(ranked_sizes) >= 4:
        size_to_level[ranked_sizes[3]] = "H4"

    # Final outline
    outline = []
    for h in all_headings:
        level = size_to_level.get(h["size"])
        if level:
            outline.append({
                "level": level,
                "text": h["text"],
                "page": h["page"]
            })

    return outline

# ---------- MAIN PIPELINE ----------
def process_pdf(pdf_path, output_path):
    title = extract_title_with_ocr(pdf_path)
    outline = extract_headings(pdf_path)

    result = {
        "title": title,
        "outline": outline
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)


# ---------- ENTRY POINT ----------
def process_all_pdfs(input_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for filename in os.listdir(input_dir):
        if filename.endswith(".pdf"):
            input_path = os.path.join(input_dir, filename)
            output_filename = filename.replace(".pdf", ".json")
            output_path = os.path.join(output_dir, output_filename)

            print(f"Processing: {filename}")
            process_pdf(input_path, output_path)

# ---------- Run for Docker ----------
if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(base_dir, "input")
    output_path = os.path.join(base_dir, "output")
    process_all_pdfs(input_path, output_path)

