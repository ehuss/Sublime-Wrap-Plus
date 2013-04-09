from __future__ import print_function
import sublime, sublime_plugin
import textwrap
import re
import time
try:
    import Default.comment as comment
except ImportError:
    import comment

def is_quoted_string(scope_r, scope_name):
    return 'quoted' in scope_name

debug_enabled = False
time_start = 0
last_time = 0
def debug_start():
    if debug_enabled:
        global time_start, last_time
        time_start = time.time()
        last_time = time_start

def debug(msg, *args):
    if debug_enabled:
        global last_time
        t = time.time()
        d = t-time_start
        print('%.3f (+%.3f)' % (d, t-last_time), end='')
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
        # XXX: What is disable_indent?
        for start, disable_indent in lc:
            start = start.rstrip()
            if line_strp.startswith(start):
                ldiff = len(line) - len(line.lstrip())
                p = line[:ldiff+len(start)]
                self.required_comment_prefix = p
                break

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
            if (self.view.substr(sublime.Region(scope_r.begin(), scope_r.begin()+2)) == '/*' and
                self.view.substr(sublime.Region(scope_r.end()-2, scope_r.end())) == '*/'
               ):
                self.min = max(self.min, scope_r.begin()+2)
                self.max = min(self.max, scope_r.end()-2)
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
        debug('line=%r' % line)
        if self.required_comment_prefix:
            debug('checking required comment prefix %r' % self.required_comment_prefix)
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
            else:
                return None, None
        return line_r, line

    def substr(self, r):
        return self.view.substr(r)

    def next_line(self, where):
        l_r = self.view.line(where)
        debug('next line region=%r' % l_r)
        pt = l_r.end()+1
        if pt >= self.max:
            debug('past max at %r' % self.max)
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

blank_line_pattern = re.compile("^[\\t \\n]*$")

# This doesn't always work, but seems decent.
numbered_list = '(?:(?:[0-9#]+[.)])+[\\t ])'
lettered_list = '(?:[\w][.)][\\t ])'
bullet_list = '(?:[*+#-]+[\\t ])'
list_pattern = re.compile('^[ \\t]*' + OR(numbered_list, lettered_list, bullet_list) + '[ \\t]*')
latex_hack = '(:?\\\\)'
rest_directive = '(:?\\.\\.)'
field_start = '(?:[:@])'  # rest, javadoc, jsdoc, etc.
new_paragraph_pattern = re.compile('^[\\t ]*' +
    OR(numbered_list, lettered_list, bullet_list,
              field_start))
space_prefix_pattern = re.compile('^[ \\t]*')
# XXX: Does not handle escaped colons in field name.
fields = OR(':[^:]+:', '@[a-zA-Z]+ ')
field_pattern = re.compile('^([ \\t]*)'+fields)  # rest, javadoc, jsdoc, etc

sep_chars = '!@#$%^&*=+`~\'\":;.,?_-'
sep_line = '[' + sep_chars + ']+[ \\t'+sep_chars+']*'

# Break pattern is a little ambiguous.  Something like "# Header" could also be a list element.
break_pattern = re.compile('^[\\t ]*' + OR(sep_line, OR(latex_hack, rest_directive) + '.*') + '$')
pure_break_pattern = re.compile('^[\\t ]*' + sep_line + '$')

