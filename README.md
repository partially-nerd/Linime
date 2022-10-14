# Linime
A PyCairo + PyGObject based animation engine for linux
NOTE: Windows support (probably using tkinter for the main canvas and window) will be added soon

The engine takes in a .linime file, and compiles it to python, which uses the module functions for its animation.
`NOTE: numpy is imported as np in linime, and math as math`

# Syntax
Take a look at demo.linime and hack at it yourself. While it hasn't got the most complicated of animations, it should hopefully give a sense of how simple the process is. To run it, just  execute `python3 main.py demo.linime` in the working directory. Might also be really helpful if you set language mode to RUBY for .linime files in vscode, as some snippets are configured, and syntax highlighting works quite neatly. 
- init (for the base code)
- new (for a new linime object)
- trans (for the queue transition object)
- wait (for pause)
- draw (for drawing an object)
