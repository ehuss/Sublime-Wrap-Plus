

import sys

import textwrap
import unittest


wrap_plus_module = sys.modules["Wrap Plus.wrap_plus"]


def run_unit_tests():
    runner = unittest.TextTestRunner()

    classes = \
    [
        SemanticLineWrapUnitTests,
        LineBalancingUnitTests,
    ]

    # Comment all the tests names on this list, to run all Unit Tests
    unit_tests_to_run = \
    [
        # "test_split_lines_with_trailing_new_line",
        # "test_split_lines_without_trailing_new_line",
        # "test_balance_characters_between_line_wraps_with_trailing_new_line",
        # "test_balance_characters_between_line_wraps_without_trailing_new_line",
        # "test_balance_characters_between_line_wraps_ending_with_long_word",
    ]

    runner.run( suite( classes, unit_tests_to_run ) )



class LineBalancingUnitTests(unittest.TestCase):

    @classmethod
    def setUp(self):
        self.maxDiff = None

        self.wrap_plus = wrap_plus_module.WrapLinesPlusCommand( None )
        self.wrap_plus._width = 50

        self.wrapper = textwrap.TextWrapper(break_long_words=False, break_on_hyphens=False)
        self.wrapper.subsequent_indent = "    "
        self.wrapper.expand_tabs = False

        global maximum_words_in_comma_separated_list
        maximum_words_in_comma_separated_list = 4

    def test_split_lines_without_trailing_new_line(self):
        self.assertEqual( [['    This is my very long line\n', '    which will wrap near its\n', '    end,']],
                self.wrap_plus._split_lines(
                self.wrapper, ["This is my very long line which will wrap near its end,"], 50, "    " ) )

    def test_split_lines_with_trailing_new_line(self):
        self.assertEqual( [['    This is my very long line\n', '    which will wrap near its\n', '    end,\n']],
                self.wrap_plus._split_lines(
                self.wrapper, ["This is my very long line which will wrap near its end,\n"], 50, "    " ) )

    def test_split_lines_with_very_long_line_and_word(self):
        self.assertEqual( [['    This is my very long line which my\n', '    very long line which\n', '    my_very_long_line_which_will_wrap_near_its_end,']],
                self.wrap_plus._split_lines(
                self.wrapper, [ "This is my very long line which my very long line which my_very_long_line_which_will_wrap_near_its_end," ], 50, "    " ) )

    def test_balance_characters_between_line_wraps_with_trailing_new_line(self):
        self.assertEqual( ['    ', 'This is my very long line which\n', '    will wrap near its end,\n'],
                self.wrap_plus.balance_characters_between_line_wraps(
                self.wrapper, ["This is my very long line which will wrap near its end,\n"], "    ", "    " ) )

    def test_balance_characters_between_line_wraps_without_trailing_new_line(self):
        self.assertEqual( ['    ', 'This is my very long line which\n', '    will wrap near its end,'],
                self.wrap_plus.balance_characters_between_line_wraps(
                self.wrapper, ["This is my very long line which will wrap near its end,"], "    ", "    " ) )

    def test_balance_characters_between_line_wraps_ending_with_long_word(self):
        self.wrap_plus._width = 80
        self.assertEqual( ['    ', 'In this proposal last chapter which lies on the part\n',
                "    called `\\nameref{sec:software_implementation}',"],
                self.wrap_plus.balance_characters_between_line_wraps(
                        self.wrapper, [ "In this proposal last chapter which lies on the part called "
                        "`\\nameref{sec:software_implementation}'," ], "    ", "    " ) )


