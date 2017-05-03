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
        """
                    Return number of vehicles within the given plates
                    :param number_plate_a: A number plate string
                    :param number_plate_b: A number plate string
                    :type number_plate_a: str
                    :type number_plate_b: str
                    :returns: number of vehicles between the given plates
                    :rtype: int
        """
        # Assert authenticity of  number plates given
        assert self.get_number_plate(number_plate_a), "Please pass a valid Kenyan number plate"
        assert self.get_number_plate(number_plate_b), "Please pass a valid Kenyan number plate"

        number_plate_a = number_plate_a.lower()
        number_plate_b = number_plate_b.lower()

        # check if the number plates are the same and return 0
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

            # These are factors that we multiply with depending on the placement of the changed character
            multiplying_factors = [0, 675324, 25974, 999]
            # get the total number of vehicles in  each character of the number plate
            plate_a_total_vehicles = self.vehicles_in_a_number_plate(list_a, multiplying_factors)
            plate_b_total_vehicles = self.vehicles_in_a_number_plate(list_b, multiplying_factors)

            # since from KC->KB there are 675324 we subtract the other values to get actual vehicles
            plate_a_vehicles = plate_a_total_vehicles[1] - plate_a_total_vehicles[2] - plate_a_total_vehicles[3] - int(
                number_plate_digits_a)
            plate_b_vehicles = plate_b_total_vehicles[1] - plate_b_total_vehicles[2] - plate_b_total_vehicles[3] - int(
                number_plate_digits_b)

            # since the number plates can be entered in any order, we check the largest and subtract from the smallest
            # then subtract 1 since we don't  want to include the plate we are checking
            if plate_a_vehicles > plate_b_vehicles:
                return plate_a_vehicles - plate_b_vehicles - 1
            return plate_b_vehicles - plate_a_vehicles - 1

    @staticmethod
    def vehicles_in_a_number_plate(list_a, multiplying_factors):
        """
        Return number of vehicles within the given plates
            :param list_a: A list of numbers
            :param multiplying_factors: a list of numbers
            :type list_a: list
            :type multiplying_factors: list
            :returns: a list with number of vehicles per number plate character
            :rtype: list
        """
        return [x1 * x2 for (x1, x2) in zip(list_a, multiplying_factors)]

    @staticmethod
    def plate_characters(number_plate):
        """
            Return characters in a number plate
            :param number_plate: A list of numbers
            :type number_plate: list
            :returns: a list of characters in a number plate
            :rtype: list
        """
        return ''.join(re.findall("[a-zA-Z]+", number_plate, re.M | re.I))

    @staticmethod
    def plate_digits(number_plate):
        """
                Return characters in a number plate
                :param number_plate: A list of string
                :type number_plate: list
                :returns: a list of  digits in  a number plate
                :rtype: list
        """
        return ''.join(re.findall("\d{3}", number_plate, re.M | re.I))
