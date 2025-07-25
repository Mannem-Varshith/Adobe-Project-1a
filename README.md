

# 📄 PDF Outline Extractor

Automatically extract a structured outline from a PDF document by identifying its **title** and **headings** based on **font sizes**. The output is a JSON file representing the document's structure. The entire process is containerized using **Docker** for easy setup and execution.

---

## 💡 Approach

The core logic is implemented in a Python script using the `PyMuPDF` library to analyze PDF content.

### 🔍 Steps:

1. **Font Analysis**  
   Scans the document to collect all unique font sizes.

2. **Heading Identification**  
   Assumes the three largest unique font sizes correspond to `H1`, `H2`, and `H3` headings.

3. **Title Extraction**  
   The title is identified as the largest text on the first page.

4. **Outline Generation**  
   Captures any text matching the heading font sizes and records its level and page number.

5. **JSON Output**  
   Saves a structured JSON outline with the title and heading hierarchy.

---

## 🚀 Usage with Docker

This project is packaged with Docker to ensure portability and hassle-free execution.

### ✅ Prerequisites

- [Docker](https://www.docker.com/) installed on your system.
- A folder containing the input PDF(s).
- An empty folder for the output JSON file(s).

---

### 🛠️ Step 1: Build the Docker Image

Build the image using the provided `Dockerfile`:

```bash
docker build -t pdf-outline-extractor .
````

---

### ▶️ Step 2: Run the Docker Container

Run the container by mounting your input/output directories:

#### 🪟 For Windows (Command Prompt):

```bash
docker run --rm -v "%cd%/input:/app/input" -v "%cd%/output:/app/output" --network none pdf-outline-extractor
```

#### 🐧 For macOS/Linux:

```bash
docker run --rm -v "$(pwd)/input:/app/input" -v "$(pwd)/output:/app/output" --network none pdf-outline-extractor
```

---

### 📁 Output

After execution, a JSON file will be created in the `output/` folder with the same name as the input PDF.

#### Example output structure:

```json
{
  "title": "Document Title",
  "headings": [
    {
      "text": "Introduction",
      "level": "H1",
      "page": 1
    },
    {
      "text": "Subsection 1.1",
      "level": "H2",
      "page": 1
    }
  ]
}
```

---

## 🧰 Tech Stack

* **Python** 🐍
* **PyMuPDF** (`fitz`)
* **Docker** 🐳

---

