from __future__ import print_function
import sublime, sublime_plugin
import textwrap
import re
import time
import unittest
try:
    import Default.comment as comment
except ImportError:
    import comment


def is_quoted_string(scope_r, scope_name):
    # string.quoted.double.block.python
    # string.quoted.single.block.python
    # string.quoted.double.single-line.python
    # string.quoted.single.single-line.python
    # comment.block.documentation.python
    return 'quoted' in scope_name or 'comment.block.documentation' in scope_name

debug_enabled = False
# debug_enabled = True

time_start = 0
last_time = 0
def debug_start(enabled):
    global time_start, last_time
    if debug_enabled or enabled:
        time_start = time.time()
        last_time = time_start

def debug(msg, *args):
    if debug_enabled:
        global last_time
        t = time.time()
        d = t-time_start
        print('%.3f (+%.3f) ' % (d, t-last_time), end='')
        last_time = t
        print(msg % args)

def debug_end():
    if debug_enabled:
        print('Total time: %.3f' % (time.time()-time_start))

class PrefixStrippingView(object):
    """View that strips out prefix characters, like comments.

    :ivar str required_comment_prefix: When inside a line comment, we want to
        restrict wrapping to just the comment section, and also retain the
        comment characters and any initial indentation.  This string is the
        set of prefix characters a line must have to be a candidate for
        wrapping in that case (otherwise it is typically the empty string).

    :ivar Pattern required_comment_pattern: Regular expression required for
        matching.  The pattern is already included from the first line in
        `required_comment_prefix`.  This pattern is set to check if subsequent
        lines have longer matches (in which case `line` will stop reading).
    """
    required_comment_prefix = ''
    required_comment_pattern = None

    def __init__(self, view, min, max):
        self.view = view
        self.min = min
        self.max = max

    def _is_c_comment(self, scope_name):
        if not 'comment' in scope_name and not 'block' in scope_name:
            return False
        for start, end, disable_indent in self.bc:
            if start == '/*' and end == '*/':
                break
        else:
            return False
        return True

    def set_comments(self, lc, bc, pt):
        self.lc = lc
        self.bc = bc
        # If the line at pt is a comment line, set required_comment_prefix to
        # the comment prefix.
        self.required_comment_prefix = ''
        # Grab the line.
        line_r = self.view.line(pt)
        line = self.view.substr(line_r)
        line_strp = line.strip()
        if not line_strp:
            # Empty line, nothing to do.
            debug('Empty line, no comment characters found.')
            return

        # Determine if pt is inside a "line comment".
        # Only whitespace is allowed to the left of the line comment.
        # XXX: What is disable_indent?
        for start, disable_indent in lc:
            start = start.rstrip()
            if line_strp.startswith(start):
                ldiff = len(line) - len(line.lstrip())
                p = line[:ldiff+len(start)]
                if self.required_comment_prefix is None or \
                   len(self.required_comment_prefix) < len(p):
                    self.required_comment_prefix = p

        # TODO: re.escape required_comment_prefix.

        # Handle email-style quoting.
        email_quote_pattern = re.compile('^' + self.required_comment_prefix + email_quote)
        m = email_quote_pattern.match(line)
        if m:
            self.required_comment_prefix = m.group()
            self.required_comment_pattern = email_quote_pattern
            debug('doing email style quoting')

        scope_r = self.view.extract_scope(pt)
        scope_name = self.view.scope_name(pt)
        debug('scope=%r range=%r', scope_name, scope_r)

        if self._is_c_comment(scope_name):
            # Check for C-style commenting with each line starting with an asterisk.
            first_star_prefix = None
            lines = self.view.lines(scope_r)
            for line_r in lines[1:-1]:
                line = self.view.substr(line_r)
                m = funny_c_comment_pattern.match(line)
                if m != None:
                    if first_star_prefix == None:
                        first_star_prefix = m.group()
                else:
                    first_star_prefix = None
                    break
            if first_star_prefix:
                self.required_comment_prefix = first_star_prefix
            # Narrow the scope to just the comment contents.
            scope_text = self.view.substr(scope_r)
            m = re.match(r'^([ \t\n]*/\*).*(\*/[ \t\n]*)$', scope_text, re.DOTALL)
            if m:
                begin = scope_r.begin() + len(m.group(1))
                end = scope_r.end() - len(m.group(2))
                self.min = max(self.min, begin)
                self.max = min(self.max, end)
            debug('Scope narrowed to %i:%i', self.min, self.max)

        debug('required_comment_prefix determined to be %r', self.required_comment_prefix,)

        # Narrow the min/max range if inside a "quoted" string.
        if is_quoted_string(scope_r, scope_name):
            # Narrow the range.
            self.min = max(self.min, self.view.line(scope_r.begin()).begin())
            self.max = min(self.max, self.view.line(scope_r.end()).end())

    def line(self, where):
        """Get a line for a point.

        :returns: A (region, str) tuple.  str has the comment prefix stripped.
        """
        line_r = self.view.line(where)
        if line_r.begin() < self.min:
            debug('line min increased')
            line_r = sublime.Region(self.min, line_r.end())
        if line_r.end() > self.max:
            debug('line max lowered')
            line_r = sublime.Region(line_r.begin(), self.max)
        line = self.view.substr(line_r)
        debug('line=%r', line)
        if self.required_comment_prefix:
            debug('checking required comment prefix %r', self.required_comment_prefix)

            if line.startswith(self.required_comment_prefix):
                # Check for an insufficient prefix.
                if self.required_comment_pattern:
                    m = self.required_comment_pattern.match(line)
                    if m:
                        if m.group() != self.required_comment_prefix:
                            # This might happen, if for example with an email
                            # comment, we go from one comment level to a
                            # deeper one (the regex matched more > characters
                            # than are in required_comment_pattern).
                            return None, None
                    else:
                        # This should never happen (matches the string but not
                        # the regex?).
                        return None, None
                l = len(self.required_comment_prefix)
                line = line[l:]
                # XXX: Should this also update line_r?
            else:
                return None, None
        return line_r, line

    def substr(self, r):
        return self.view.substr(r)

    def next_line(self, where):
        l_r = self.view.line(where)
        debug('next line region=%r', l_r)
        pt = l_r.end()+1
        if pt >= self.max:
            debug('past max at %r', self.max)
            return None, None
        return self.line(pt)

    def prev_line(self, where):
        l_r = self.view.line(where)
        pt = l_r.begin()-1
        if pt <= self.min:
            return None, None
        return self.line(pt)

