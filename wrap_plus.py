import sublime, sublime_plugin
import string
import textwrap
import re
import comment

# Ideas for improvements:
# - Handle > quoted text better.
#   Would like to treat it like single-line comment (as detected from the comment module).
# - Would be nice if it knew it was in a multi-line python string.
# - Wrap on a blank line should advance to the next line.
# - Handle HTML.
# - Hard tab handling is a little funky.  Particularly with subsequent_indent.

def previous_line(view, sr):
    """sr should be a Region covering the entire hard line"""
    if sr.begin() == 0:
        return None
    else:
        return view.full_line(sr.begin() - 1)

def next_line(view, sr):
    """sr should be a Region covering the entire hard line, including
    the newline"""
    if sr.end() == view.size():
        return None
    else:
        return view.full_line(sr.end())

def OR(*args):
    return '(?:' + '|'.join(args) + ')'
def CONCAT(*args):
    return '(?:' + ''.join(args) + ')'

blank_line_pattern = re.compile("^[\\t ]*\\n?$")
sep_line_pattern = re.compile("^[\\t \\n!@#$%^&*=+`~'\":;.,?_-]*$")
# This doesn't always work, but seems decent.
numbered_list = '(?:(?:[0-9#]+[.)]?)+[\\t ])'
lettered_list = '(?:[\w][.)][\\t ])'
bullet_list = '(?:[*+-]+[\\t ])'
header1 = '(:?[=#]+)'
header2 = '(:?\\\\)'
rest_directive = '(:?\\.\\.)'
rest_field_name = '(?::)'
# Hack for python triple quote for now.
python_triple_quote = '(:?(:?""")|(:?\'\'\'))'
new_paragraph_pattern = re.compile('^[\\t ]*' +
    CONCAT(OR(numbered_list, lettered_list, bullet_list, header1, header2,
              rest_directive, python_triple_quote, rest_field_name), '.*') +
    '$')
standalone_pattern = re.compile('^[\\t ]*' + OR(header1, header2, rest_directive, python_triple_quote) + '.*$')

def is_blank_line(line):
    """Determines if the given line is a "blank" line."""
    return blank_line_pattern.match(line) != None or sep_line_pattern.match(line) != None

def is_new_paragraph(line, required_prefix=''):
    """Determines if the given line is the beginning of a new paragraph."""
    if required_prefix and line.startswith(required_prefix):
        # Trim out the required prefix.
        line = line[len(required_prefix):]
    return new_paragraph_pattern.match(line) != None

def is_standalone(line, required_prefix=''):
    """Determines if the given line should be on its own (like a header)."""
    if required_prefix and line.startswith(required_prefix):
        # Trim out the required prefix.
        line = line[len(required_prefix):]
    return standalone_pattern.match(line) != None

def has_prefix(view, line, prefix):
    if not prefix:
        return True

    line_start = view.substr(sublime.Region(line.begin(),
        line.begin() + len(prefix)))

    return line_start == prefix

def determine_required_prefix(view, line_begin):
    required_prefix = None
    (line_comments, block_comments) = comment.build_comment_data(view, line_begin)
    #print 'line_comments=%r block_comments=%r' % (line_comments, block_comments)
    dataStart = comment.advance_to_first_non_white_space_on_line(view, line_begin)
    for c in line_comments:
        (start, disable_indent) = c
        comment_region = sublime.Region(dataStart,
                                        dataStart + len(start))
        if view.substr(comment_region) == start:
            required_prefix = view.substr(sublime.Region(line_begin, comment_region.end()))
            break
    return required_prefix

def expand_to_paragraph(view, tp):
    """
    Returns a region representing a "paragraph" surrounding the given text point.

    An empty region indicates that there is no paragraph here.
    """
    sr = view.full_line(tp)
    if is_blank_line(view.substr(sr)):
        return sublime.Region(tp, tp)

    # If the current line starts with a comment, only select lines that are
    # also commented.
    required_prefix = determine_required_prefix(view, sr.begin())
    #print 'required_prefix=%r' % (required_prefix,)

    # Move up until we reach a blank line, the previous paragraph, or
    # beginning of view.
    firstr = sr
    def is_para_start(lr):
        line = view.substr(lr)
        return ((lr == None or is_new_paragraph(line, required_prefix)) or
                is_blank_line(line) or
                not has_prefix(view, lr, required_prefix))

    if not is_para_start(firstr):
        # print 'first line is not start of para.'
        while True:
            prev = previous_line(view, firstr)
            if prev==None:
                # print 'start of view'
                break
            prev_line = view.substr(prev)
            if is_blank_line(prev_line):
                # print 'is blank line'
                break
            if not has_prefix(view, prev, required_prefix):
                # print 'does not have required prefix'
                break
            if is_standalone(prev_line, required_prefix):
                # print 'is standalone'
                break
            firstr = prev
            if is_new_paragraph(prev_line, required_prefix):
                # print 'is new para'
                break

    # print 'First line of expand=%r: %r' % (firstr, view.substr(firstr))

    # Move down until the end of this para.
    last = sr.end()
    next = sr
    while True:
        next = next_line(view, next)

        if next != None:
            # print 'next line=%r: %r' % (next, view.substr(next))
            nextl = view.substr(next)
        if (next == None or is_new_paragraph(nextl, required_prefix) or
                is_blank_line(nextl) or
                not has_prefix(view, next, required_prefix)):
            break
        else:
            last = next.end()

    return sublime.Region(firstr.begin(), last)

