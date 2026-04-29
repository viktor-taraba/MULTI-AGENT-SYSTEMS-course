# LlamaIndex / LlamaParse — Supported File Types (Extended)

## Purpose
This document expands on the initial summary of supported file types for LlamaIndex (via LlamaParse and the LlamaIndex file-readers ecosystem). It consolidates: the broad LlamaParse supported formats, SimpleDirectoryReader default behavior and explicitly supported extensions, and the set of specialized readers provided by the llama-index-readers-file package. Practical tips and integration examples are included.

## High-level summary
- LlamaParse: supports 130+ file formats across Documents, Images, Spreadsheets, and Audio; commonly used formats include PDF, DOCX, PPTX, XLSX, TXT, HTML, EPUB, JPG/PNG, CSV/TSV, and common audio/video types (MP3, MP4, WAV, M4A, WEBM).
- SimpleDirectoryReader: built-in convenience loader that attempts to read files as text by default and explicitly recognizes a set of common extensions (CSV, DOCX, EPUB, HWP, IPYNB, JPEG/JPG, MBOX, MD, MP3/MP4, PDF, PNG, PPT(X/M), etc.). It can be extended via the file_extractor mapping.
- llama-index-readers-file: a plugin/integration package that provides many specialized reader classes (DocxReader, PDFReader, PyMuPDFReader, IPYNBReader, PptxReader, PandasCSVReader, ImageReader, VideoAudioReader, UnstructuredReader, XMLReader, and more).

---

## Detailed listings

1) LlamaParse (cloud parsing service) — categories & sample extensions
- Documents (common): pdf, docx, doc, pptx, ppt, rtf, txt, epub
- Documents (additional examples): docm, dot, hwp, key, pages, pptm, potx, sxw, wpd, wps, xml, and many more (the service lists 130+ formats in total).
- Images: jpg, jpeg, png, gif, bmp, tiff, webp (also svg, htm/html for embedded markup scenarios)
- Spreadsheets: xlsx, xls, csv, tsv, numbers, ods (also xlsm, xlsb, dif, sylk, dbf, etc.)
- Audio/video: mp3, mp4, wav, m4a, webm (and other common codecs such as mpeg/mpga)

Notes: LlamaParse emphasizes table recognition, multimodal parsing (images/diagrams), and structured outputs (text, markdown, JSON). It is the recommended parser for complex layouts and multimodal content.

2) SimpleDirectoryReader — default explicit support
SimpleDirectoryReader will attempt to read any file as text by default. In addition, it explicitly recognizes the following (based on extension detection):
- .csv
- .docx
- .epub
- .hwp
- .ipynb
- .jpeg, .jpg
- .mbox
- .md
- .mp3, .mp4
- .pdf
- .png
- .ppt, .pptm, .pptx

Key features and behaviors:
- By default reads top-level directory; set recursive=True to include subdirectories.
- Use required_exts to restrict loaded extensions, or input_files to supply explicit file paths.
- Encoding defaults to UTF-8 but can be overridden.
- Extensible via file_extractor: pass a dict mapping file extensions to BaseReader instances (custom readers must return a list of Document objects).

3) llama-index-readers-file (readers integration / PyPI)
This integration provides many ready-made reader classes for more accurate parsing. Some of the supported readers include:
- DocxReader
- HWPReader
- PDFReader
- PyMuPDFReader
- EpubReader
- FlatReader (plain text)
- HTMLTagReader
- ImageCaptionReader
- ImageReader
- ImageVisionLLMReader
- IPYNBReader
- MarkdownReader
- MboxReader
- PptxReader (with options like extract_images, context_consolidation_with_llm)
- PandasCSVReader, CSVReader, PagedCSVReader
- VideoAudioReader
- UnstructuredReader
- ImageTabularChartReader
- XMLReader
- RTFReader

Usage pattern: install the package (pip install llama-index-readers-file), import desired reader classes and pass instances in the SimpleDirectoryReader file_extractor mapping for robust parsing of each extension.

---

## Practical guidance / recommendations
- For best results with mixed or complex documents (multi-column PDFs, images with captions, slides with visuals), use LlamaParse (cloud) or specialized readers (PyMuPDFReader, PDFReader, PptxReader) rather than the default plain-text fallback.
- If you rely on local parsing only, install llama-index-readers-file to obtain a wide set of robust readers that integrate with SimpleDirectoryReader.
- For unsupported proprietary formats: (a) check LlamaParse full list; (b) add a custom BaseReader for the extension; or (c) convert files to a supported format (PDF, TXT) in a preprocessing step.
- For images within documents or standalone images, use ImageReader or ImageVisionLLMReader if you need captions/extracted visual context.
- For tabular-heavy files, prefer PandasCSVReader / PagedCSVReader or let LlamaParse perform table recognition and structured output.
- For large ingestion volumes, use LlamaParse API/CLI with parallel workers and consider rate/volume limits for cloud plans.

---

## Example snippets
1) Use LlamaParse parser with SimpleDirectoryReader (Python)
```py
from llama_cloud_services import LlamaParse
from llama_index.core import SimpleDirectoryReader

parser = LlamaParse(api_key="llx-...", result_type="markdown")
file_extractor = {".pdf": parser}

documents = SimpleDirectoryReader("./data", file_extractor=file_extractor).load_data()
```

2) Use a local PDFReader from llama-index-readers-file
```py
from llama_index.core import SimpleDirectoryReader
from llama_index.readers.file import PDFReader

parser = PDFReader()
file_extractor = {".pdf": parser}

documents = SimpleDirectoryReader("./data", file_extractor=file_extractor).load_data()
```

---

## Sources
- Supported Document Types — LlamaParse: https://developers.llamaindex.ai/python/cloud/llamaparse/supported_document_types/
- LlamaParse overview & examples (GitHub): https://github.com/run-llama/llama_cloud_services/blob/main/parse.md
- SimpleDirectoryReader docs (readthedocs): https://llamaindexxx.readthedocs.io/en/latest/module_guides/loading/simpledirectoryreader.html
- PyPI — llama-index-readers-file (readers integration & supported reader classes): https://pypi.org/project/llama-index-readers-file/

(End of report.)