def OR(*args):
    return '(?:' + '|'.join(args) + ')'
def CONCAT(*args):
    return '(?:' + ''.join(args) + ')'

blank_line_pattern = re.compile(r'(?:^[\t \{\}\n]*)$|(?:.*"""\\?)')
max_words_in_comma_separated_list = 4

list_of_words_pattern = re.compile(r'(?:^|\s)+[^ ]+', re.MULTILINE)
next_word_pattern = re.compile(r'\s+[^ ]+', re.MULTILINE)

whitespace_character = (" ", "\t")
word_separator_characters = ( ",", ".", "?", "!", ":", ";" )

# This doesn't always work, but seems decent.
numbered_list = r'(?:(?:[0-9#]+[.)])+[\t ])'
lettered_list = r'(?:[\w][.)][\t ])'
bullet_list = r'(?:[*+#-]+[\t ])'
list_pattern = re.compile(r'^[ \t]*' + OR(numbered_list, lettered_list, bullet_list) + r'[ \t]*')
latex_hack = r'(?:\\)(?!,|;|&|%|text|emph|cite|\w?(page)?ref|url|footnote|(La)*TeX)'
rest_directive = r'(?:\.\.)'
field_start = r'(?:[:@])'  # rest, javadoc, jsdoc, etc.

new_paragraph_pattern_string = r'^[\t ]*' + OR(numbered_list, lettered_list, bullet_list, field_start, r'\{')
# print( "pattern: " + new_paragraph_pattern_string )

new_paragraph_pattern = re.compile(new_paragraph_pattern_string)
space_prefix_pattern = re.compile(r'^[ \t]*')

# XXX: Does not handle escaped colons in field name.
fields = OR(r':[^:]+:', '@[a-zA-Z]+ ')
field_pattern = re.compile(r'^([ \t]*)'+fields)  # rest, javadoc, jsdoc, etc

sep_chars = '!@#$%^&*=+`~\'\":;.,?_-'
sep_line = '[' + sep_chars + r']+[ \t'+sep_chars+']*'

# Break pattern is a little ambiguous.  Something like "# Header" could also be a list element.
break_pattern = re.compile(r'^[\t ]*' + OR(sep_line, OR(latex_hack, rest_directive) + '.*') + '$')
pure_break_pattern = re.compile(r'^[\t ]*' + sep_line + '$')

email_quote = r'[\t ]*>[> \t]*'
funny_c_comment_pattern = re.compile(r'^[\t ]*\*')

