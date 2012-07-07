Sublime Wrap Plus
=================
Enhanced "wrap lines" command for Sublime Text 2.

Downloading
-----------
The best way to download and install Sublime Wrap Plus is to use the Package Control plugin.  TBD

Alternatively, you can fetch from github:

	git clone git://github.com/ehuss/Sublime-Wrap-Plus.git

and place it in your packages directory.

Configuring
-----------
No need to configure anything.  By default it uses the default keystroke for wrap lines:

* Windows/Linux: Alt+Q
* OS X: Super+Alt+Q

If you want to use a different keystroke, go to "Preferences" then "Key Bindings - User", and enter something like this:

	{ "keys": ["alt+q"], "command": "wrap_lines_plus" },

Do not include the trailing comma if it is the last entry.

Using
-----
Whenever the cursor is anywhere within a paragraph, hitting the Wrap Plus keystroke will cause it to try to discover where the paragraph starts and where it ends.  It will then wrap all of those lines according to the wrap width you currently have set (View/Word Wrap Column). It handles a variety of lists, like bulleted lists or numbered lists. They should line up nicely:

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

Lines with subsequent indents should maintain their indent:

<pre>
	:param cupcake: Cupcake ipsum dolor sit amet marzipan faworki.
		Wafer I love croissant. Tart carrot cake pastry applicake
		lollipop I love  cotton brownie.
</pre>

In a source code file, it should transparently handle single-line
comment characters, like:

<pre>
    # Lorem ipsum dolor sit amet, consectetuer adipiscing elit.
    # Aenean commodo ligula eget dolor. Aenean massa. Cum sociis
    # natoque penatibus et magnis dis parturient montes, nascetur
</pre>

If you select a range of characters, *only* the lines that are selected will be wrapped (the stock Sublime wrap lines extends the selection to what it thinks is a paragraph).  I find this behavior preferable to give me more control.
