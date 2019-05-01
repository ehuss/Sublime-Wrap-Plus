

import os
import sys

import textwrap
import unittest

PACKAGE_ROOT_DIRECTORY = os.path.dirname( os.path.dirname( os.path.realpath( __file__ ) ) )
CURRENT_PACKAGE_NAME = os.path.basename( PACKAGE_ROOT_DIRECTORY ).rsplit('.', 1)[0]
wrap_plus_module = sys.modules[CURRENT_PACKAGE_NAME + ".wrap_plus"]


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

    # calculate_lines_count Unit Tests
    def test_calculate_lines_count_with_maximum_lines_indent(self):
        line = "This is my very long line which will wrap near its end,"
        indentation = "                                                            "
        result = self.wrap_plus.calculate_lines_count( line, indentation, indentation, 50 )
        self.assertEqual( (138, 8335), result )

    def test_calculate_lines_count_with_minimum_lines_indent(self):
        line = "This is my very long line which will wrap near its end,"
        indentation = ""
        result = self.wrap_plus.calculate_lines_count( line, indentation, indentation, 50 )
        self.assertEqual( (2, 55), result )

    def test_calculate_lines_count_with_only_one_line(self):
        line = "This is my very long line which will wrap near its end,"
        indentation = ""
        result = self.wrap_plus.calculate_lines_count( line, indentation, indentation, 80 )
        self.assertEqual( (1, 55), result )

    # _split_lines Unit Tests
    def test_split_lines_with_long_subsequent_indentation(self):
        self.wrapper.subsequent_indent = "                      "
        self.assertEqual( [['This is my very long line which will\n', '                      wrap near its\n', '                      end,']],
                self.wrap_plus._split_lines(
                self.wrapper, ["This is my very long line which will wrap near its end,"], 50 ) )

    def test_split_lines_without_trailing_new_line(self):
        self.assertEqual( [['This is my very long line\n', '    which will wrap near its\n', '    end,']],
                self.wrap_plus._split_lines(
                self.wrapper, ["This is my very long line which will wrap near its end,"], 50 ) )

    def test_split_lines_with_trailing_new_line(self):
        self.assertEqual( [['This is my very long line\n', '    which will wrap near its\n', '    end,\n']],
                self.wrap_plus._split_lines(
                self.wrapper, ["This is my very long line which will wrap near its end,\n"], 50 ) )

    def test_split_lines_with_very_long_line_and_word(self):
        self.assertEqual( [['This is my very long line which my\n', '    very long line which\n', '    my_very_long_line_which_will_wrap_near_its_end,']],
                self.wrap_plus._split_lines(
                self.wrapper, [ "This is my very long line which my very long line which my_very_long_line_which_will_wrap_near_its_end," ], 50 ) )

    # balance_characters_between_line_wraps Unit Tests
    def test_balance_characters_between_line_wraps_with_long_subsequent_indentation(self):
        indent = "%                                         "
        input_text = "% tests dd açsdkjflçk çalskdj fçlakj lçkasjd fçlakjs dçflkjadd açsdkjflçk çalskdj fçlakj lçkasjd fçlakjs dçflkja"
        expected_list = \
        [
            '',
            '% tests dd açsdkjflçk çalskdj fçlakj lçkasjd\n',
            '%                                         fçlakjs\n',
            '%                                         dçflkjadd\n',
            '%                                         açsdkjflçk\n',
            '%                                         çalskdj\n',
            '%                                         fçlakj\n',
            '%                                         lçkasjd\n',
            '%                                         fçlakjs\n',
            '%                                         dçflkja'
        ]
        self.assertEqual( expected_list,
                self.wrap_plus.balance_characters_between_line_wraps(
                self.wrapper, [input_text], "", indent ) )

    def test_balance_characters_between_line_wraps_with_big_multi_line_balancing(self):
        self.wrap_plus._width = 80
        input_text = \
        [
            "Inclui a IA para reconhecer o formatação nos módulos de beautifying.",
            "Ela eh uma heurística,",
            "que cada bloco implementa e faz ele gerar um arquivo de configuração que representa a atual formatação do código (aqui esta o verdadeiro desafio do trabalho,",
            "pesquise trabalhos correlatos).",
        ]
        expected_list = \
        [
            '% ',
            'Inclui a IA para reconhecer o formatação nos módulos de beautifying.',
            '% ',
            'Ela eh uma heurística,',
            '% ',
            'que cada bloco implementa e faz ele gerar um arquivo de\n',
            '% configuração que representa a atual formatação do código\n',
            '% (aqui esta o verdadeiro desafio do trabalho,',
            '% ',
            'pesquise trabalhos correlatos).',
        ]
        self.assertEqual( expected_list,
                self.wrap_plus.balance_characters_between_line_wraps(
                self.wrapper, input_text, "% ", "% " ) )

    def test_balance_characters_between_line_wraps_with_comment_indentation_balance(self):
        self.wrap_plus._width = 80
        input_text = \
        [
            "Inclui a IA para reconhecer o formatação nos módulos de beautifying.",
            "Ela eh uma heurística,",
            "que cada bloco implementa e faz ele gerar um arquivo de",
        ]
        expected_list = \
        [
            '% ',
            'Inclui a IA para reconhecer o formatação nos módulos de beautifying.',
            '% ',
            'Ela eh uma heurística,',
            '% ',
            'que cada bloco implementa e faz ele gerar um arquivo de',
        ]
        self.assertEqual( expected_list,
                self.wrap_plus.balance_characters_between_line_wraps(
                self.wrapper, input_text, "% ", "% " ) )

    def test_balance_characters_between_line_wraps_commented_line(self):
        indent = "%                                        "
        self.wrap_plus._width = 80
        input_text = "% tests dd açsdkjflçk çalskdj fçlakj lçkasjd fçlakjs dçflkjadd açsdkjflçk çalskdj fçlakj lçkasjd fçlakjs dçflkja"
        expected_list = \
        [
            '% ', '% tests dd açsdkjflçk çalskdj fçlakj lçkasjd fçlakjs dçflkjadd\n',
            '%                                        açsdkjflçk çalskdj fçlakj\n',
            '%                                        lçkasjd fçlakjs dçflkja',
        ]
        self.assertEqual( expected_list,
                self.wrap_plus.balance_characters_between_line_wraps(
                self.wrapper, [input_text], "% ", indent ) )

    def test_balance_characters_between_line_wraps_with_trailing_new_line(self):
        self.assertEqual( ['    ', 'This is my very long line which\n', '    will wrap near its end,\n'],
                self.wrap_plus.balance_characters_between_line_wraps(
                self.wrapper, ["This is my very long line which will wrap near its end,\n"], "    ", "    " ) )

    def test_balance_characters_between_line_wraps_without_trailing_new_line(self):
        self.assertEqual( ['    ', 'This is my very long line which\n', '    will wrap near its end,'],
                self.wrap_plus.balance_characters_between_line_wraps(
                self.wrapper, ["This is my very long line which will wrap near its end,"], "    ", "    " ) )

    def test_balance_characters_between_line_wraps_starting_with_comment(self):
        self.assertEqual( ['% ', 'you still only configuring a few\n', '% languages closely related. On this\n', '% case, C, C++, Java, Pawn, etc.'],
                self.wrap_plus.balance_characters_between_line_wraps( self.wrapper,
                [ "you still only configuring a few languages closely related. On this case, C, C++, Java, Pawn, etc." ], "% ", "% " ) )

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

    # is_comma_separated_list Unit Tests
    def test_is_command_separated_list_5_items(self):
        self.is_comma_separated_list( "1, 2, 3, 4, 5", 1, (True, 12, 5) )

    def test_is_command_separated_list_4_items(self):
        self.is_comma_separated_list( "1, 2_ 3, 4, 5", 1, (True, 12, 4) )

    def test_is_command_separated_list_3_items(self):
        self.is_comma_separated_list( "1_ 2, 3, 4_ 5", 4, (True, 12, 3) )

    def test_is_command_separated_list_2_items(self):
        self.is_comma_separated_list( "1_ 2, 3_ 4_ 5", 4, (True, 12, 2) )

    def test_is_command_separated_list_upperbound_with_1_by_5_trailing_items(self):
        self.is_comma_separated_list( "1, 2_ 3_ 4_ 5", 1, (False, 0, 0) )

    def test_is_command_separated_list_upperbound_with_4_middle_items(self):
        self.is_comma_separated_list( "1_ 2, 3_ 4_ 5 6, 7",  4, (False, 0, 0) )

    def test_is_command_separated_list_upperbound_with_2_by_5_trailing_items(self):
        self.is_comma_separated_list( "1_ 2, 3_ 4_ 5 6_ 7",  4, (False, 0, 0) )

    def test_is_command_separated_list_upperbound_2_by_4_trailing_items(self):
        self.is_comma_separated_list( "1_ 2, 3_ 4__5 6_ 7",  4, (False, 0, 0) )

    def test_is_command_separated_list_lowerbound_with_3_items(self):
        self.is_comma_separated_list( "1 2, 3 4_5 6, 7",  3, (True, 14, 3) )

    def test_is_command_separated_list_lowerbound_with_2_items(self):
        self.is_comma_separated_list( "1 2, 3_4_5 6, 7",  3, (True, 14, 3) )

    def test_is_command_separated_list_lowerbound_with_1_items(self):
        self.is_comma_separated_list( "1 2, 3_4_5_6, 7",  3, (True, 14, 3) )

    def test_is_command_separated_list_lowerbound_with_trailing_1_space(self):
        self.is_comma_separated_list( "1 2, 3_ 4_5_6 7 ",  3, (True, 15, 2) )

    def test_is_command_separated_list_lowerbound_with_trailing_2_space(self):
        self.is_comma_separated_list( "1 2, 3_ 4_5_6 7  ",  3, (True, 16, 2) )

    def is_comma_separated_list(self, text, index, goal):
        self.assertTrue( text[index] in wrap_plus_module.word_separator_characters )
        self.assertEqual( goal, self.wrap_plus.is_comma_separated_list( text, index ) )

    # semantic_line_wrap Unit Tests
    def test_semantic_line_wrap_simple_sentence(self):
        self.semantic_line_wrap( "1", "1" )

    def test_semantic_line_wrap_simple_sentence_with_single_comma(self):
        self.semantic_line_wrap( "which will take, you quite some time",
        "which will take,\nyou quite some time" )

    def test_semantic_line_wrap_simple_sentence_with_dual_comma(self):
        self.wrap_plus.maximum_items_in_comma_separated_list = 4
        self.semantic_line_wrap( "which will take, you, quite some time",
        "which will take, you, quite some time" )

    def test_semantic_line_wrap_simple_sentence_with_dual_comma_with_3_items_minimum(self):
        self.wrap_plus.maximum_items_in_comma_separated_list = 3
        self.semantic_line_wrap( "which will take, you, quite some time",
        "which will take,\nyou, quite some time" )

    def test_semantic_line_wrap_long_word(self):
        self.semantic_line_wrap( "quitesometimequitesometimequitesometimequitesometimequitesometimequitesometimequitesometime",
        "quitesometimequitesometimequitesometimequitesometimequitesometimequitesometimequitesometime" )

    def test_semantic_line_wrap_ending_with_comma_list(self):
        self.semantic_line_wrap( "you still only configuring a few languages closely related. On this case, C, C++, Java, Pawn, etc.",
        "you still only configuring a few languages closely related.\nOn this case,\nC, C++, Java, Pawn,\netc." )

    def test_semantic_line_wrap_ending_with_trailling_comma_on_list(self):
        self.semantic_line_wrap( "you still only configuring a few languages closely related. On this case, C, C++, Java, Pawn, etc,",
        "you still only configuring a few languages closely related.\nOn this case,\nC, C++, Java, Pawn, etc," )

    def test_semantic_line_wrap_with_comma_list_on_the_middle(self):
        self.semantic_line_wrap( "which will not more take, you quite oh the time, some time, more time, the time, per time",
        "which will not more take,\nyou quite oh the time,\nsome time, more time, the time, per time" )

    def test_semantic_line_wrap_with_comma_list_on_the_end(self):
        self.semantic_line_wrap( "few languages close related. On this case, C, C++, Java, Pawn, etc. more over break this line",
        "few languages close related.\nOn this case,\nC, C++, Java, Pawn,\netc.\nmore over break this line" )

    def test_semantic_line_wrap_with_numeric_comma_list_on_the_end(self):
        self.semantic_line_wrap( "1 2 3 4. 5 6 7, 1, 2, 3, 4, 5. 6 7 8 9 1",
        "1 2 3 4.\n5 6 7,\n1, 2, 3, 4,\n5.\n6 7 8 9 1" )

    def test_semantic_line_wrap_with_word_and_alpha_separator(self):
        self.semantic_line_wrap( ["E explicar como esta nova ferramenta difere das demais já existentes,",
                "e", "qual as vantagens de ter uma ferramenta."],
                "E explicar como esta nova ferramenta difere das demais já existentes,\n"
                "e qual as vantagens de ter uma ferramenta.",
            skip_list=True )

    def test_semantic_line_wrap_with_long_word_at_comma_list_end(self):
        self.semantic_line_wrap( "For all other languages you still need to find out another source code "
                "formatter tool, which will be certainly limited\\footnote{\\url{https://stackoverflow.com/"
                "questions/31438377/how-can-i-get-eclipse-to-wrap-lines-after-a-period-instead-of-before}}",

                "For all other languages you still need to find out another source code "
                "formatter\ntool,\nwhich will be certainly\nlimited\\footnote{\\url{https://stackoverflow.com/"
                "questions/31438377/how-can-i-get-eclipse-to-wrap-lines-after-a-period-instead-of-before}}" )

    def test_semantic_line_wrap_with_80_characters(self):
        self.semantic_line_wrap( [ "few languages close related. On this case, C, C++, Javas, Pawn, if, you, already, had, written, the, program, assure, everything, is, under, versioning, control, system, and, broke, everything, etc. more over break this line", "", "" ],
            "few languages close related.\nOn this case,\nC, C++, Javas, Pawn, if, you, already, had, written, the, program, assure,\neverything, is, under, versioning, control, system, and, broke, everything,\netc.\nmore over break this line" )

    def test_semantic_line_wrap_with_79_characters(self):
        self.semantic_line_wrap( [ "few languages close related. On this case, C, C++, Java, Pawn, if, you, already, had, written, the, program, assure, everything, is, under, versioning, control, system, and, broke, everything, etc. more over break this line", "", "" ],
            "few languages close related.\nOn this case,\nC, C++, Java, Pawn, if, you, already, had, written, the, program, assure,\neverything, is, under, versioning, control, system, and, broke, everything,\netc.\nmore over break this line" )

    def test_semantic_line_wrap_with_81_characters(self):
        self.semantic_line_wrap( [ "few languages close related. On this case, C, C++, Javas, Pawns, if, you, already, had, written, the, program, assure, everything, is, under, versioning, control, system, and, broke, everything, etc. more over break this line", "", "" ],
            "few languages close related.\nOn this case,\nC, C++, Javas, Pawns, if, you, already, had, written, the, program, assure,\neverything, is, under, versioning, control, system, and, broke, everything,\netc.\nmore over break this line" )

    def test_semantic_line_wrap_with_81_characters_on_list_flushing(self):
        self.semantic_line_wrap( [ "few languages close related. On this case, C, C++, Javas, Pawns, if, you, already, had, written, the, programs, assure, everything, is, under, versioning, control, system, and, broke, everything, etc. more over break this line", "", "" ],
            "few languages close related.\nOn this case,\nC, C++, Javas, Pawns, if, you, already, had, written, the, programs, assure,\neverything, is, under, versioning, control, system, and, broke, everything,\netc.\nmore over break this line" )

    def test_semantic_line_wrap_with_initial_indentation(self):
        self.semantic_line_wrap( [ "For all other languages you still need to find out another source code f tool, "
                "which will be certainly limited and still need to configure all over again.", "    ", "    " ],
                "    For all other languages you still need to find out another source code f\n"
                "    tool,\n"
                "    which will be certainly limited and still need to configure all over again." )

    def test_semantic_line_wrap_with_0_items_list(self):
        self.wrap_plus.maximum_items_in_comma_separated_list = 3
        self.semantic_line_wrap( [ "% as boas práticas de programação (code clean, GOF, DEITEL"
                "(forminhas das boas práticas)). E deixa claro qual é o problema", "", "% " ],
                "% as boas práticas de programação (code clean,\n"
                "% GOF,\n"
                "% DEITEL(forminhas das boas práticas)).\n"
                "% E deixa claro qual é o problema" )

    def test_semantic_line_wrap_with_3_items_list(self):
        self.wrap_plus.maximum_items_in_comma_separated_list = 4
        self.semantic_line_wrap( [ "% as boas práticas de programação (code clean, GOF, DEITEL"
                "(forminhas das boas práticas)). E deixa claro qual é o problema", "", "% " ],
                "% as boas práticas de programação (code clean, GOF,\n"
                "% DEITEL(forminhas das boas práticas)).\n"
                "% E deixa claro qual é o problema" )

    def semantic_line_wrap(self, initial_text, goal, **kwargs):
        """
        Call the wrap_plus.semantic_line_wrap() function correctly.

        `initial_text` is the text to apply the line wrapping
        `goal` is the expected result of this test

        Optionally, `initial_text` can be a list with 3 elements:
        [initial_text, initial_indent, subsequent_indent]
        """
        skip_list = kwargs.pop('skip_list', False)
        if isinstance( initial_text, list ) and not skip_list:
            self.assertEqual( goal, "".join( self.wrap_plus.semantic_line_wrap(
                    [initial_text[0]], initial_text[1], initial_text[2], **kwargs ) ) )

        else:
            self.assertEqual( goal, "".join( self.wrap_plus.semantic_line_wrap(
                    initial_text if skip_list else [initial_text], "", "", **kwargs ) ) )


def load_tests(loader, standard_tests, pattern):
    suite = unittest.TestSuite()
    suite.addTest( SemanticLineWrapUnitTests( 'test_semantic_line_wrap_with_word_and_alpha_separator' ) )
    return suite

# Comment this to run individual Unit Tests
load_tests = None