class WrapLinesPlusCommand(sublime_plugin.TextCommand):

    def _my_full_line(self, region):
        # Special case scenario where you select an entire line.  The normal
        # "full_line" function will extend it to contain the next line
        # (because the cursor is actually at the beginning of the next line).
        # I would prefer it didn't do that.
        if self.view.substr(region.end()-1) == '\n':
            return self.view.full_line(sublime.Region(region.begin(), region.end()-1))
        else:
            return self.view.full_line(region)

    def _is_paragraph_start(self, line_r, line):
        # Certain patterns at the beginning of the line indicate this is the
        # beginning of a paragraph.

        # print( "line: " + str( line ) )
        # print( "new_paragraph_pattern.match(line): " + str( new_paragraph_pattern.match(line) ) )
        return new_paragraph_pattern.match(line) != None

    def _is_paragraph_break(self, line_r, line, pure=False):
        """A paragraph "break" is something like a blank line, or a horizontal line,
        or anything that  should not be wrapped and treated like a blank line
        (i.e. ignored).
        """
        if self._is_blank_line(line): return True
        scope_name = self.view.scope_name(line_r.begin())
        debug('scope_name=%r (%r)', scope_name, line_r)
        if 'heading' in scope_name:
            return True
        if pure:
            return pure_break_pattern.match(line) != None
        else:
            return break_pattern.match(line) != None

    def _is_blank_line(self, line):
        return blank_line_pattern.match(line) != None

    def _find_paragraph_start(self, pt):
        """Start at pt and move up to find where the paragraph starts.

        :returns: The (line, line_region) of the start of the paragraph.
        """
        view = self._strip_view
        current_line_r, current_line = view.line(pt)
        started_in_comment = self._started_in_comment(pt)

        debug('is_paragraph_break?')
        if self._is_paragraph_break(current_line_r, current_line):
            return current_line_r, current_line
        debug('no')

        while 1:
            # Check if this line is the start of a paragraph.
            debug('start?')
            if self._is_paragraph_start(current_line_r, current_line):
                debug('current_line is paragraph start: %r', current_line,)
                break
            # Check if the previous line is a "break" separator.
            debug('break?')
            prev_line_r, prev_line = view.prev_line(current_line_r)
            if prev_line_r == None:
                # current_line is as far up as we're allowed to go.
                break
            if self._is_paragraph_break(prev_line_r, prev_line):
                debug('prev line %r is a paragraph break', prev_line,)
                break
            # If the previous line has a comment, and we started in a
            # non-comment scope, stop.  No need to check for comment to
            # non-comment change because the prefix restrictions should handle
            # that.
            if (not started_in_comment and
                self.view.score_selector(prev_line_r.end(), 'comment')
               ):
                debug('prev line contains a comment, cannot continue.')
                break
            debug('prev_line %r is part of the paragraph', prev_line,)
            # Previous line is a part of this paragraph.  Add it, and loop
            # around again.
            current_line_r = prev_line_r
            current_line = prev_line
        return current_line_r, current_line

    def _find_paragraphs(self, sr):
        """Find and return a list of paragraphs as regions.

        :param Region sr: The region where to look for paragraphs.  If it is
            an empty region, "discover" where the paragraph starts and ends.
            Otherwise, the region defines the max and min (with potentially
            several paragraphs contained within).

        :returns: A list of (region, lines, comment_prefix) of each paragraph.
        """
        result = []
        debug('find paragraphs sr=%r', sr,)
        if sr.empty():
            is_empty = True
            view_min = 0
            view_max = self.view.size()
        else:
            is_empty = False
            full_sr = self._my_full_line(sr)
            view_min = full_sr.begin()
            view_max = full_sr.end()
        started_in_comment = self._started_in_comment(sr.begin())
        self._strip_view = PrefixStrippingView(self.view, view_min, view_max)
        view = self._strip_view
        # Loop for each paragraph (only loops once if sr is empty).
        paragraph_start_pt = sr.begin()
        while 1:
            debug('paragraph scanning start %r.', paragraph_start_pt,)
            view.set_comments(self._lc, self._bc, paragraph_start_pt)
            lines = []
            if is_empty:
                # Find the beginning of this paragraph.
                debug('empty sel finding paragraph start.')
                current_line_r, current_line = self._find_paragraph_start(paragraph_start_pt)
                debug('empty sel paragraph start determined to be %r %r', current_line_r, current_line)
            else:
                # The selection defines the beginning.
                current_line_r, current_line = view.line(paragraph_start_pt)
                debug('sel beggining = %r %r', current_line_r, current_line)

            # Skip blank and unambiguous break lines.
            while 1:
                debug('skip blank line')
                if not self._is_paragraph_break(current_line_r, current_line, pure=True):
                    debug('not paragraph break')
                    break
                if is_empty:
                    debug('empty sel on paragraph break %r', current_line,)
                    return []
                current_line_r, current_line = view.next_line(current_line_r)

            paragraph_start_pt = current_line_r.begin()
            paragraph_end_pt = current_line_r.end()
            # current_line_r now points to the beginning of the paragraph.
            # Move down until the end of the paragraph.
            debug('Scan until end of paragraph.')
            while 1:
                debug('current_line_r=%r max=%r', current_line_r, view.max)
                # If we started in a non-comment scope, and the end of the
                # line contains a comment, include any non-comment text in the
                # wrap and stop looking for more.
                if (not started_in_comment and
                    self.view.score_selector(current_line_r.end(), 'comment')
                   ):
                    debug('end of paragraph hit a comment.')
                    # Find the start of the comment.
                    # This assumes comments do not have multiple scopes.
                    comment_r = self.view.extract_scope(current_line_r.end())
                    # Just in case something is wonky with the scope.
                    end_pt = max(comment_r.begin(), current_line_r.begin())
                    # A substring of current_line.
                    subline_r = sublime.Region(current_line_r.begin(), end_pt)
                    subline = self.view.substr(subline_r)
                    # Do not include whitespace preceding the comment.
                    m = re.search('([ \t]+$)', subline)
                    if m:
                        end_pt -= len(m.group(1))
                    debug('non-comment contents are: %r', subline)
                    paragraph_end_pt = end_pt
                    lines.append(subline)
                    # Skip over the comment.
                    current_line_r, current_line = view.next_line(current_line_r)
                    break

                lines.append(current_line)
                paragraph_end_pt = current_line_r.end()

                current_line_r, current_line = view.next_line(current_line_r)
                if current_line_r == None:
                    # Line is outside of our range.
                    debug('Out of range, stopping.')
                    break
                debug('current_line = %r %r', current_line_r, current_line)
                if self._is_paragraph_break(current_line_r, current_line):
                    debug('current line is a break, stopping.')
                    break
                if self._is_paragraph_start(current_line_r, current_line):
                    debug('current line is a paragraph start, stopping.')
                    break


            paragraph_region = sublime.Region(paragraph_start_pt, paragraph_end_pt)
            result.append((paragraph_region, lines, view.required_comment_prefix))

            if is_empty:
                break

            # Skip over blank lines and break lines till the next paragraph
            # (or end of range).
            debug('skip over blank lines')
            while current_line_r != None:
                if self._is_paragraph_start(current_line_r, current_line):
                    break
                if not self._is_paragraph_break(current_line_r, current_line):
                    break
                # It's a paragraph break, skip over it.
                current_line_r, current_line = view.next_line(current_line_r)

            if current_line_r == None:
                break

            debug('next_paragraph_start is %r %r', current_line_r, current_line)
            paragraph_start_pt = current_line_r.begin()
            if paragraph_start_pt >= view_max:
                break

        return result

    def _determine_width(self, width):
        """Determine the maximum line width.

        :param Int width: The width specified by the command.  Normally 0
            which means "figure it out".

        :returns: The maximum line width.
        """
        # print( "_determine_width, width: " + str( width ) )
        if width == 0 and self.view.settings().get('wrap_width'):
            try:
                width = int(self.view.settings().get('wrap_width'))
            except TypeError:
                pass

        # print( "_determine_width, before get('rulers'), width: " + str( width ) )
        if width == 0 and self.view.settings().get('rulers'):
            # try and guess the wrap width from the ruler, if any
            try:
                width = int(self.view.settings().get('rulers')[0])
            except ValueError:
                pass
            except TypeError:
                pass

        # print( "_determine_width, before get('WrapPlus.wrap_width', width): " + str( width ) )
        if width == 0:
            width = self.view.settings().get('WrapPlus.wrap_width', width)

        # Value of 0 means 'automatic'.
        if width == 0:
            width = 78

        ile = self.view.settings().get('WrapPlus.include_line_endings', 'auto')
        if ile == True:
            width -= self._determine_line_ending_size()
        elif ile == 'auto':
            if self._auto_word_wrap_enabled() and self.view.settings().get('wrap_width', 0) != 0:
                width -= self._determine_line_ending_size()

        return width

    def _determine_line_ending_size(self):
        # Sublime always uses 1, regardless of the file type/OS.
        return 1
        etypes = {
            'windows': 2,
            'unix': 1,
            'cr': 1,
        }
        return etypes.get(self.view.line_endings().lower(), 1)

    def _auto_word_wrap_enabled(self):
        ww = self.view.settings().get('word_wrap')
        return (ww == True or
                (ww == 'auto' and self.view.score_selector(0, 'text')))

    def _determine_tab_size(self):
        tab_width = 8
        if self.view.settings().get('tab_size'):
            try:
                tab_width = int(self.view.settings().get('tab_size'))
            except TypeError:
                pass

        if tab_width == 0:
            tab_width = 8
        self._tab_width = tab_width

    def _determine_comment_style(self):
        # I'm not exactly sure why this function needs a point.  It seems to
        # return the same value regardless of location for the stuff I've
        # tried.
        (self._lc, self._bc) = comment.build_comment_data(self.view, 0)

    def _started_in_comment(self, point):
        if self.view.score_selector(point, 'comment'):
            return True
        # Check for case where only whitespace is before a comment.
        line_r = self.view.line(point)
        if self.view.score_selector(line_r.end(), 'comment'):
            line = self.view.substr(line_r)
            m = re.search('(^[ \t]+)', line)
            if m:
                pt_past_space = line_r.begin() + len(m.group(1))
                if self.view.score_selector(pt_past_space, 'comment'):
                    return True
        return False

    def _width_in_spaces(self, text):
        tab_count = text.count('\t')
        return tab_count*self._tab_width + len(text)-tab_count

    def _make_indent(self):
        # This is suboptimal.
        return ' '*4
        # if self.view.settings().get('translate_tabs_to_spaces'):
        #     return ' ' * self._tab_width
        # else:
        #     return '\t'

    def _extract_prefix(self, paragraph_region, lines, required_comment_prefix):
        # The comment prefix has already been stripped from the lines.
        # If the first line starts with a list-like thing, then that will be the initial prefix.
        initial_prefix = ''
        subsequent_prefix = ''
        first_line = lines[0]
        m = list_pattern.match(first_line)
        if m:
            initial_prefix = first_line[0:m.end()]
            stripped_prefix = initial_prefix.lstrip()
            leading_whitespace = initial_prefix[:len(initial_prefix)-len(stripped_prefix)]
            subsequent_prefix = leading_whitespace+' '*self._width_in_spaces(stripped_prefix)
        else:
            m = field_pattern.match(first_line)
            if m:
                # The spaces in front of the field start.
                initial_prefix = m.group(1)
                if len(lines) > 1:
                    # How to handle subsequent lines.
                    m = space_prefix_pattern.match(lines[1])
                    if m:
                        # It's already indented, keep this indent level
                        # (unless it is less than where the field started).
                        spaces = m.group(0)
                        if self._width_in_spaces(spaces) >= self._width_in_spaces(initial_prefix)+1:
                            subsequent_prefix = spaces
                if not subsequent_prefix:
                    # Not already indented, make an indent.
                    subsequent_prefix = initial_prefix + self._make_indent()
            else:
                m = space_prefix_pattern.match(first_line)
                if m:
                    initial_prefix = first_line[0:m.end()]
                    if len(lines) > 1:
                        m = space_prefix_pattern.match(lines[1])
                        if m:
                            subsequent_prefix = lines[1][0:m.end()]
                        else:
                            subsequent_prefix = ''
                    else:
                        subsequent_prefix = initial_prefix
                else:
                    # Should never happen.
                    initial_prefix = ''
                    subsequent_prefix = ''

        pt = paragraph_region.begin()
        scope_r = self.view.extract_scope(pt)
        scope_name = self.view.scope_name(pt)
        if len(lines)==1 and is_quoted_string(scope_r, scope_name):
            # A multi-line quoted string, that is currently only on one line.
            # This is mainly for Python docstrings.  Not sure if it's a
            # problem in other cases.
            true_first_line_r = self.view.line(pt)
            true_first_line = self.view.substr(true_first_line_r)
            if true_first_line_r.begin() <= scope_r.begin():
                m = space_prefix_pattern.match(true_first_line)
                debug('single line quoted string triggered')
                if m:
                    subsequent_prefix = m.group() + subsequent_prefix

        # Remove the prefixes that are there.
        new_lines = []
        new_lines.append(first_line[len(initial_prefix):].strip())
        for line in lines[1:]:
            if line.startswith(subsequent_prefix):
                line = line[len(subsequent_prefix):]
            new_lines.append(line.strip())

        debug('initial_prefix=%r subsequent_prefix=%r', initial_prefix, subsequent_prefix)

        return (required_comment_prefix+initial_prefix,
                required_comment_prefix+subsequent_prefix,
                new_lines)

    def run(self, edit, width=0):
        debug_start(self.view.settings().get('WrapPlus.debug', False))
        debug('\n\n#########################################################################')
        self._width = self._determine_width(width)

        # print('wrap width = %r', self._width)
        self._determine_tab_size()
        self._determine_comment_style()

        # paragraphs is a list of (region, lines, comment_prefix) tuples.
        paragraphs = []
        for s in self.view.sel():
            debug('examine %r', s)
            paragraphs.extend(self._find_paragraphs(s))

        view_settings = self.view.settings()
        debug('paragraphs is %r', paragraphs)

        break_long_words = view_settings.get('WrapPlus.break_long_words', True)
        break_on_hyphens = view_settings.get('WrapPlus.break_on_hyphens', True)

        minimum_line_size_percent              = view_settings.get('WrapPlus.minimum_line_size_percent', 0.2)
        disable_line_wrapping_by_maximum_width = view_settings.get('WrapPlus.disable_line_wrapping_by_maximum_width', False)

        # print( "minimum_line_size_percent: " + str( minimum_line_size_percent ) )
        if view_settings.get('WrapPlus.semantic_line_wrap', False):

            def line_wrapper_type():
                return self.semantic_line_wrap(paragraph_lines, init_prefix, subsequent_prefix,
                        minimum_line_size_percent, disable_line_wrapping_by_maximum_width)

        else:

            def line_wrapper_type():
                return self.classic_wrap_text(wrapper, paragraph_lines, init_prefix, subsequent_prefix)

        wrapper = textwrap.TextWrapper(break_long_words=break_long_words,
                                       break_on_hyphens=break_on_hyphens)
        wrapper.width = self._width
        wrapper.expand_tabs = False

        # print( "self._width: " + str( self._width ) )

        if paragraphs:
            # Use view selections to handle shifts from the replace() command.
            self.view.sel().clear()
            for region, lines, comment_prefix in paragraphs:
                self.view.sel().add(region)

            # Regions fetched from view.sel() will shift appropriately with
            # the calls to replace().
            for index, selection in enumerate(self.view.sel()):
                paragraph_region, paragraph_lines, required_comment_prefix = paragraphs[index]
                init_prefix, subsequent_prefix, paragraph_lines = self._extract_prefix(paragraph_region, paragraph_lines, required_comment_prefix)

                text = line_wrapper_type()

                # I can't decide if I prefer it to not make the modification
                # if there is no change (and thus don't mark an unmodified
                # file as modified), or if it's better to include a "non-
                # change" in the undo stack.
                self.view.replace(edit, selection, text)
                self.print_text_replacements(text, selection)

        self.move_cursor_below_the_last_paragraph()

    def semantic_line_wrap(self, paragraph_lines, init_prefix, subsequent_prefix,
                minimum_line_size_percent=0.0, disable_line_wrapping_by_maximum_width=False):
        new_text = [init_prefix]
        init_prefix_length = len( init_prefix )

        is_allowed_to_wrap           = False
        is_possible_space            = False
        is_flushing_comma_list       = False
        is_comma_separated_list      = False
        is_flushing_accumalated_line = False

        text        = ' '.join(paragraph_lines)
        text_length = len(text)

        minimum_line_size = int( self._width * minimum_line_size_percent )
        # print( "minimum_line_size: %s" % ( minimum_line_size ) )

        accumulated_line     = ""
        line_start_index     = 0
        comma_list_end_point = 0

        for index, character in enumerate(text):
            accumulated_line_length = len( accumulated_line )
            next_word_length        = self.peek_next_word_length( index, text )

            if is_possible_space and character in whitespace_character:
                continue

            else:
                is_possible_space = False

            # Skip the next characters as we already know they are a list. This is only called when
            # the `comma_list_end_point` is lower than the `self._width`, otherwise the line will
            # be immediately flushed
            if comma_list_end_point > 0:
                comma_list_end_point -= 1

                # print( "semantic_line_wrap, is_flushing, index: %d, accumulated_line_length: %d, comma_list_size: %d, line_remaining_size: %s, comma_list_end_point: %d, character: %s" % ( index, accumulated_line_length, index - line_start_index, self._width - index - line_start_index, comma_list_end_point, character ) )

                if not is_flushing_accumalated_line:

                    if not disable_line_wrapping_by_maximum_width \
                            and accumulated_line_length + next_word_length + init_prefix_length > self._width:

                        # print( "semantic_line_wrap, Flushing accumulated_line... next_word_length: %d" % ( next_word_length ) )
                        is_flushing_accumalated_line = True

                        # Current character is a whitespace, but it must the the next, so fix the index
                        index -= 1

                    else:
                        accumulated_line += character

                        is_flushing_comma_list = True
                        continue

            else:
                is_flushing_comma_list  = False
                is_comma_separated_list = False

            # print( "semantic_line_wrap, character: %s " % ( character ) )
            if not disable_line_wrapping_by_maximum_width \
                    and not is_flushing_accumalated_line \
                    and accumulated_line_length + next_word_length + init_prefix_length > self._width:

                # print( "semantic_line_wrap, Flushing accumulated_line... next_word_length: %d" % ( next_word_length ) )
                is_flushing_accumalated_line = True

                # Current character is a whitespace, but it must the the next, so fix the index
                index -= 1

            if accumulated_line_length > minimum_line_size:
                is_allowed_to_wrap = True

            if character in word_separator_characters and is_allowed_to_wrap \
                    or is_flushing_accumalated_line:

                if index + 2 < text_length:
                    is_followed_by_space = text[index+1] in whitespace_character

                    if is_followed_by_space:

                        if character in word_separator_characters \
                                and not is_flushing_comma_list:

                            is_comma_separated_list, comma_list_end_point = self.is_comma_separated_list(text, index, line_start_index)
                            comma_list_end_point -= index - line_start_index + 3

                        if ( comma_list_end_point > 0 \
                                and not is_flushing_comma_list ) \
                                or not is_comma_separated_list \
                                or is_flushing_accumalated_line:

                            # It is not the first line anymore, now we need to care about the `subsequent_prefix` length
                            init_prefix_length = len( subsequent_prefix )

                            if character in whitespace_character:
                                character = ""

                            new_text.append( accumulated_line + character + "\n" + subsequent_prefix )
                            accumulated_line = ""
                            line_start_index = index + 1

                            is_possible_space            = True
                            is_allowed_to_wrap           = False
                            is_flushing_accumalated_line = False

                    else:
                        accumulated_line += character

                else:
                    accumulated_line += character

            else:
                accumulated_line += character

        if len( accumulated_line ):
            new_text.append(accumulated_line)

        # print( "semantic_line_wrap, new_text: " + str( new_text ) )
        return "".join(new_text)

    def peek_next_word_length(self, index, text):
        match = next_word_pattern.match( text, index )

        if match:
            next_word = match.group(0)

            # print( "peek_next_word_length: %s" % next_word )
            return len( next_word )

        return 0

    def is_comma_separated_list(self, text, index, line_start_index=0):
        # print( "is_comma_separated_list, index: %3d, line_start_index: %d" % ( index, line_start_index ) )

        next_character    = " "
        text_length       = len( text ) - 1
        slice_start_index = index

        while index < text_length:
            index     = index + 1
            character = text[index]

            if index + 1 < text_length:
                next_character = text[index+1]

            # print( "is_comma_separated_list, character: %s, next_character: %s" % ( character, next_character ) )
            if ( character in word_separator_characters \
                    and next_character in whitespace_character ) \
                    or index >= text_length:

                comma_section = text[ slice_start_index+1:index+1 ]
                # print( "is_comma_separated_list, text:    " + comma_section )

                results       = list_of_words_pattern.findall( comma_section )
                results_count = len( results )
                # print( "is_comma_separated_list, results: " + str( results ) )

                if 0 < results_count < max_words_in_comma_separated_list:

                    # Get the last match object
                    for match in list_of_words_pattern.finditer( comma_section ):
                        pass

                    match_end          = match.end(0)
                    possible_match_end = 0

                    # `line_start_index` always greater than `index`, like 50 - 20 = 30
                    # 50, 20 = 30, 80 - 30 = 50, 50 - 10 = 40
                    # print( "is_comma_separated_list, line_remaining_size: " + str( self._width - ( index - line_start_index ) - match_end ) )
                    # print( "is_comma_separated_list, match_end:           " + str( match_end ) )

                    is_there_new_commas, possible_match_end = self.is_comma_separated_list( text, index, line_start_index + match_end )
                    # print( "is_comma_separated_list, possible_match_end:  " + str( possible_match_end ) )

                    if possible_match_end > 0:
                        return True, possible_match_end + match_end

                    # print( "is_comma_separated_list, slice_start_index - line_start_index + match_end: " + str( slice_start_index - line_start_index + match_end ) )
                    return True, slice_start_index - line_start_index + match_end

                else:
                    return False, 0

        return False, 0

    def classic_wrap_text(self, wrapper, paragraph_lines, init_prefix, subsequent_prefix):
        orig_init_prefix = init_prefix
        orig_subsequent_prefix = subsequent_prefix

        if orig_init_prefix or orig_subsequent_prefix:
            # Textwrap is somewhat limited.  It doesn't recognize tabs
            # in prefixes.  Unfortunately, this means we can't easily
            # differentiate between the initial and subsequent.  This
            # is a workaround.
            init_prefix = orig_init_prefix.expandtabs(self._tab_width)
            subsequent_prefix = orig_subsequent_prefix.expandtabs(self._tab_width)
            wrapper.initial_indent = init_prefix
            wrapper.subsequent_indent = subsequent_prefix

        text = '\n'.join(paragraph_lines)
        text = text.expandtabs(self._tab_width)
        text = wrapper.fill(text)

        # Put the tabs back to the prefixes.
        if orig_init_prefix or orig_subsequent_prefix:

            if init_prefix != orig_subsequent_prefix or subsequent_prefix != orig_subsequent_prefix:
                lines = text.splitlines()

                if init_prefix != orig_init_prefix:
                    debug('fix tabs %r', lines[0])
                    lines[0] = orig_init_prefix + lines[0][len(init_prefix):]
                    debug('new line is %r', lines[0])

                if subsequent_prefix != orig_subsequent_prefix:

                    for index, line in enumerate(lines[1:]):
                        lines[index+1] = orig_subsequent_prefix + lines[index+1][len(subsequent_prefix):]

                text = '\n'.join(lines)

        return text

    def move_cursor_below_the_last_paragraph(self):
        selection = self.view.sel()
        end = selection[len(selection)-1].end()
        line = self.view.line(end)
        end = min(self.view.size(), line.end()+1)
        self.view.sel().clear()
        region = sublime.Region(end)
        self.view.sel().add(region)
        self.view.show(region)
        debug_end()

    def print_text_replacements(self, text, selection):
        replaced_txt = self.view.substr(selection)

        if replaced_txt != text:
            debug('replaced text not the same:\noriginal=%r\nnew=%r', replaced_txt, text)
        else:
            debug('replaced text is the same')


