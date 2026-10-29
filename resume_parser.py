import fitz


def extract_resume_text(pdf_file):
    """Extract readable text from an uploaded PDF resume."""

    try:
        pdf_bytes = pdf_file.read()

        with fitz.open(stream=pdf_bytes, filetype="pdf") as document:
            pages = []

            for page in document:
                text = page.get_text()

                if text.strip():
                    pages.append(text)

        return "\n".join(pages).strip()

    except Exception as error:
        raise ValueError(
            "Could not read this PDF. Please upload a valid PDF resume."
        ) from error