def my_full_line(view, region):
    # Special case scenario where you select an entire line.  The normal
    # "full_line" function will extend it to contain the next line (because
    # the cursor is actually at the beginning of the next line).  I would
    # prefer it didn't do that.
    if view.substr(region.end()-1) == '\n':
        return view.full_line(sublime.Region(region.begin(), region.end()-1))
    else:
        return view.full_line(region)

def all_paragraphs_intersecting_selection(view, sr):
    """Returns a list of Regions that represent "paragraphs" based on the
    given selection region.

    Empty selection regions try to be "smart" and look up and down to
    determine an entire paragraph.

    Non-empty selection regions are hard-fixed to begin at the beggining of
    the line (of the beginning of the selection) towards the end of the line
    (at the end of the selection), and then try to determine if there are
    multiple paragraphs in between (each paragraph is wrapped separately).
    """
    paragraphs = []
    if sr.empty():
        para = expand_to_paragraph(view, sr.begin())
        if not para.empty():
            paragraphs.append(para)
    else:
        # Expand the selection so the beginning starts at the start of a line
        # and the end ends at the end of a line.
        new_sr = my_full_line(view, sr)
        # print 'Initial expanded selection=%r: %r' % (new_sr, view.substr(new_sr))
        # Scanning starts at the beggining.
        para = sublime.Region(new_sr.begin(), new_sr.begin())
        while True:
            if para.end() > new_sr.end():
                # Went past the end of selection.
                # print 'Past end of selection.'
                break
            # Skip "blank" lines.
            while True:
                line = next_line(view, para)
                if line == None:
                    # End of view reached.
                    # print 'End of view while skipping blank lines.'
                    break
                if is_blank_line(view.substr(line)):
                    # Move the beginning past this blank line.
                    # print 'Skipping blank line.'
                    if line.end() <= new_sr.end():
                        para = sublime.Region(line.end(), line.end())
                    else:
                        # print 'Skipping blank line moved past selection.'
                        break
                else:
                    # Paragraph begins here.
                    para = view.full_line(para)
                    # print 'Found non-blank line.'
                    break

            required_prefix = determine_required_prefix(view, para.begin())

            # Skip till a "blank" line, or a "new paragraph" line or end of selection.
            while True:
                line = next_line(view, para)
                if line == None:
                    # End of view reached, no more new lines.
                    # print 'no next line.'
                    break
                # print 'next_line=%r' % (view.substr(line))
                if line.end() > new_sr.end():
                    # print 'Skipping lines reached end of selection line=%r new_sr=%r.' % (line, new_sr)
                    break
                line_text = view.substr(line)
                if is_blank_line(line_text):
                    # print 'Is blank line.'
                    break
                if is_new_paragraph(line_text, required_prefix):
                    # print 'Is new para.'
                    break
                if not has_prefix(view, line, required_prefix):
                    # print 'Does not have prefix.'
                    break
                # Extend the paragraph.
                para = sublime.Region(para.begin(), line.end())

            if para.empty():
                # print 'Empty paragraph, no paragraphs found in selection.'
                break
            else:
                # print 'Adding paragraph %r: %r' % (para, view.substr(para))
                paragraphs.append(para)
                para = sublime.Region(para.end()+1, para.end()+1)

    return paragraphs