def plugin_loaded():
    pass
    # print( "\n\n" )
    # main()

    # wrap_plus = WrapLinesPlusCommand( None )
    # wrap_plus._width = 80
    # wrap_plus.semantic_line_wrap( [ "you still only configuring a few languages closely related. On this case, C, C++, Java, Pawn, etc." ], "", "" )
    # wrap_plus.semantic_line_wrap( [ "quitesometimequitesometimequitesometimequitesometimequitesometimequitesometimequitesometime" ], "", "" )
    # wrap_plus.semantic_line_wrap( [ "which will not more take, you quite oh the time, some time, more time, the time, per time" ], "", "" )
    # wrap_plus.semantic_line_wrap( [ "few languages closely related. On this case, C, C++, Java, Pawn, etc. more over break this line" ], "", "" )
    # wrap_plus.semantic_line_wrap( [ "few languages close related. On this case, C, C++, Javas, Pawn, if, you, already, had, written, the, program, assure, everything, is, under, versioning, control, system, and, broke, everything, etc. more over break this line" ], "", "" )
    # wrap_plus.semantic_line_wrap( [ "For all other languages you still need to find out another source code formatter tool, which will be certainly limited\\footnote{\\url{https://stackoverflow.com/questions/31438377/how-can-i-get-eclipse-to-wrap-lines-after-a-period-instead-of-before}}" ], "", "" )
    # wrap_plus.semantic_line_wrap( [ "For all other languages you still need to find out another source code f tool, which" ], "    ", "    " )


