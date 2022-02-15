#!/usr/bin/env python

import yaml
import sys
import os


defaultName = "main"
defaultMain = "main"
defaultCompiler = "g++"
defaultVersion = "c++11"

def depsCheck():
    if (os.path.isfile("deps.yaml")):
        input("Already a deps.yaml here, this will delete the file. Hit enter to continue\n")
        os.remove("deps.yaml")

def generateMake():
    print("> --- Making makefile from deps.yaml --- <")

    if (not os.path.isfile("deps.yaml")):
        print("Missing deps.yaml, can be created with mmake new")
        quit()


    if (os.path.isfile("Makefile")):
        input("Already a Makefile here, this will delete the file. Hit enter to continue\n")
        os.remove("Makefile")
    
    deps = {}
    with open("deps.yaml","r") as f:
        deps = yaml.safe_load(f)
    
    name = deps['name']
    version = deps['version']
    compiler = deps['compiler']
    libsArray = deps['libs']
    libs = ""

    oFiles = ""

    for file in os.listdir("."):
        filename = os.fsdecode(file)
        if (filename.endswith(".cpp")):
            oFiles += filename.replace(".cpp",".o") + " "

    for i in libsArray:
        libs += f"-l{i} "

    with open("Makefile","w") as makefile:

        makefile.write(f"CC={compiler}\n")
        makefile.write(f"CFLAGS=-Wall -Werror -std={version} -g -O\n")
        makefile.write(f"LIBS={libs}\n")
        makefile.write(f"\n.default: all\nall: {name}\n\n")
        makefile.write(f"clean:\n\trm -rf {name} *.o\n\n")
        makefile.write(f"{name}: {oFiles}\n\t$(CC) $(CFLAGS) -o $@ $^ $(LIBS)\n\n")
        makefile.write(f"%.o: %.cpp\n\t$(CC) $(CFLAGS) -c $^ $(LIBS)\n")

        makefile.close()

    print("> Done!")




if __name__ == "__main__":

    with open("/home/danielmills/.scripts/mmake/config.yaml","r") as stream:
        try:
            config = yaml.safe_load(stream)

            defaultName = config["default-name"]
            defaultMain = config["default-main"]
            defaultCompiler = config["default-compiler"]
            defaultVersion = config["default-version"]

        except yaml.YAMLError as exc:
            print(exc)
            quit()


    argc = len(sys.argv)

    if argc > 2:
        print("ERROR: too many arguments (1 expected)")
        exit()


    if (argc == 1):
        generateMake()


        quit()

    arg = [arg for i, arg in enumerate(sys.argv) if i > 0][0]

    if (arg == "d"):
        depsCheck()

        print("> --- Generate new deps.yaml with defaults --- <")

        deps = {
            'name':defaultName,
            'main':defaultMain,
            'version':defaultVersion,
            'compiler':defaultCompiler,
            'libs':[]
        }

        print("> Done, wrote file to deps.yaml")

        with open("deps.yaml","w") as f:
            yaml.safe_dump(deps,f)

        generateMake()
        
        quit()






    if (arg == "new"):
        
        depsCheck()

        deps = {'libs':[]}

        print("> --- Generate new deps.yaml --- <")

        name = input(f"> Name of project? (defaults to '{defaultName}'): ")

        if (name.strip() == ""):
            name = defaultName
        
        print(f"> Setting name to {name}")
        deps['name'] = name

        main = input(f"> Name of main file? (defaults to '{defaultMain}', exclude .cpp): ")

        if (main.strip() == ""):
            main = defaultMain
        
        print(f"> Setting main to {main}")
        deps['main'] = main

        compiler = input(f"> Compiler? (defaults to {defaultCompiler}): ")
        
        if (compiler.strip() == ""):
            compiler = defaultCompiler
        
        print(f"> Setting compiler to {compiler}")
        deps['compiler'] = compiler

        version = input(f"> C++ Version? (defaults to {defaultVersion}): ")

        if (version.strip() == ""):
            version = defaultVersion
        
        print(f"> Setting version to {version}")
        deps['version'] = version


        print("> Done, wrote file to deps.yaml")

        with open("deps.yaml","w") as f:
            yaml.safe_dump(deps,f)

        generateMake()
        
        quit()