class SemanticLineWrapUnitTests(unittest.TestCase):

    @classmethod
    def setUp(self):
        self.maxDiff = None
        self.wrap_plus = wrap_plus_module.WrapLinesPlusCommand( None )
        self.wrap_plus._width = 80

        global maximum_words_in_comma_separated_list
        maximum_words_in_comma_separated_list = 4

    def test_is_command_separated_list(self):
        self.is_comma_separated_list( "1, 2, 3, 4, 5", 1, True )
        self.is_comma_separated_list( "1_ 2, 3, 4_ 5", 4, True )
        self.is_comma_separated_list( "1_ 2, 3_ 4_ 5", 4, True )
        self.is_comma_separated_list( "1_ 2, 3_ 4, 5", 4, True )

    def test_is_command_separated_list_upperbound(self):
        self.is_comma_separated_list( "1, 2_ 3_ 4_ 5", 1, False )
        self.is_comma_separated_list( "1_ 2, 3_ 4_ 5 6, 7",  4, False )
        self.is_comma_separated_list( "1_ 2, 3_ 4__5 6_ 7",  4, False )
        self.is_comma_separated_list( "1_ 2, 3_ 4_ 5 6_ 7",  4, False )

    def test_is_command_separated_list_lowerbound(self):
        self.is_comma_separated_list( "1 2, 3 4_5 6, 7",  3, True )
        self.is_comma_separated_list( "1 2, 3_4_5 6, 7",  3, True )
        self.is_comma_separated_list( "1 2, 3_4_5_6, 7",  3, True )

    def is_comma_separated_list(self, text, index, goal):
        self.assertTrue( text[index] in wrap_plus_module.word_separator_characters )
        self.assertEqual( goal, self.wrap_plus.is_comma_separated_list( text, index, True )[0]
            or self.wrap_plus.is_comma_separated_list( text, index, False )[0] )

    def test_semantic_line_wrap_simple_sentences(self):
        self.semantic_line_wrap( "1", "1" )
        self.semantic_line_wrap( "which will take, you quite some time",
        "which will take,\nyou quite some time" )

        self.semantic_line_wrap( "which will take, you, quite some time",
        "which will take,\nyou, quite some time" )

    def test_semantic_line_wrap_long_word(self):
        self.semantic_line_wrap( "quitesometimequitesometimequitesometimequitesometimequitesometimequitesometimequitesometime",
        "quitesometimequitesometimequitesometimequitesometimequitesometimequitesometimequitesometime" )

    def test_semantic_line_wrap_ending_with_comma_list(self):
        self.semantic_line_wrap( "you still only configuring a few languages closely related. On this case, C, C++, Java, Pawn, etc.",
        "you still only configuring a few languages closely related.\nOn this case, C, C++, Java, Pawn, etc." )

    def test_semantic_line_wrap_with_comma_list_on_the_middle(self):
        self.semantic_line_wrap( "which will not more take, you quite oh the time, some time, more time, the time, per time",
        "which will not more take,\nyou quite oh the time,\nsome time, more time, the time, per time" )

    def test_semantic_line_wrap_with_comma_list_on_the_end(self):
        self.semantic_line_wrap( "few languages close related. On this case, C, C++, Java, Pawn, etc. more over break this line",
        "few languages close related.\nOn this case, C, C++, Java, Pawn, etc.\nmore over break this line" )

    def test_semantic_line_wrap_with_numeric_comma_list_on_the_end(self):
        self.semantic_line_wrap( "1 2 3 4. 5 6 7, 1, 2, 3, 4, 5. 6 7 8 9 1",
        "1 2 3 4.\n5 6 7, 1, 2, 3, 4, 5.\n6 7 8 9 1" )

    def test_semantic_line_wrap_with_long_word_at_comma_list_end(self):
        self.semantic_line_wrap( "For all other languages you still need to find out another source code "
                "formatter tool, which will be certainly limited\\footnote{\\url{https://stackoverflow.com/"
                "questions/31438377/how-can-i-get-eclipse-to-wrap-lines-after-a-period-instead-of-before}}",

                "For all other languages you still need to find out another source code "
                "formatter\ntool,\nwhich will be certainly\nlimited\\footnote{\\url{https://stackoverflow.com/"
                "questions/31438377/how-can-i-get-eclipse-to-wrap-lines-after-a-period-instead-of-before}}" )

    def test_semantic_line_wrap_with_80_characters(self):
        self.semantic_line_wrap( [ "few languages close related. On this case, C, C++, Javas, Pawn, if, you, already, had, written, the, program, assure, everything, is, under, versioning, control, system, and, broke, everything, etc. more over break this line", "", "" ],
            "few languages close related.\nOn this case, C, C++, Javas, Pawn, if, you, already, had, written, the, program,\nassure, everything, is, under, versioning, control, system, and, broke,\neverything, etc.\nmore over break this line" )

    def test_semantic_line_wrap_with_79_characters(self):
        self.semantic_line_wrap( [ "few languages close related. On this case, C, C++, Java, Pawn, if, you, already, had, written, the, program, assure, everything, is, under, versioning, control, system, and, broke, everything, etc. more over break this line", "", "" ],
            "few languages close related.\nOn this case, C, C++, Java, Pawn, if, you, already, had, written, the, program,\nassure, everything, is, under, versioning, control, system, and, broke,\neverything, etc.\nmore over break this line" )

    def test_semantic_line_wrap_with_81_characters(self):
        self.semantic_line_wrap( [ "few languages close related. On this case, C, C++, Javas, Pawns, if, you, already, had, written, the, program, assure, everything, is, under, versioning, control, system, and, broke, everything, etc. more over break this line", "", "" ],
            "few languages close related.\nOn this case, C, C++, Javas, Pawns, if, you, already, had, written, the,\nprogram, assure, everything, is, under, versioning, control, system, and, broke,\neverything, etc.\nmore over break this line" )

    def test_semantic_line_wrap_with_81_characters_on_list_flushing(self):
        self.semantic_line_wrap( [ "few languages close related. On this case, C, C++, Javas, Pawns, if, you, already, had, written, the, programs, assure, everything, is, under, versioning, control, system, and, broke, everything, etc. more over break this line", "", "" ],
            "few languages close related.\nOn this case, C, C++, Javas, Pawns, if, you, already, had, written, the,\nprograms, assure, everything, is, under, versioning, control, system, and,\nbroke, everything, etc.\nmore over break this line" )

    def test_semantic_line_wrap_with_initial_indentation(self):
        self.semantic_line_wrap( [ "For all other languages you still need to find out another source code f tool, "
                "which will be certainly limited and still need to configure all over again.", "    ", "    " ],
                "    For all other languages you still need to find out another source code f\n"
                "    tool,\n"
                "    which will be certainly limited and still need to configure all over again." )

    def semantic_line_wrap(self, initial_text, goal):

        if isinstance( initial_text, list ):
            self.assertEqual( goal, "".join( self.wrap_plus.semantic_line_wrap( [initial_text[0]], initial_text[1], initial_text[2] ) ) )

        else:
            self.assertEqual( goal, "".join( self.wrap_plus.semantic_line_wrap( [initial_text], "", "" ) ) )


def suite(classes, unit_tests_to_run):
    """
        Problem with sys.argv[1] when unittest module is in a script
        https://stackoverflow.com/questions/2812218/problem-with-sys-argv1-when-unittest-module-is-in-a-script

        Is there a way to loop through and execute all of the functions in a Python class?
        https://stackoverflow.com/questions/2597827/is-there-a-way-to-loop-through-and-execute-all-of-the-functions

        looping over all member variables of a class in python
        https://stackoverflow.com/questions/1398022/looping-over-all-member-variables-of-a-class-in-python
    """
    suite = unittest.TestSuite()
    unit_tests_to_run_count = len( unit_tests_to_run )

    for _class in classes:
        _object = _class()

        for function_name in dir( _object ):

            if function_name.lower().startswith( "test" ):

                if unit_tests_to_run_count > 0 \
                        and function_name not in unit_tests_to_run:

                    continue

                suite.addTest( _class( function_name ) )

    return suite