def main():
    runner = unittest.TextTestRunner()
    runner.run( suite() )


def suite():
    """
        Problem with sys.argv[1] when unittest module is in a script
        https://stackoverflow.com/questions/2812218/problem-with-sys-argv1-when-unittest-module-is-in-a-script

        Is there a way to loop through and execute all of the functions in a Python class?
        https://stackoverflow.com/questions/2597827/is-there-a-way-to-loop-through-and-execute-all-of-the-functions

        looping over all member variables of a class in python
        https://stackoverflow.com/questions/1398022/looping-over-all-member-variables-of-a-class-in-python
    """
    suite   = unittest.TestSuite()
    classes = [ WrapPlusUnitTests ]

    for _class in classes:
        _object = _class()

        for methode_name in dir( _object ):

            if methode_name.lower().startswith( "test" ):
                suite.addTest( WrapPlusUnitTests( methode_name ) )

    return suite


class WrapPlusUnitTests(unittest.TestCase):

    @classmethod
    def setUp(self):
        self.maxDiff = None
        self.wrap_plus = WrapLinesPlusCommand( None )
        self.wrap_plus._width = 80

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
        self.assertTrue( text[index] in word_separator_characters )
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
            self.assertEqual( goal, self.wrap_plus.semantic_line_wrap( [initial_text[0]], initial_text[1], initial_text[2] ) )

        else:
            self.assertEqual( goal, self.wrap_plus.semantic_line_wrap( [initial_text], "", "" ) )


