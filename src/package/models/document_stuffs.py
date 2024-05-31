import pymupdf
from collections import defaultdict
from typing import List, Dict

class CustomSection:
    def __init__(self, section_title, section_text):
        self.title = section_title
        self.text = section_text
        
    # =======================================
    #                  DUNDERS
    # =======================================
    
    def __getitem__(self, idx):
        return self.text[idx]
    
    def __len__(self):
        return len(self.text)
    
    def __str__(self):
        return f"Custom section {self.title}"
    
    def __repr__(self):
        return str(self)

class CustomPage:
    def __init__(self, page_number: int, page: pymupdf.Page, page_headings: List[str]):
        text = page.get_text("text")
        image_list = page.get_images(full=True)
        self.just_text = text                                  # internal use for analysis
        self.page_number = page_number
        self.num_sections = len(page_headings)
        self.num_chars = len(text)
        self.num_images = len(image_list)
        self.sections = self._make_sections(text, page_headings)
        # images itself
        # page number
        # should have a text attribute and a sections attribute
    
    def _make_sections(self, text: str, page_headings) -> List[CustomSection]:
        sections = defaultdict(list)
        lines = text.split("\n")
        current_heading = page_headings.pop(0)
        next_heading = page_headings.pop(0) if page_headings else None
        for line in lines:
            if next_heading and next_heading.split(":")[-1] in line:
                current_heading = next_heading
                next_heading = page_headings.pop(0) if page_headings else None
            sections[current_heading].append(line)
        page_headings += [current_heading] # here for overflow which we want
        return [CustomSection(title, "\n".join(text)) for title, text in sections.items()]

    # =======================================
    #                  DUNDERS
    # =======================================
    def __getitem__(self, idx):
        return self.sections[idx]

    def __str__(self):
        s = ""
        for section in self.sections:
            s += section.title + "\n"
        return f"Page {self.page_number} of document. Has {len(self.sections)} sections: \n" + s

    def __repr__(self):
        return str(self)

class CustomDocument:
    def __init__(self, file_path):
        pymupdf_doc = self._load_pdf(file_path)
        labels: Dict[int, List[str]] = self._create_multilevel_headings(pymupdf_doc.get_toc())
        self.file_path = file_path
        self.metadata = pymupdf_doc.metadata
        self.pages = self._create_pages(labels, pymupdf_doc)
        
    def _load_pdf(self, file_path: str) -> pymupdf.Document:
        """Load pdfs"""
        pdf = pymupdf.open(file_path)
        return pdf

    def _create_multilevel_headings(self, table_of_content: List[List[int]]) -> Dict[int, List[str]]:
        """given a pdf table of content we get a heading id to chunk properly"""
        page_mapping = defaultdict(list)
        current_heading = []
        for heading_level, heading_title, page_number in table_of_content: 
            # check if the criterion is met
            if heading_level <= len(current_heading):
                current_heading = current_heading[:heading_level - 1] # in the case of headinglevel = 1 it returns an empty list
            current_heading.append(heading_title)
    
            # add the joined headers
            page_mapping[page_number].append(":".join(current_heading))
            
        return page_mapping

    def _create_pages(self, labels: Dict[int, List[str]], doc: pymupdf.Document) -> List[CustomPage]:
        pages, page_headings = [], []
        for page_num, page in enumerate(doc):
            page_num += 1
            page_headings += labels.get(page_num, ["Other"])
            pages.append(CustomPage(page_num, page, page_headings)) # headings should go away once popped
        return pages
        
    def get_full_text(self) -> str:
        """Text I would need to do analysis and show end users"""
        full_text = []
        for page_num, page in enumerate(self.pages):
            page_num += 1
            full_text.append(f"Page {page_num}:")
            for section in page.sections:
                full_text.append(section.text)
        return "\n".join(full_text)
    # =======================================
    #                  DUNDERS
    # =======================================
    def __getitem__(self, idx):
        return self.pages[idx]

    def __str__(self):
        return f"PDF of {self.file_path}, has {len(self.pages)} pages. Use .metadata attribute to see more"

    def __repr__(self):
        return str(self)    