# python3 main.py demo.py

from sys import argv
from os import system


def main(args):
    with open(args[1], "r") as file:
        file = file.read()
    
    compiled = """import linime, numpy as np, math

class scene(linime.Scene):

    def  __init__(self):
        super().__init__()
        
"""
    init = file.split("#PROPERTIES")[1].replace(" ","").removeprefix("\n").removesuffix("\n").replace("-"," ")
    draw = file.split("#DRAW")[1].replace(" ","").removeprefix("\n").removesuffix("\n")
    queue = file.split("#QUEUE")[1].replace(" ","").removeprefix("\n").removesuffix("\n")

    for line in init.split("new"):
        if line == "":
            continue
        name = line.split("=")[0]
        kind = line.split("=")[1].split("{")[0].removesuffix("\n")
        prop_lines = "\n"
        for i in line.split("{")[1].split("}")[0].removeprefix("\n").removesuffix("\n").split("\n"):
            prop_lines += f"        self.{name}.{i.split(':')[0]} = {i.split(':')[1]} \n"
        compiled += f"        self.{name} = linime.{kind}() {prop_lines} \n"

    compiled += "        self.queue = ["

    for line in queue.split("\n"):
        if "wait" in line:
            compiled += f"('pause', {line.split('::')[1]}),"
            continue
        elif "+" in line:
            compiled += "("
            for i in line.split("+"):
                splitted = i.split("::")
                name = splitted[0]
                prop = splitted[1].split(":")[0]
                start, end = splitted[1].split(":")[1].split("->")
                
                compiled += f"(self.{name}, '{prop}', {start}, {end}), "
            compiled += "),"
            continue
        splitted = line.split("::")
        name = splitted[0]
        prop = splitted[1].split(":")[0]
        start, end = splitted[1].split(":")[1].split("->")
        
        compiled += f"(self.{name}, '{prop}', {start}, {end}), "

    compiled += """]\n\n        self.__start__()\n\n    def __draw__(self, area, context):\n        
        if any(self.queue): self.__queue__(context)
        else: self.__show__(context)\n\n"""

    for line in draw.split("\n"):
        compiled += f"        self.{line.split('::')[1]}.__{line.split('::')[0]}__(context)"

    compiled += "\n\nscene()"

    with open("OutFile.py", "w") as out:
        out.write(compiled)
    
    system("python3 OutFile.py")

if __name__ == "__main__":
    main(argv)