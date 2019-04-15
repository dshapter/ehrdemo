import re
import argparse
import io
import subprocess
from ehr_error import PDFParseException
from EHRPageProcessor import PageProcessor

from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage


class Record:
    def __init__(self, header=None, body=None):
        self.header = header
        self.body = ''
        self.page_data = None

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

def extract_text_from_pdf(pdf_path):
    resource_manager = PDFResourceManager()
    page_io_list = []
    text = None
    with open(pdf_path, 'rb') as fh:
        for page in PDFPage.get_pages(fh,
                                      caching=True,
                                      check_extractable=True):
            fake_file_handle = io.StringIO()
            converter = TextConverter(resource_manager, fake_file_handle)
            page_interpreter = PDFPageInterpreter(resource_manager, converter)
            page_interpreter.process_page(page)
            page_io_list.append(fake_file_handle)

        text = fake_file_handle.getvalue()

    #fake_file_handle.close()
    return page_io_list


def extract_text(input, pdf_extracter_cmd):
    cmd = [
        pdf_extracter_cmd,
        input,
        '-'
    ]
    output = subprocess.Popen(cmd,
                              stdout=subprocess.PIPE)
    return output.stdout.read()


def parse_pages(page_list):
    number_of_pages = len(page_list)
    if number_of_pages == 0:
        return # throw exception here
    encounter_index = 0
    records = []
    for page in page_list:
        # start a state machine
        page_text = page.getvalue()
        # use the 'Page x of y' to determine beginnings and end of encounters
        match = re.search('Page\s([0-9])\sof\s([0-9])', page_text)
        if not match:
            raise PDFParseException
        current_num_pages = 0
        page_number = int(match.group(1))
        encounter_pages = int(match.group(2))
        if page_number == 1:
            # this is a new encounter/record
            records.append(Record())
            records[encounter_index].add_text(page_text)
        else:
            records[encounter_index].add_text(page_text)
            if page_number == encounter_pages:
                # finished this encounter
                records[encounter_index].process_pages()
                encounter_index += 1

    print(len(records))




if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', help='PDF file to parse')
    parser.add_argument('--pdf_cmd', help='command to extract PDF')
    args = parser.parse_args()
    text = extract_text(args.input, args.pdf_cmd)
    tokens = text.decode().split('\n')
    #for token in tokens:
    #    print(token)
    page_list = extract_text_from_pdf(args.input)
    parse_pages(page_list)



