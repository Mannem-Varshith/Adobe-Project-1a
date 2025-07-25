FROM python:3.10-slim
WORKDIR /app
RUN pip install --no-cache-dir pymupdf
COPY extract_outline.py .
ENTRYPOINT ["python", "extract_outline.py"] 