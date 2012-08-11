# Use Cases
# =========
#
# Notes
# -----
# - A blank line is a line with only zero or more whitespace.
# - Tabs probably need special handling.  Currently just expand them to spaces.
# - Cursor should move below post-wrapped text in such a way that you can
#   repeatedly press the wrap key and keep moving forward.
#
# One Paragraph
# -------------
# A single normal standalone paragraph, separated by blank lines.
#
# Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Nulla consequat massa quis enim
# ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Nulla consequat massa quis enim.
# ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Nulla consequat massa quis enim.
#
# Single point: Anywhere in text should wrap the whole thing as one paragraph, no indent.
# Selection: Only wrap lines selected (still one paragraph).
#
# Two Paragraphs
# --------------
# Multiple paragraphs, separated by blank lines.
#
# Paragraph one consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium quis, se.
#
#
# Paragraph two consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium quis, se.
#
# Single point: Anywhere in one paragraph, wrap that paragraph only, no indent, preserve blank lines.
# Selection: Only wrap lines in the selection.  If there is a blank line in the selection, this indicates a separation between paragraphs.  Multiple blank lines should be preserved.
#
# Indented Paragraphs1
# --------------------
#
#     Paragraph one consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium quis, se.
#     Paragraph one consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium quis, se.
#
# Single point: Preserve indent, wrap as before.
# Selection: Only wrap selected lines, preserve indent.
#
# Indented Paragraphs2
# --------------------
# First line is indented, subsequent lines are not.
#
#     Paragraph one consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium quis, se.
# Paragraph one continued consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium quis, se.
#
#     Paragraph two consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium quis, se.
# Paragraph one continued consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium quis, se.
#
# Single point: Preserve indent on first line, subsequent lines have whatever indentation level is on the second line.
# Selection: Same logic, wherever the selection starts, pretend that's the line the paragraph starts.
#
# Indented Paragraphs3
# --------------------
# First line is not indented, subsequent lines are.
#
#     Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus.
#         Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus.
#     Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus.
#
#     Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus.
#         Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus.
#             Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus.
#
# First line should keep whatever indentation it has.  Subsequent lines should match whatever indentation the second line has.
#
# Line Separators
# ---------------
# Line separators behave like blank lines.  They stop paragraph discovery.  They should be preserved if selected.
# A separator is a line with only punctuation.
#     !@#$%^&*=+`~'\":;.,?_-
#
#     ...........................
#     Paragraph one consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis
#     ...........................
#     Paragraph one consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis
#     Paragraph one consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis
#
# Single point: In paragraph, do not go above or below separators, don't modify them.
# Selection (text only): Wrap only selected lines.
# Selection (includes separator): Treat separator like a blank line (separates paragraphs), preserve it without modification.
#
# Lists
# -----
# Various types of lists.  Bullets:
#     * Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus.
#     ** Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus.
#     + Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus.
#     Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus.
#     - Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus.
#     # Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus.
#     # Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et
#       magnis dis parturient montes, nascetur ridiculus mus.
#     ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et.
#
# Bullet must be followed by a space.
# Bullets may be multiple characters.
# Beware bullets which appear like comment characters.
#
# Numbers:
# Must end with a dot or paren:
#
# 1. foo foo foo foo foo foo foo foo foo foo foo foo foo foo foo foo foo foo foo foo foo foo foo foo foo foo foo foo foo foo foo
# 1.2. bar bar bar bar bar bar bar bar bar bar bar bar bar bar bar bar bar bar bar bar bar bar bar bar bar bar bar bar bar bar bar
# 1) Blah
# 1.2) bar bar bar bar bar bar bar bar bar bar bar bar bar bar bar bar bar bar bar bar bar bar bar bar bar bar bar bar bar bar bar
# 1.3.4) bar bar bar bar bar bar bar bar bar bar bar bar bar bar bar bar bar bar bar bar bar bar bar bar bar bar bar bar bar bar bar
#
# Letters:
# Must end with dot or paren.
# a. foo foo foo foo foo foo foo foo foo foo foo foo foo foo foo foo foo foo foo foo foo foo foo foo foo foo foo foo foo foo foo
# bar bar bar bar bar bar bar bar bar bar bar bar bar bar bar bar bar bar bar bar bar bar bar bar bar bar bar bar bar bar
# a) foo foo foo foo foo foo foo foo foo foo foo foo foo foo foo foo foo foo foo foo foo foo foo foo foo foo foo foo foo foo foo
# A. baz baz baz baz baz baz baz baz baz baz baz baz baz baz baz baz baz baz baz baz baz baz baz baz baz baz baz baz baz baz baz
# I. foo foo foo foo foo foo foo foo foo foo foo foo foo foo foo foo foo foo foo foo foo foo foo foo foo foo foo foo foo foo foo
#
# Single point on line where list starts: Maintain indent of bullet on first
# line. Paragraph discovery does not go up.  Discovery stops when it sees a new
# bullet start.  Subsequent lines lign up with the start of the text on the
# first line.
#
# Single point on line within bullet entry: Same as before, except discovery
# goes up until the entry start.
#
# Selection: Only wrap lines in selection.  Bullet starts within selection are
# treated like new paragraphs with same rules.
#
# ReST field name
# ---------------
# ":" field name ":"
#
#     :foo: Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus.
#     Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus.
#     :bar: Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus.
#           Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus.
#
# Similar to bullet lists, except alignment of subsequent lines follow whatever
# is there.  If not indented relative to the field name, add an indent.
#
# ReST Directives
# ---------------
# .. data:: sample
#     Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus.
# .. data:: sample2
#     Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus.
#
#         I'm indented, preserve me.  Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus.
#
# Preserve directive line (don't touch).  All lines indented at whatever the
# first line was indented at, plus any additional indent found at the start of a
# paragraph.
#
# Python Triple Strings
# ---------------------
# """Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Nulla consequat massa quis enim. Donec pede justo, fringilla vel, aliquet nec, vulputate eget, arcu. In enim justo, rhoncus ut, imperdiet a, venenatis vitae, justo. Nullam dictum felis eu pede mollis pretium."""
#
#
# def foo():
#     """Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et
#     magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis,
#     ultricies nec, pellentesque eu, pretium quis, sem. Nulla consequat massa quis enim. Donec pede justo, fringilla vel, aliquet nec, vulputate eget,
#     arcu. In enim justo, rhoncus ut, imperdiet a, venenatis vitae, justo. Nullam dictum felis eu pede mollis pretium.
#     """
#     sample code here.
#
#     """Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus."""
#     situation where triple quote not.
#
#
# Treat the triple quote at the beginning as the start of a paragraph (similar
# to bullets).  Don't go beyond the triple quote.  It's OK if this only works
# when Python syntax is selected.  (Possibly make this work for all languages.)
#
# GT Quoted
# ---------
# Quoted with the greater-than symbol.
#
#     >> This is a blockquote with two paragraphs. Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aliquam hendrerit mi posuere lectus. Vestibulum enim wisi, viverra nec, fringilla in, laoreet vitae, risus.
#     >>
#     >> Donec sit amet nisl. Aliquam semper ipsum sit amet velit. Suspendisse id sem consectetuer libero luctus adipiscing.
#     > This is a blockquote with two paragraphs. Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aliquam hendrerit mi posuere lectus. Vestibulum enim wisi, viverra nec, fringilla in, laoreet vitae, risus.
#     >
#     > Donec sit amet nisl. Aliquam semper ipsum sit amet velit. Suspendisse id sem consectetuer libero luctus adipiscing.
#
#     Intermixed line without quote. Aliquam semper ipsum sit amet velit. Suspendisse id sem consectetuer libero luctus adipiscing.Aliquam semper ipsum sit amet velit. Suspendisse id sem consectetuer libero luctus adipiscing.
#
#     > > Donec sit amet nisl. Aliquam semper ipsum sit amet velit. Suspendisse id sem consectetuer libero luctus adipiscing.
#     > > Donec sit amet nisl. Aliquam semper ipsum sit amet velit. Suspendisse id sem consectetuer libero luctus adipiscing.
#     > This is a blockquote with one paragraph. Lorem ipsum dolor sit amet,
#     consectetuer adipiscing elit. Aliquam hendrerit mi posuere lectus.
#     Vestibulum enim wisi, viverra nec, fringilla in, laoreet vitae, risus.
#
#     > Donec sit amet nisl. Aliquam semper ipsum sit amet velit. Suspendisse
#     id sem consectetuer libero luctus adipiscing.
#
# Single point: Should ignore gt symbol.  Wrap as normal, but remove the gt
# symbol first, and then readd it with the correct indentation.
#
# Selection: Only wrap selected lines.  Ignore gt symbol.  Use gt symbol indent
# found on first line of each paragraph.
#
# This behaves just like comments.
#
# Changes in the number of carets (with possible intermixed spaces) should be
# treated like a paragraph boundary.
#
# LaTeX Math
# ----------
# The quadratic form $\mN$ for the integration of the squared norm of an $m$-dimensional linear function on any simplex $\Omega$ of dimension $n$ can therefore be written as
# \begin{align}
# \label{eq:integration_matrix}
# \mN &= \Factorial{n} \, \vol{\Omega} \, \Transpose{\mP} \inp{\mH^0_n \otimes \IdentityMatrix_m} \, \mP \nonumber\\%
#     &= \Factorial{n} \, \vol{\Omega} \, \mN^0~.
# \end{align}
# The discrete $L^2$-product of piecewise-linear functions on a simplical complexes is obtained by assembling the quadratic forms $\mN$ of each simplex into an operator $\mM$ on the whole complex.
#
# Don't touch lines that start with a backslash.
#
# Comments
# --------
# Comments are somewhat complicated.
#
# When wrapping inside a comment, the comment characters should be invisible,
# and all rules above should work correctly.  The comment characters should be
# removed before wrapping and added with the correct indentation after wrapping.
#
# These only apply to their respective syntax modes.
#
#     Shouldn't touch this line.
#     /* C comment style1
#      * I put stars
#      * at the beginning
#      * of each line
#      */
#     /* C comment style2
#     just writing stuff. */
#     Shouldn't touch this line.
#     /*
#     C comment style3
#     just writing stuff. */
#     /*
#     C comment style4
#     just writing stuff.
#     */
#     Shouldn't touch this line.
#
#     don't touch
#     /* C comment style5 Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec
#
#     Quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Nulla consequat massa quis enim. Donec pede justo, fringilla vel, aliquet nec, vulputate eget, arcu. In enim justo, rhoncus ut, imperdiet a, venenatis vitae, justo. Nullam dictum felis eu pede mollis pretium.
#     */
#     don't touch
#
#     // Single line comment. Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes,
#     // nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Nulla consequat massa quis enim. Donec pede justo, fringilla vel, aliquet nec, vulputate eget, arcu. In enim justo, rhoncus ut, imperdiet a, venenatis vitae, justo. Nullam dictum felis eu pede mollis pretium.
#
#     Don't touch this line.
#     # Pound comment. Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus.
#     # Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Nulla consequat massa quis enim. Donec pede justo, fringilla vel, aliquet nec, vulputate eget, arcu. In enim justo, rhoncus ut, imperdiet a, venenatis vitae, justo.
#     # Nullam dictum felis eu pede mollis pretium.
#     #
#     # Next paragraph quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Nulla consequat massa quis enim. Donec pede justo, fringilla vel, aliquet nec, vulputate eget, arcu. In enim justo, rhoncus ut, imperdiet a, venenatis vitae, justo.
#     Don't touch this line.
#
# Selections that span both comment and non-comment lines should treat them as
# paragraph boundaries, although this is a silly use case, and probably is OK if
# it doesn't work.
#

