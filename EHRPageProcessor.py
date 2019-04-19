import re


class PageProcessor:
    keywords = ['Reason\sFor\sVisit:',
                'HPI:',
                'Secondary:',
                'Ocular\sMeds\s\(Initial\):',
                'Mental\sStatus:',
                'PSFH/ROS\sUpdated\sDate:',
                'Medical\sHx:',
                'Surgical\sHx:',
                'Systemic\sMeds:',
                'Allergies:',
                'Family\sHx:',
                'Social\sHx:',
                'ROS:',
                'VA',
                'IOP:',
                'Dilation:',
                'External',
                'Anterior',
                'Posterior'
                ]
    
    def __init__(self, text):
        self.text = text
        self.substring = text
        self.reason = None
        self.hpi = None
        self.secondary = None
        self.ocular_meds = None
        self.mental_state = None
        self.psh_ros_update_data = None
        self.medical_history = None
        self.surgical_history = None
        self.systemic_meds = None
        self.allergies = None
        self.family_hx = None
        self.social_hx = None
        self.ros = None
        self.va = None
        self.iop = None
        self.dilation = None
        self.external = None
        self.anterior = None
        self.posterior = None
        self.extract_pairs()

    def extract_pairs(self):
        index = 0
        self.reason = self.lookup(index)
        index += 1
        self.hpi = self.lookup(index)
        index += 1
        self.secondary = self.lookup(index)
        index += 1
        self.ocular_meds = self.lookup(index)
        index += 1
        self.mental_state = self.lookup(index)
        index += 1
        self.psh_ros_update_data = self.lookup(index)
        index += 1
        self.medical_history = self.lookup(index)
        index += 1
        self.surgical_history = self.lookup(index)
        index += 1
        self.systemic_meds = self.lookup(index)
        index += 1
        self.allergies = self.lookup(index)
        index += 1
        self.family_hx = self.lookup(index)
        index += 1
        self.social_hx = self.lookup(index)
        index += 1
        self.ros = self.lookup(index)
        index += 1
        self.va = self.lookup(index)
        index += 1
        self.iop = self.lookup(index)
        index += 1
        self.dilation = self.lookup(index)
        index += 1
        self.external = self.lookup(index)
        index += 1
        self.anterior = self.lookup(index)
        index += 1
        self.posterior = self.lookup(index)

    def lookup(self, index):
        if index+1 < len(self.keywords):
            search_string = '({})(.+)({})'.format(self.keywords[index], self.keywords[index+1])
            match = re.search(search_string, self.substring)
            if match:
                self.substring = self.substring[match.start(3):]
                return match.group(2)
        else:
            search_string = '({})(.+)'.format(self.keywords[index])
            match = re.search(search_string, self.substring)
            if match:
                return match.group(2)
        return None

class Helper:
    '''
    This is a cheater class using the complete PDF text as extracted from
    the command line tool. The idea here is ues this  class to help
    post process any ambiguous text blocks found in the main page processr.
    '''
    def __init__(self, text, encounter):
        self.text = text.decode()
        self.iop = ''
        enc = 0
        start = 0
        # TODO: figure out logic here; not getting the right values for IP
        while True:
            match = re.search('IOP', self.text[start:])
            if match:
                start = match.end()
                if enc == encounter:
                    tokens = self.text[start:].split('\n')
                    for i in range(5):
                        if i % 2 == 0:
                            self.iop += tokens[i].replace('\n', ' ')
                            self.iop += ' '
                    break

            enc += 1

