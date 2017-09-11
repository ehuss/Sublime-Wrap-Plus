

import sublime, sublime_plugin

class WrapLinesEnhancementCommand(sublime_plugin.TextCommand):
    """
    Wrap without loosing cursor position
    https://github.com/ehuss/Sublime-Wrap-Plus/issues/19

    My workaround is simple. Create a new plugin with the following implementations:
    https://github.com/ggutierrez
    """

    def run(self, edit, **kwargs):

        pos = self.view.sel()[0].begin()

        self.view.run_command('wrap_lines_plus', kwargs)
        self.view.sel().clear()
        self.view.sel().add(sublime.Region(pos))


last_used_width = 80

class WrapLinesEnhancementAskCommand(sublime_plugin.TextCommand):

    def run(self, edit, **kwargs):
        sublime.active_window().show_input_panel(
            'Provide wrapping width:', str( last_used_width ),
            self.input_package, None, None
        )

    def input_package(self, width):
        global last_used_width

        last_used_width = width
        self.view.run_command('wrap_lines_plus', { 'width': int( width ) } )


