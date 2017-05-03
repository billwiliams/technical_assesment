import re


class Vehicle:
    def __init__(self):
        pass

    def get_number_plate(self, sentence):
        """
            Return kenyan number plates in a given sentence
            :param sentence: A string to extract number plates
            :type sentence: str
            :returns: a list with kenyan number plates
            :rtype: list
            """
        # assert that the given parameter is a string
        assert isinstance(sentence, str), 'Argument of wrong type.Please pass a string parameter'

        # pattern to match the number plates start with a K followed by 2 alphabetic letters followed by 3 digits then a
        # single alphabetic letter. the first part can also be separated by a single or multiple spaces

        pattern = 'K[a-z]{2}\d{3}[a-z]{1}|K[a-z]{2}\s+\d{3}[a-z]{1}'

        # find all the matched instances of the pattern ignoring the case and including mulltiline string
        number_plates = re.findall(pattern, sentence, re.M | re.I)

        # check if result has 000 in digit part since only from 001 is allowed

        collect_number_plates = [number_plate for number_plate in number_plates if (re.findall('\d{3}', number_plate, re.M | re.I) != ['000'])]

        # return corresponding results
        return collect_number_plates
