# LlamaIndex / LlamaParse — Supported File Types

## Executive summary
LlamaParse (integrated with LlamaIndex) supports 130+ file formats across four primary categories: Documents, Images, Spreadsheets, and Audio. The sections below list the most common file extensions and additional supported formats, plus practical notes on loaders and integration (SimpleDirectoryReader, LlamaParse CLI/API).

## Key categories and file extensions
Data below is summarized from the LlamaParse / LlamaIndex documentation.

1) Documents (common)
- pdf, docx, doc, pptx, ppt, rtf, txt, epub

Also supported (examples from full list):
- 602, abw, cgm, cwk, docm, dot, dotm, hwp, key, lwp, mw, mcw, pages, pbd, pptm, pot, potm, potx, sda, sdd, sdp, sdw, sgl, sti, sxi, sxw, stw, sxg, uof, uop, uot, vor, wpd, wps, xml, zabw

2) Images (common)
- jpg, jpeg, png, gif, bmp, tiff, webp

Also supported (examples):
- svg, htm, html

3) Spreadsheets (common)
- xlsx, xls, csv, tsv, numbers, ods

Also supported (examples):
- xlsm, xlsb, xlw, dif, sylk, slk, prn, et, fods, uos1, uos2, dbf, wk1	6wk4, wks, 123, wq1, wq2, wb1	6wb3, qpw, xlr, eth

4) Audio (common)
- mp3, mp4, wav, m4a, webm

Also supported (examples):
- mpeg, mpga

Notes: the official LlamaParse documentation indicates "130+ file formats" and provides an extensive supported list beyond the common formats above.

## Loaders & integration
- LlamaParse provides a CLI (llama-parse) and Python API (llama_cloud_services.LlamaParse) to parse files and emit outputs as text, Markdown, or structured JSON. Example CLI usage from the repo: `llama-parse my_file.pdf --result-type text --output-file output.txt`.
- LlamaParse integrates with LlamaIndex's SimpleDirectoryReader; you can pass a parser instance as a file_extractor mapping (e.g., `{".pdf": parser}`) so SimpleDirectoryReader will use LlamaParse for those extensions.
- SimpleDirectoryReader and the LlamaIndex loader system are extensible: you can add custom file extractors/readers by mapping file extensions to reader objects that return Document lists.

## Practical tips
- If you have uncommon or proprietary file types, check whether a direct extension is listed in the full supported list; if not, add a custom BaseReader or pre-convert the file to a supported format (e.g., PDF or TXT) before ingestion.
- For multimodal content (images inside PDFs, diagrams), LlamaParse can extract images and return image documents; the API supports downloading image bytes or returning them as part of the parsed result.
- For large-scale or high-volume ingestion, prefer the LlamaParse API/CLI which supports batching and parallel workers.

## Short example (Python) — using LlamaParse + SimpleDirectoryReader
```py
from llama_cloud_services import LlamaParse
from llama_index import SimpleDirectoryReader

parser = LlamaParse(api_key="llx-...", result_type="markdown")
file_extractor = {".pdf": parser}

documents = SimpleDirectoryReader("./data", file_extractor=file_extractor).load_data()
```

## Sources
- Supported Document Types — LlamaParse (developers.llamaindex.ai): https://developers.llamaindex.ai/python/cloud/llamaparse/supported_document_types/
- LlamaParse overview and examples (GitHub): https://github.com/run-llama/llama_cloud_services/blob/main/parse.md

(Report generated from the cited documentation and repository examples.)
