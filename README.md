#  PDF Outline Extractor – Adobe India Hackathon 2025 (Round 2)

##  Challenge Theme: Connecting the Dots Through Docs

This project extracts a structured outline from PDF documents, identifying the **title**, **H1**, **H2**, and **H3** headings along with their **page numbers**.

Built for **Round 2 of the Adobe India Hackathon 2025**, this solution runs fully offline inside a Docker container and adheres to all constraints (≤10s runtime, ≤200MB image size, CPU-only, amd64).

##  Problem Statement

Build a PDF outline extractor that:
- Accepts PDF files (≤ 50 pages)
- Extracts:
  - **Title**
  - **Headings**: H1, H2, H3 (with level and page number)
- Outputs a JSON file like:

```json
{
  "title": "Understanding AI",
  "outline": [
    { "level": "H1", "text": "Introduction", "page": 1 },
    { "level": "H2", "text": "What is AI?", "page": 2 },
    { "level": "H3", "text": "History of AI", "page": 3 }
  ]
}
```

##  Folder Structure

```
pdf-outline-extractor/
├── app/
│   ├── input/            # PDF files go here
│   ├── output/           # JSON outputs will be generated here
│   └── main.py           # Python script for heading extraction
├── Dockerfile
├── requirements.txt
└── README.md
```

##  Approach

Since most PDFs lack a built-in table of contents (TOC), we use a font-size-based heuristic:

- Largest font → Title
- Next 3 font sizes → H1, H2, H3
- The first text with the largest font on page 1 is assumed to be the title
- The rest are stored as structured heading levels with page numbers

##  Dockerized Setup (Offline, amd64)

###  Build Docker Image

```bash
docker build --platform linux/amd64 -t pdf-outline-extractor .
```

###  Run Docker Container

```bash
docker run --rm -v "${PWD}/app/input:/app/input" -v "${PWD}/app/output:/app/output" --network none pdf-outline-extractor
```

This will process all `.pdf` files in `app/input/` and output `.json` files to `app/output/`.

##  Dependencies

- python:3.10-slim
- PyMuPDF==1.23.9

You can install them locally using:

```bash
pip install -r requirements.txt
```

##  Constraints Handled

| Constraint                 | Status                      |
|----------------------------|-----------------------------|
| PDF ≤ 50 pages             |  Supported                  |
| Runtime ≤ 10 seconds       |  Fast execution             |
| Model size ≤ 200MB         |  No ML model used           |
| Offline execution          |  Fully offline              |
| Platform = AMD64, CPU only |  Docker base is linux/amd64 |


##  Team

**Team Name:** _Creanovate_

**Members:**
- Raghav Kumar Jha  
- Labhansh Pal  
- Aaron Mathew
Built for Adobe India Hackathon 2025 – Round 2

##  Notes

- Place your PDF files in `app/input/`
- The output `.json` files will be saved in `app/output/`
- File name of output matches the input PDF
- Heuristics can be adjusted in `main.py` for better accuracy

##  Sample Run Output

```
Processing: file01.pdf
Saved to app/output/file01.json
```