class WrapLinesPlusCommand(sublime_plugin.TextCommand):
    # XXX
    list_prefix_pattern = re.compile('^[ \\t]*(([\w]+[.)])+|([-+*#]+))[ \\t]*')
    space_prefix_pattern = re.compile('^[ \\t]*')

    def extract_prefix(self, sr, tab_width):
        """Determine the initial and subsequent prefixes for the given region.
        """
        line_regions = self.view.split_by_newlines(sr)
        if len(line_regions) == 0:
            # XXX: When does this happen?
            return None, None, ''

        # If the first line starts with a line-comment, then assume all lines will be comments.
        comment_prefix = ''
        first_tp = line_regions[0].begin()
        (line_comments, block_comments) = comment.build_comment_data(self.view, first_tp)
        # print 'line_comments=%r block_comments=%r' % (line_comments, block_comments)
        dataStart = comment.advance_to_first_non_white_space_on_line(self.view, first_tp)
        for c in line_comments:
            (start, disable_indent) = c
            comment_region = sublime.Region(dataStart,
                                            dataStart + len(start))
            if self.view.substr(comment_region) == start:
                comment_prefix = self.view.substr(sublime.Region(first_tp, comment_region.end()))
                break
        # print 'comment_prefix=%r' % (comment_prefix,)

        lines = [self.view.substr(lr) for lr in line_regions]
        if comment_prefix:
            def filter_comment_prefix(x):
                if x.startswith(comment_prefix):
                    return x[len(comment_prefix):]
                else:
                    return x
            lines = map(filter_comment_prefix, lines)


        first_line = lines[0]

        # If the first line starts with a list-like thing, then that will be the initial prefix.
        list_prefix_match = self.list_prefix_pattern.match(first_line)
        if list_prefix_match:
            initial_prefix = first_line[0:list_prefix_match.end()]
            # print 'List prefix match %r' % (initial_prefix,)
            # XXX: Replace spaces with tabs when appropriate.
            subsequent_prefix = ' '*self.width_in_spaces(initial_prefix, tab_width)
        else:
            space_prefix_match = self.space_prefix_pattern.match(first_line)
            if space_prefix_match:
                initial_prefix = first_line[0:space_prefix_match.end()]
                if len(lines) > 1:
                    subsequent_prefix_match = self.space_prefix_pattern.match(lines[1])
                    if subsequent_prefix_match:
                        subsequent_prefix = lines[1][0:subsequent_prefix_match.end()]
                    else:
                        subsequent_prefix = ''
                else:
                    subsequent_prefix = initial_prefix
            else:
                return None, None, u'\n'.join(lines)
        # print 'initial_prefix=%r subsequent_prefix=%r' % (initial_prefix, subsequent_prefix)

        # Fix up the lines.
        new_lines = []
        new_lines.append(first_line[len(initial_prefix):])
        for line in lines[1:]:
            if line.startswith(subsequent_prefix):
                line = line[len(subsequent_prefix):]
            new_lines.append(line)

        # print 'new_lines=%r' % (new_lines,)
        return (comment_prefix+initial_prefix,
                comment_prefix+subsequent_prefix,
                u'\n'.join(new_lines)
               )

    def width_in_spaces(self, str, tab_width):
        sum = 0;
        for c in str:
            if c == '\t':
                sum += tab_width
            else:
                sum += 1
        return sum

    def run(self, edit, width=0):
        # print '#########################################################################'
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

        if width == 0:
            width = 78

        # Make sure tabs are handled as per the current buffer
        tab_width = 8
        if self.view.settings().get("tab_size"):
            try:
                tab_width = int(self.view.settings().get("tab_size"))
            except TypeError:
                pass

        if tab_width == 0:
            tab_width = 8
        # print 'tab_width=%r' % (tab_width,)

        paragraphs = []
        for s in self.view.sel():
            # print 'Determine paragraphs for %r' % (s,)
            paragraphs.extend(all_paragraphs_intersecting_selection(self.view, s))
        # print 'paragraphs=%r' % (paragraphs,)
        # Good for testing selection routine.
        #self.view.add_regions('test', paragraphs, 'comment', sublime.DRAW_EMPTY)
        #return

        if len(paragraphs) > 0:
            self.view.sel().clear()
            for p in paragraphs:
                self.view.sel().add(p)

            # This isn't an ideal way to do it, as we loose the position of the
            # cursor within the paragraph: hence why the paragraph is selected
            # at the end.
            for s in self.view.sel():
                wrapper = textwrap.TextWrapper()
                wrapper.expand_tabs = False
                wrapper.width = width
                init_prefix, subsequent_prefix, txt = self.extract_prefix(s, tab_width)
                # print 'init_prefix=%r subsequent_prefix=%r' % (init_prefix, subsequent_prefix)
                if init_prefix or subsequent_prefix:
                    wrapper.initial_indent = init_prefix
                    wrapper.subsequent_indent = subsequent_prefix
                    # XXX: Handle tabs.
                    #wrapper.width -= self.width_in_spaces(init_prefix, tab_width)

                if wrapper.width < 0:
                    continue

                #txt = self.view.substr(s)
                #if prefix:
                #    txt = txt.replace(prefix, u"")

                # XXX: Need to think about this.
                txt = string.expandtabs(txt, tab_width)

                # print 'wrapping %r, init=%r, subseq=%r width=%r' % (txt, wrapper.initial_indent, wrapper.subsequent_indent, wrapper.width)
                txt = wrapper.fill(txt) + u"\n"
                replaced_txt = self.view.substr(s)
                if txt != replaced_txt:
                    self.view.replace(edit, s, txt)

            # Move cursor below the last paragraph.
            end = self.view.sel()[-1].end()
            self.view.sel().clear()
            self.view.sel().add(sublime.Region(end))
