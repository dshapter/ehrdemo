from EHRPageProcessor import PageProcessor, Helper
from ehr_error import PDFParseException


class Record:
    def __init__(self, header=None, body=None):
        self.header = header
        self.body = ''
        self.page_data = None
        self.helper = None

    def add_text(self,text):
        self.body += text

    def extract_pages(self, text):
        match = re.search('(.+)({}.+)'.format(PageOne.keywords[0]), text)
        header = ''
        if match:
            header = match.group(1)
            self.body = match.group(2)
        else:
            raise PDFParseException
        header = header.replace('NameChart#DOBRefer Doctor', '')
        header = header.replace('DateLocationPCPInsurance', '')
        self.header = header
        self.body = match.group(2)
        self.process_pages()

    def process_pages(self):
        self.page_data = PageProcessor(self.body)
        return

    def add_helper_text(self, text, encounter):
        self.helper = Helper(text, encounter)
        pass

    def post_process(self):
        print (self.page_data.va)
