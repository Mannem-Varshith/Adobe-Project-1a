import os
import json
import fitz  # PyMuPDF

INPUT_DIR = "/app/input"
OUTPUT_DIR = "/app/output"

def extract_outline(pdf_path):
    doc = fitz.open(pdf_path)
    font_sizes = []
    headings = []
    title = None

    # Collect all font sizes to determine thresholds
    for page_num in range(len(doc)):
        page = doc[page_num]
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            for line in block.get("lines", []):
                for span in line.get("spans", []):
                    font_sizes.append(span["size"])
    if not font_sizes:
        return None
    # Get unique font sizes, sorted descending
    unique_sizes = sorted(set(font_sizes), reverse=True)
    h1_size = unique_sizes[0]
    h2_size = unique_sizes[1] if len(unique_sizes) > 1 else h1_size
    h3_size = unique_sizes[2] if len(unique_sizes) > 2 else h2_size

    # Title: largest text on first page
    first_page = doc[0]
    title = ""
    max_size = 0
    for block in first_page.get_text("dict")["blocks"]:
        for line in block.get("lines", []):
            for span in line.get("spans", []):
                if span["size"] > max_size and span["text"].strip():
                    max_size = span["size"]
                    title = span["text"].strip()

    # Headings (flat list)
    for page_num in range(len(doc)):
        page = doc[page_num]
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            for line in block.get("lines", []):
                for span in line.get("spans", []):
                    text = span["text"].strip()
                    if not text or len(text) < 2:
                        continue
                    size = span["size"]
                    if size == h1_size:
                        level = "H1"
                    elif size == h2_size:
                        level = "H2"
                    elif size == h3_size:
                        level = "H3"
                    else:
                        continue
                    headings.append({
                        "level": level,
                        "text": text,
                        "page": page_num + 1
                    })

    # Build hierarchical outline
    outline = []
    stack = []  # Each element: (level, node)
    level_order = {"H1": 1, "H2": 2, "H3": 3}
    for heading in headings:
        node = {**heading, "children": []}
        while stack and level_order[heading["level"]] <= level_order[stack[-1][0]]:
            stack.pop()
        if not stack:
            outline.append(node)
        else:
            stack[-1][1]["children"].append(node)
        stack.append((heading["level"], node))

    return {
        "title": title,
        "outline": outline
    }

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    for filename in os.listdir(INPUT_DIR):
        if filename.lower().endswith(".pdf"):
            pdf_path = os.path.join(INPUT_DIR, filename)
            outline = extract_outline(pdf_path)
            if outline:
                out_path = os.path.join(OUTPUT_DIR, filename.rsplit(".", 1)[0] + ".json")
                with open(out_path, "w", encoding="utf-8") as f:
                    json.dump(outline, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    main() 