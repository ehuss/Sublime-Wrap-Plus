

import sys

import textwrap
import unittest


wrap_plus_module = sys.modules["Wrap Plus.wrap_plus"]


def run_manual_tests():
    wrap_plus        = wrap_plus_module.WrapLinesPlusCommand( None )
    wrap_plus._width = 80

    # wrap_plus.semantic_line_wrap( [ "you still only configuring a few languages closely related. On this case, C, C++, Java, Pawn, etc." ], "", "", balance_characters_between_line_wraps=True )
    # wrap_plus.semantic_line_wrap( [ "you still only configuring a few languages closely related. On this case, C, C++, Java, Pawn, etc." ], "", "" )
    # wrap_plus.semantic_line_wrap( [ "quitesometimequitesometimequitesometimequitesometimequitesometimequitesometimequitesometime" ], "", "" )
    # wrap_plus.semantic_line_wrap( [ "which will not more take, you quite oh the time, some time, more time, the time, per time" ], "", "" )
    # wrap_plus.semantic_line_wrap( [ "few languages closely related. On this case, C, C++, Java, Pawn, etc. more over break this line" ], "", "" )
    # wrap_plus.semantic_line_wrap( [ "few languages close related. On this case, C, C++, Javas, Pawn, if, you, already, had, written, the, program, assure, everything, is, under, versioning, control, system, and, broke, everything, etc. more over break this line" ], "", "" )
    # wrap_plus.semantic_line_wrap( [ "For all other languages you still need to find out another source code formatter tool, which will be certainly limited\\footnote{\\url{https://stackoverflow.com/questions/31438377/how-can-i-get-eclipse-to-wrap-lines-after-a-period-instead-of-before}}" ], "", "" )
    # wrap_plus.semantic_line_wrap( [ "For all other languages you still need to find out another source code f tool, which" ], "    ", "    " )

    wrapper   = textwrap.TextWrapper(break_long_words=False, break_on_hyphens=False)
    wrap_plus = wrap_plus_module.WrapLinesPlusCommand( None )
    wrap_plus._width          = 50
    wrapper.expand_tabs       = False
    wrapper.subsequent_indent = "    "

    # wrap_plus._split_lines( wrapper, [ "This is my very long line which my very long line which my_very_long_line_which_will_wrap_near_its_end," ], 50 )
    # wrap_plus._split_lines( wrapper, [ "This is my very long line which will wrap near its end,\n" ], 50 )

    # wrap_plus.balance_characters_between_line_wraps( wrapper, [ "This is my very long line which will wrap near its end,\n" ], "    ", "    " )
    # wrap_plus.balance_characters_between_line_wraps( wrapper, [ "This is my very long line which will wrap near its end,", "This is my very long line which will wrap near its end," ], "    ", "    " )
    # wrap_plus.balance_characters_between_line_wraps( wrapper, [ "% you still only configuring a few languages closely related. On this case, C, C++, Java, Pawn, etc." ], "% ", "% " )
    wrap_plus.balance_characters_between_line_wraps( wrapper, [ "% you still only configuring a few languages closely related.", "On this case, C, C++, Java, Pawn, etc." ], "% ", "%                             " )

    wrap_plus._width = 80
    # wrap_plus._split_lines( wrapper, [  "In this proposal last chapter which lies on the part called `\\nameref{sec:software_implementation}'," ], 80 )
    # wrap_plus.balance_characters_between_line_wraps( wrapper, [  "In this proposal last chapter which lies on the part called `\\nameref{sec:software_implementation}'," ], "    ", "    " )


