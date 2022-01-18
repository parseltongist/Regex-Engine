import sys
from colorama import init, Fore

init(autoreset=True)


sys.setrecursionlimit(50)


def metachar_preprocessing(_string, _template):
    if _template:
        if _template[0] in "*?+":
            print("REGEX PATERN ERROR. you can't have '*?+' at the beginning of the string\nTRY AGAIN")
            return main()
        if _template[0] == "^":
            _template = _template[1:]
            _string = _string[:len(_template)]
        if _template[-1] == "$":
            if not char_match(_template[-2], _string[-1]):
                return "a", "b"  # temporarily fix to repr "FALSE"
            else:
                _template = _template[:-1]
                _string = _string[-len(_template):]
    return _template, _string


def char_match(_regex_char, _char) -> bool:
    return any([not _regex_char, _regex_char == ".", _regex_char == _char])


def string_match(_template, _string):
    #print("Checking:", _template, _string)


    loop_range = min([len(_template), len(_string)])

    #print("Loop range is: ", loop_range)

    for i in range(loop_range):
        try:
            if not char_match(_template[i], _string[i]):
                #print(f"line #36: {_template[i]} doesn't match {_string[i]}\n")

                if "?" in _template:
                    next_step = 1 if _template[i] == "?" else 2

                    # print("the step value is", next_step)

                    #print(f"trying to match {_template[i + next_step]} and {_string[i]}")
                    next_symbol_check = char_match(_template[i + next_step], _string[i])  # skipping '?' and comparing next mandatory sign, test 'ca?t|cat'

                    # print(f"the result of this try is {next_symbol_check:}")

                    if not next_symbol_check:  # problem  that this variable doesn't change it's name
                        return False
                    i += 1
                    if i == loop_range:
                        return True

                    # return True # fixing 1 test but breaks 3

                """ * funcitons is not yet done, just copied from above '?' fun"""

                if "*" in _template:
                    #print("line #63 triggered\n")
                    # re-write the logic, as steps must be different. example be*|beer  be|br
                    next_step = 1 if _template[i] == "*" else 2

                    # print("Step: ", next_step)

                    # need to check both repeat and 0 scenario:

                    if _template[i-1] == _string[i]:  # repeative letter case
                        #print("line 76")
                        _string = _string[:i] + _string[i::].strip(_template[i-1])  # cut repittive leters in _string

                        loop_range = min([len(_template), len(_string)])
                        # try call this the same fun here

                        next_symbol_check = char_match(_template[i + next_step], _string[i])
                        if not next_symbol_check:
                            return False

                        i += 1
                        if i == loop_range:
                            return True

                    elif _template[i-1] == ".":
                        #print("LINE 86. case with repitive dot!")
                        #print("ORIGINAL VALUES: ", _template, _string)
                        #print(_template[i+1], _string[i+1])

                        # removing repittive signs.
                        _string = _string[:i+1] + _string[i+1::].strip(_string[i])

                        _template = _template[i+1::]
                        _string = _string[i+1::]

                        loop_range = min([len(_template), len(_string)])

                        return string_match(_template, _string)





                    elif _template[i+1] == _string[i]:  # abscent letter case
                        #print("Line # 81", _template[i-1])
                        # WORKS

                        # CHECK BELOW string if - is ok?
                        next_symbol_check = char_match(_template[i - next_step], _string[i])
                        if not next_symbol_check:
                            return False

                        i += 1
                        if i == loop_range:
                            return True

                    elif _template[i+1] == _string[i]:  # 0 repititions, (letter presented only once here)
                        #print('line 86')
                        pass


                        next_symbol_check = char_match(_template[i + next_step], _string[i])
                        #print(f"the result of this try is {next_symbol_check:}")
                        if not next_symbol_check:
                            return False

                        i += 1
                        if i == loop_range:
                            return True

                else:  # in none of IFs triggered
                    return False

        except IndexError:
            return _template[i] == _template[-1] == '?'  # should be True :)
    return True


def template_without_optional_chars(_template):
    symbols = {"*", "?"}
    while any(["?" in _template, "*" in _template]):
        for s in symbols:
            index = _template.find(s)
            if index != -1:
                _template = _template[:index - 1] + _template[index + 1:]
    return _template


def full_match(_template, _string, i=0):
    # if _template and not _string - checking if _template will still be True after removing optional characters.
    if _template and not _string:
        if template_without_optional_chars(_template):
            return False
        # if _template is bigger than _string - checking if that is taht case after removing optional characters.
        elif len(_template) > len(_string):
            if len(template_without_optional_chars(_template)) > len(_string):
                return False
    elif not _template:
        return True


    if string_match(_template, _string):
        return True

    else:

        i = 1
        # creating the loop and checking if template can be found in string
        while i < len(_string):

            if string_match(_template, _string[i:]):
                return True
            #print(" increasing counter line # 100  +=1 ")
            i += 1

        # ISSUE WITH THIS LOOP.  STRING_MATCH FUNCTION IS OK. I need to terminate the loop once no longer element in the string
        return False


def main():

    try:
        template, string = input().split("|")
        # template, string = "col.*r|colouuuuuuuuuuur".split("|")
    except ValueError:
        print("ERROR! Input should be like a|a. Please try again")
        return main()
    # template, string = metachar_preprocessing("colou*r|colouur")  # for tests
    template, string = metachar_preprocessing(string, template)
    print(full_match(template, string))


def run_tests():
    # test input -> answer
    test_pool = {'colou?r|color': True,
                 'colou?r|colour': True,
                 'colou?r|colouur': False,
                 'colou*r|color': True,
                 'colou*r|colour': True,
                 'colou*r|colouur': True,
                 'col.*r|color': True,
                 'col.*r|colour': True,
                 'col.*r|colr': True,
                 'col.*r|collar': True,
                 'col.*r$|colors': False,
                 }

    failed_tests = []
    for pair in test_pool.keys():
        # failed tests at this moment:
        ['colou?r|color', 'colou?r|colour', 'colou*r|colouur', 'col.*r|colour', 'col.*r|collar']
        template, string = pair.split("|")

        template, string = metachar_preprocessing(string, template)

        #print(f"\n\nSTART MATCHING {template} and {string}\n\n")

        # print(full_match(template, string))
        print(f"{pair} {Fore.GREEN}passed" if full_match(template, string) == test_pool[pair] else f"{pair} {Fore.RED} failed")


if __name__ == '__main__':
    #main()
    run_tests()