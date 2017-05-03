import re
import string


class Vehicle:
    def __init__(self):
        pass

    @staticmethod
    def get_number_plate(sentence):
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

        collect_number_plates = [number_plate for number_plate in number_plates if
                                 (re.findall('\d{3}', number_plate, re.M | re.I) != ['000'])]

        # return corresponding results
        return collect_number_plates

    def number_of_vehicles(self, number_plate_a, number_plate_b):
        number_plate_a = number_plate_a.lower()
        number_plate_b = number_plate_b.lower()
        if number_plate_a.replace(" ", "") == number_plate_b.replace(" ", ""):
            return 0
        else:
            characters = sorted(set(string.ascii_letters.lower()))
            # map characters to the numeric equivalent in integers
            mapped_characters = dict(zip(characters, [ord(character) % 32 for character in characters]))
            # obtain the character and digit parts of the number plate
            number_plate_characters_a = self.plate_characters(number_plate_a)
            number_plate_characters_b = self.plate_characters(number_plate_b)
            number_plate_digits_a = self.plate_digits(number_plate_a)
            number_plate_digits_b = self.plate_digits(number_plate_b)
            # change the character part into number to compute changes
            list_a = [mapped_characters[c] for c in number_plate_characters_a]
            list_b = [mapped_characters[c] for c in number_plate_characters_b]
            # get the difference in the number plates
            diff = [x1 - x2 for (x1, x2) in zip(list_a, list_b)]
            # These are factors that we multiply with depending on the placement of the changed character
            multiplying_factors = [0, 675324, 25974, 999]
            # we multiply the difference with the factors to obtain the respective changes when we wiggle a character
            character_change_values = [x1 * x2 for (x1, x2) in zip(diff, multiplying_factors)]
            # we calculate the changes in the digit part and last character
            digit_changes = character_change_values[3] - int(number_plate_digits_b) + int(number_plate_digits_a) - 1
            number_of_cars = character_change_values[1] - character_change_values[2] - digit_changes
            if number_of_cars < 1:
                return -number_of_cars
            return number_of_cars

    @staticmethod
    def plate_characters(number_plate):
        return ''.join(re.findall("[a-zA-Z]+", number_plate, re.M | re.I))

    @staticmethod
    def plate_digits(number_plate):
        return ''.join(re.findall("\d{3}", number_plate, re.M | re.I))