"""
Use Cases
=========

Notes
-----
- A blank line is a line with only zero or more whitespace.
- Tabs probably need special handling.  Currently just expand them to spaces.
- Cursor should move below post-wrapped text in such a way that you can
  repeatedly press the wrap key and keep moving forward.

One Paragraph
-------------
A single normal standalone paragraph, separated by blank lines.

Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Nulla consequat massa quis enim
ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Nulla consequat massa quis enim.
ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Nulla consequat massa quis enim.

Single point: Anywhere in text should wrap the whole thing as one paragraph, no indent.
Selection: Only wrap lines selected (still one paragraph).

Two Paragraphs
--------------
Multiple paragraphs, separated by blank lines.

Paragraph one consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium quis, se.


Paragraph two consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium quis, se.

Single point: Anywhere in one paragraph, wrap that paragraph only, no indent, preserve blank lines.
Selection: Only wrap lines in the selection.  If there is a blank line in the selection, this indicates a separation between paragraphs.  Multiple blank lines should be preserved.

Indented Paragraphs1
--------------------

    Paragraph one consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium quis, se.
    Paragraph one consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium quis, se.

Single point: Preserve indent, wrap as before.
Selection: Only wrap selected lines, preserve indent.

Indented Paragraphs2
--------------------
First line is indented, subsequent lines are not.

    Paragraph one consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium quis, se.
Paragraph one continued consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium quis, se.

    Paragraph two consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium quis, se.
Paragraph one continued consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium quis, se.

Single point: Preserve indent on first line, subsequent lines have whatever indentation level is on the second line.
Selection: Same logic, wherever the selection starts, pretend that's the line the paragraph starts.

Indented Paragraphs3
--------------------
First line is not indented, subsequent lines are.

    Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus.
        Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus.
    Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus.

    Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus.
        Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus.
            Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus.

First line should keep whatever indentation it has.  Subsequent lines should match whatever indentation the second line has.

Line Separators
---------------
Line separators behave like blank lines.  They stop paragraph discovery.  They should be preserved if selected.
A separator is a line with only punctuation.
    !@#$%^&*=+`~'\":;.,?_-

    ...........................
    Paragraph one consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis
    ...........................
    Paragraph one consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis
    Paragraph one consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis

Single point: In paragraph, do not go above or below separators, don't modify them.
Selection (text only): Wrap only selected lines.
Selection (includes separator): Treat separator like a blank line (separates paragraphs), preserve it without modification.

Lists
-----
Various types of lists.  Bullets:
    * Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus.
    ** Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus.
    + Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus.
    Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus.
    - Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus.
    # Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus.
    # Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et
      magnis dis parturient montes, nascetur ridiculus mus.
    ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et.

Bullet must be followed by a space.
Bullets may be multiple characters.
Beware bullets which appear like comment characters.

Numbers:
Must end with a dot or paren:

1. foo foo foo foo foo foo foo foo foo foo foo foo foo foo foo foo foo foo foo foo foo foo foo foo foo foo foo foo foo foo foo
1.2. bar bar bar bar bar bar bar bar bar bar bar bar bar bar bar bar bar bar bar bar bar bar bar bar bar bar bar bar bar bar bar
1) Blah
1.2) bar bar bar bar bar bar bar bar bar bar bar bar bar bar bar bar bar bar bar bar bar bar bar bar bar bar bar bar bar bar bar
1.3.4) bar bar bar bar bar bar bar bar bar bar bar bar bar bar bar bar bar bar bar bar bar bar bar bar bar bar bar bar bar bar bar

Letters:
Must end with dot or paren.
a. foo foo foo foo foo foo foo foo foo foo foo foo foo foo foo foo foo foo foo foo foo foo foo foo foo foo foo foo foo foo foo
bar bar bar bar bar bar bar bar bar bar bar bar bar bar bar bar bar bar bar bar bar bar bar bar bar bar bar bar bar bar
a) foo foo foo foo foo foo foo foo foo foo foo foo foo foo foo foo foo foo foo foo foo foo foo foo foo foo foo foo foo foo foo
A. baz baz baz baz baz baz baz baz baz baz baz baz baz baz baz baz baz baz baz baz baz baz baz baz baz baz baz baz baz baz baz
I. foo foo foo foo foo foo foo foo foo foo foo foo foo foo foo foo foo foo foo foo foo foo foo foo foo foo foo foo foo foo foo

Single point on line where list starts: Maintain indent of bullet on first
line. Paragraph discovery does not go up.  Discovery stops when it sees a new
bullet start.  Subsequent lines lign up with the start of the text on the
first line.

Single point on line within bullet entry: Same as before, except discovery
goes up until the entry start.

Selection: Only wrap lines in selection.  Bullet starts within selection are
treated like new paragraphs with same rules.

ReST field name
---------------
":" field name ":"

    :foo: Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus.
    Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus.
    :bar: Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus.
          Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus.

Similar to bullet lists, except alignment of subsequent lines follow whatever
is there.  If not indented relative to the field name, add an indent.

ReST Directives
---------------
.. data:: sample
    Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus.
.. data:: sample2
    Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus.

        I'm indented, preserve me.  Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus.

Preserve directive line (don't touch).  All lines indented at whatever the
first line was indented at, plus any additional indent found at the start of a
paragraph.

GT Quoted
---------
Quoted with the greater-than symbol.

    >> This is a blockquote with two paragraphs. Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aliquam hendrerit mi posuere lectus. Vestibulum enim wisi, viverra nec, fringilla in, laoreet vitae, risus.
    >>
    >> Donec sit amet nisl. Aliquam semper ipsum sit amet velit. Suspendisse id sem consectetuer libero luctus adipiscing.
    > This is a blockquote with two paragraphs. Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aliquam hendrerit mi posuere lectus. Vestibulum enim wisi, viverra nec, fringilla in, laoreet vitae, risus.
    >
    > Donec sit amet nisl. Aliquam semper ipsum sit amet velit. Suspendisse id sem consectetuer libero luctus adipiscing.

    Intermixed line without quote. Aliquam semper ipsum sit amet velit. Suspendisse id sem consectetuer libero luctus adipiscing.Aliquam semper ipsum sit amet velit. Suspendisse id sem consectetuer libero luctus adipiscing.

    > > Donec sit amet nisl. Aliquam semper ipsum sit amet velit. Suspendisse id sem consectetuer libero luctus adipiscing.
    > > Donec sit amet nisl. Aliquam semper ipsum sit amet velit. Suspendisse id sem consectetuer libero luctus adipiscing.
    > This is a blockquote with one paragraph. Lorem ipsum dolor sit amet,
    consectetuer adipiscing elit. Aliquam hendrerit mi posuere lectus.
    Vestibulum enim wisi, viverra nec, fringilla in, laoreet vitae, risus.

    > Donec sit amet nisl. Aliquam semper ipsum sit amet velit. Suspendisse
    id sem consectetuer libero luctus adipiscing.

Single point: Should ignore gt symbol.  Wrap as normal, but remove the gt
symbol first, and then readd it with the correct indentation.

Selection: Only wrap selected lines.  Ignore gt symbol.  Use gt symbol indent
found on first line of each paragraph.

This behaves just like comments.

Changes in the number of carets (with possible intermixed spaces) should be
treated like a paragraph boundary.

LaTeX Math
----------
The quadratic form $\mN$ for the integration of the squared norm of an $m$-dimensional linear function on any simplex $\Omega$ of dimension $n$ can therefore be written as
\begin{align}
\label{eq:integration_matrix}
\mN &= \Factorial{n} \, \vol{\Omega} \, \Transpose{\mP} \inp{\mH^0_n \otimes \IdentityMatrix_m} \, \mP \nonumber\\%
    &= \Factorial{n} \, \vol{\Omega} \, \mN^0~.
\end{align}
The discrete $L^2$-product of piecewise-linear functions on a simplical complexes is obtained by assembling the quadratic forms $\mN$ of each simplex into an operator $\mM$ on the whole complex.

Don't touch lines that start with a backslash.

Comments
--------
Comments are somewhat complicated.

When wrapping inside a comment, the comment characters should be invisible,
and all rules above should work correctly.  The comment characters should be
removed before wrapping and added with the correct indentation after wrapping.

These only apply to their respective syntax modes.

    Shouldn't touch this line.
    /* C comment style1
     * I put stars
     * at the beginning
     * of each line
     */
    /* C comment style2
    just writing stuff. */
    Shouldn't touch this line.
    /*
    C comment style3
    just writing stuff. */
    /*
    C comment style4
    just writing stuff.
    */
    Shouldn't touch this line.

    don't touch
    /* C comment style5 Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec

    Quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Nulla consequat massa quis enim. Donec pede justo, fringilla vel, aliquet nec, vulputate eget, arcu. In enim justo, rhoncus ut, imperdiet a, venenatis vitae, justo. Nullam dictum felis eu pede mollis pretium.
    */
    don't touch

    // Single line comment. Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes,
    // nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Nulla consequat massa quis enim. Donec pede justo, fringilla vel, aliquet nec, vulputate eget, arcu. In enim justo, rhoncus ut, imperdiet a, venenatis vitae, justo. Nullam dictum felis eu pede mollis pretium.

    Don't touch this line.
    # Pound comment. Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus.
    # Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Nulla consequat massa quis enim. Donec pede justo, fringilla vel, aliquet nec, vulputate eget, arcu. In enim justo, rhoncus ut, imperdiet a, venenatis vitae, justo.
    # Nullam dictum felis eu pede mollis pretium.
    #
    # Next paragraph quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Nulla consequat massa quis enim. Donec pede justo, fringilla vel, aliquet nec, vulputate eget, arcu. In enim justo, rhoncus ut, imperdiet a, venenatis vitae, justo.
    Don't touch this line.

Selections that span both comment and non-comment lines should treat them as
paragraph boundaries, although this is a silly use case, and probably is OK if
it doesn't work.

"""


# Python Triple Strings
# ---------------------
"""Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Nulla consequat massa quis enim. Donec pede justo, fringilla vel, aliquet nec, vulputate eget, arcu. In enim justo, rhoncus ut, imperdiet a, venenatis vitae, justo. Nullam dictum felis eu pede mollis pretium."""


def foo():
    """Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et
    magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis,
    ultricies nec, pellentesque eu, pretium quis, sem. Nulla consequat massa quis enim. Donec pede justo, fringilla vel, aliquet nec, vulputate eget,
    arcu. In enim justo, rhoncus ut, imperdiet a, venenatis vitae, justo. Nullam dictum felis eu pede mollis pretium.

    :param foo: Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Nulla consequat massa quis enim.
    """
    sample code here.

    """Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus."""
    situation where triple quote not.

''' fdafdfs ''''
Treat the triple quote at the beginning as the start of a paragraph (similar
to bullets).  Don't go beyond the triple quote.  It's OK if this only works
when Python syntax is selected.  (Possibly make this work for all languages.)