email_quote = '[\\t ]*>[> \\t]*'
funny_c_comment_pattern = re.compile('^[\\t ]*\*(?: |$)')

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
            min = 0
            max = self.view.size()
        else:
            is_empty = False
            full_sr = self._my_full_line(sr)
            min = full_sr.begin()
            max = full_sr.end()
        self._strip_view = PrefixStrippingView(self.view, min, max)
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

            lines.append(current_line)
            paragraph_start_pt = current_line_r.begin()
            paragraph_end_pt = current_line_r.end()
            # current_line_r now points to the beginning of the paragraph.
            # Move down until the end of the paragraph.
            debug('Scan until end of paragraph.')
            while 1:
                debug('current_line_r=%r max=%r', current_line_r, view.max)
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
                lines.append(current_line)
                paragraph_end_pt = current_line_r.end()

            paragraph_r = sublime.Region(paragraph_start_pt, paragraph_end_pt)
            result.append((paragraph_r, lines, view.required_comment_prefix))

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
            if paragraph_start_pt >= max:
                break

        return result

    def _determine_width(self, width):
        if width == 0 and self.view.settings().get("wrap_width"):
            try:
                width = int(self.view.settings().get("wrap_width"))
            except TypeError:
                pass

        if width == 0 and self.view.settings().get("rulers"):
            # try and guess the wrap width from the ruler, if any
            try:
                width = int(self.view.settings().get("rulers")[0])
            except ValueError:
                pass
            except TypeError:
                pass

        # Value of 0 means "automatic".
        if width == 0:
            width = 78
        else:
            width -= self.view.settings().get("WrapPlus.wrap_col_diff", 0)
        debug('width is %i', width)

        self._width = width

    def _determine_tab_size(self):
        tab_width = 8
        if self.view.settings().get("tab_size"):
            try:
                tab_width = int(self.view.settings().get("tab_size"))
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

    def _extract_prefix(self, paragraph_r, lines, required_comment_prefix):
        # The comment prefix has already been stripped from the lines.
        # If the first line starts with a list-like thing, then that will be the initial prefix.
        initial_prefix = ''
        subsequent_prefix = ''
        first_line = lines[0]
        m = list_pattern.match(first_line)
        if m:
            initial_prefix = first_line[0:m.end()]
            subsequent_prefix = ' '*self._width_in_spaces(initial_prefix)
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

        pt = paragraph_r.begin()
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
        debug_start()
        debug('#########################################################################')
        self._determine_width(width)
        debug('determined width to be %r' % self._width)
        self._determine_tab_size()
        self._determine_comment_style()

        # paragraphs is a list of (region, lines, comment_prefix) tuples.
        paragraphs = []
        for s in self.view.sel():
            debug('examine %r' % s)
            paragraphs.extend(self._find_paragraphs(s))

        if paragraphs:
            # Use view selections to handle shifts from the replace() command.
            self.view.sel().clear()
            for r, l, p in paragraphs:
                self.view.sel().add(r)

            # Regions fetched from view.sel() will shift appropriately with
            # the calls to replace().
            for i, s in enumerate(self.view.sel()):
                paragraph_r, paragraph_lines, required_comment_prefix = paragraphs[i]
                break_long_words = self.view.settings().get('WrapPlus.break_long_words', True)
                break_on_hyphens = self.view.settings().get('WrapPlus.break_on_hyphens', True)
                wrapper = textwrap.TextWrapper(break_long_words=break_long_words,
                                               break_on_hyphens=break_on_hyphens)
                wrapper.width = self._width
                init_prefix, subsequent_prefix, paragraph_lines = self._extract_prefix(paragraph_r, paragraph_lines, required_comment_prefix)
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

                wrapper.expand_tabs = False

                txt = '\n'.join(paragraph_lines)
                txt = txt.expandtabs(self._tab_width)
                txt = wrapper.fill(txt)

                # Put the tabs back to the prefixes.
                if orig_init_prefix or orig_subsequent_prefix:
                    if init_prefix != orig_subsequent_prefix or subsequent_prefix != orig_subsequent_prefix:
                        lines = txt.splitlines()
                        if init_prefix != orig_init_prefix:
                            debug('fix tabs %r' % lines[0])
                            lines[0] = orig_init_prefix + lines[0][len(init_prefix):]
                            debug('new line is %r' % lines[0])
                        if subsequent_prefix != orig_subsequent_prefix:
                            for i, line in enumerate(lines[1:]):
                                lines[i+1] = orig_subsequent_prefix + lines[i+1][len(subsequent_prefix):]
                        txt = '\n'.join(lines)

                replaced_txt = self.view.substr(s)
                # I can't decide if I prefer it to not make the modification
                # if there is no change (and thus don't mark an unmodified
                # file as modified), or if it's better to include a "non-
                # change" in the undo stack.
                self.view.replace(edit, s, txt)
                if replaced_txt != txt:
                    debug('replaced text not the same:\noriginal=%r\nnew=%r', replaced_txt, txt)
                else:
                    debug('replaced text is the same')

        # Move cursor below the last paragraph.
        s = self.view.sel()
        end = s[len(s)-1].end()
        line = self.view.line(end)
        end = min(self.view.size(), line.end()+1)
        self.view.sel().clear()
        r = sublime.Region(end)
        self.view.sel().add(r)
        self.view.show(r)
        debug_end()

