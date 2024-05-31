import pymupdf
from typing import List

class Chunk:
    def __init__(self, text: str, metadata):
        self.text = text
        self.metadata = metadata
        
class CustomCharacterTextSplitter:
    def __init__(self, num_chars: int = 256, overlap: int = 0):
        self.num_chars = num_chars
        self.overlap = overlap

    def split_document(self, doc: pymupdf.Document) -> List[Chunk]:
        chunks = []
        section_md = []
        page_number_md = []
        remainder = 0
        overflow = False
        chunk_text = ""
        for page in doc:
            for section in page:
                if overflow:
                    window_end = remainder
                    section_md.append(section.title) if section_md[-1] != section.title else None
                    page_number_md.append(page.page_number) if page_number_md[-1] != page.page_number else None
                else:
                    window_end = self.num_chars
                    section_md = [section.title]
                    page_number_md = [page.page_number]
                    
                section_length = len(section)
                window_start   = 0
                
                while window_start < section_length:
                    chunk_text += section[window_start:window_end]
                    chunk_metadata = {"page": tuple(page_number_md), "section": tuple(section_md)}
                    
                    if window_end > section_length:
                        remainder = window_end - section_length
                        overflow = True
                        break
                    else:
                        chunks.append(Chunk(chunk_text, chunk_metadata))
                        chunk_text = ""
                        window_start = window_end - self.overlap
                        window_end   += self.num_chars - self.overlap
                        overflow = False

        return chunks