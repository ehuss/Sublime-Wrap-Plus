# Sublime Wrap Plus #
Enhanced "wrap lines" command for Sublime Text 2.  This is for the *manual* hard line wrap command (Alt-Q in Windows, Command-Alt-Q in OS X).  It does not affect the automatic soft line wrapping.

## Downloading ##
The best way to download and install Sublime Wrap Plus is to use the Package Control plugin.  If you do not already have it installed, it's really the best way to manage your packages.

For users new to the package manager:
* Go to http://wbond.net/sublime_packages/package_control and install Package Control.
* Restart Sublime Text 2.

Install Sublime Wrap Plus:
* Bring up the Command Palette (`Command+Shift+P` on OS X, `Control+Shift+P` on Linux/Windows).
* Select "Package Control: Install Package" and wait while Package Control fetches the latest package list.
* Select Wrap Plus when the list appears.

Package Control will handle automatically updating your packages.

Alternatively, you can fetch from github:

	git clone git://github.com/ehuss/Sublime-Wrap-Plus.git

and place it in your packages directory.

## Configuring ##
No need to configure anything.  By default it uses the default keystroke for wrap lines:

* Windows/Linux: Alt+Q
* OS X: Super+Alt+Q

If you want to use a different keystroke, go to "Preferences" then "Key Bindings - User", and add an entry like this:

	{ "keys": ["alt+q"], "command": "wrap_lines_plus" },

Do not include the trailing comma if it is the last entry.

There are a few settings you can tweak if you so desire.  You can set them in Preferences / Settings-User.  They are:

<table>
  <tr>
    <th>Name</th><th>Default</th><th>Description</th>
  </tr>
  <tr>
    <td>"WrapPlus.break_long_words"</td>
    <td>true</td>
    <td>A single word that is longer than your wrap column will be forced to be break at the wrap column.</td>
  </tr>
  <tr>
    <td>"WrapPlus.break_on_hyphens"</td>
    <td>true</td>
    <td>Whether or not to break lines on hyphens.</td>
  </tr>
</table>

## Using ##
Whenever the cursor is anywhere within a paragraph, hitting the Wrap Plus keystroke will cause it to try to discover where the paragraph starts and where it ends.  It will then wrap all of those lines according to the wrap width you currently have set (View/Word Wrap Column).

### Lists ###
It handles a variety of lists, like bulleted lists or numbered lists. They should line up nicely:

<pre>
	- Kielbasa beef andouille chuck short loin, filet mignon jerky
      tail fatback ball tip meatloaf sausage spare ribs bresaola
      rump.
	* Shankle shoulder ham, strip steak pastrami ground round shank
      sausage tail corned beef drumstick boudin bacon prosciutto
      turkey.
	1. Jerky prosciutto pork loin shankle, corned beef capicola
       pork pastrami fatback short loin ground round.
		a. Sirloin fatback pancetta pork belly ham hock strip
           steak chuck, drumstick brisket chicken corned
           beef speck pig kielbasa short loin.
</pre>

### Subsequent Indents ###
Lines with subsequent indents should maintain their indent:

<pre>
	:param cupcake: Cupcake ipsum dolor sit amet marzipan faworki.
		Wafer I love croissant. Tart carrot cake pastry applicake
		lollipop I love cotton brownie.
</pre>

### Comment Lines ###
In a source code file, it should transparently handle single-line
comment characters, like:

<pre>
    # Lorem ipsum dolor sit amet, consectetuer adipiscing elit.
    # Aenean commodo ligula eget dolor. Aenean massa. Cum sociis
    # natoque penatibus et magnis dis parturient montes, nascetur
</pre>

If you use block-style comments in C or C++, it will restrict the wrapping to only the contents in the comment (it won't jump out and wrap nearby code lines).  Also, if you use funny C block comments that start with an asterisk, that should be preserved:

<pre>
    /*
     * This is a multiline C-style comment.  The asterisk characters on the
     * left should be preserved (when in C or C++ mode), if they are already
     * there.
     */
</pre>

In addition, JavaDoc or JsDoc style documentation should work, too:

<pre>
    /**
     * Sample function description.  Just in case the description is very long.
     * Cupcake ipsum dolor sit amet marzipan faworki. Wafer I love croissant. Tart
     * carrot cake pastry applicake lollipop I love cotton brownie.
     * @param {string} paramname Multi-line parameter description (or any javadoc
     *     tag) should indent with 4 spaces.  Cupcake ipsum dolor sit amet
     *     marzipan faworki. Wafer I love croissant. Tart carrot cake pastry
     *     applicake lollipop I love cotton brownie.
     */
</pre>

### Python Strings ###
When wrapping inside a Python triple quoted string, wrapping will be constrained to the inside of the string.  That way, doc strings won't get wrapped with function definitions:

<pre>
    def foo():
        """Pressing the wrap lines character while inside this string should wrap it
        nicely, without affecting the def foo line.
        """
</pre>

### Email Quotes ###
Lines with email-style quoting should be handled.  Nested quotes should be treated as separate paragraphs.

<pre>
    &gt; This is a quoted paragraph.
    &gt; &gt; This is a nested quoted paragraph.  Wrapping the first paragraph won't
    &gt; &gt; touch this paragraph.
    &gt; And continuing with a third paragraph.
</pre>

### Selection Wrapping ###
If you select a range of characters, *only* the lines that are selected will be wrapped (the stock Sublime wrap lines extends the selection to what it thinks is a paragraph).  I find this behavior preferable to give me more control.

## Epilogue ##
Wrap Plus handles a lot of situations that the stock Sublime word wrapper doesn't handle, but it's likely there are many situations where it doesn't work quite right.  If you come across a problem, the immediate solution is to manually select the lines you want to wrap (this will constrain wrapping to just those lines).  If you'd like, feel free to post an issue on the github page: https://github.com/ehuss/Sublime-Wrap-Plus
