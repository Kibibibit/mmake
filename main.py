#!/usr/bin/env python


import yaml
import sys
import os

CONFIG_PATH = os.path.dirname(os.path.abspath(__file__))+"/config.yaml"
DEPS_PATH = "deps.yaml"
MAKE_PATH = "Makefile"

DEFAULT_NAME = "default-name"
FIELD_NAME = "name"

DEFAULT_VERSION = "default-version"
FIELD_VERSION = "version"

DEFAULT_COMPILER = "default-compiler"
FIELD_COMPILER = "compiler"

DEFAULT_CFLAGS = "default-cflags"
FIELD_CFLAGS = "cflags"

FIELD_LIBS = "libs"

ARG_FORCE = "--force"
ARG_NAME = "--name"
ARG_VERSION = "--version"
ARG_COMPILER = "--compiler"
ARG_LIB = "--lib"
ARG_REMOVE_LIB = "--remove-lib"
ARG_CFLAG = "--cflag"
ARG_REMOVE_CFLAG = "--remove-cflag"

SHORTS = {

    "-f":ARG_FORCE,
    "-n":ARG_NAME,
    "-v":ARG_VERSION,
    "-c":ARG_COMPILER,
    "-l":ARG_LIB,
    "-rl":ARG_REMOVE_LIB,
    "-cf":ARG_CFLAG,
    "-rcf":ARG_REMOVE_CFLAG
}


ARGS = [
    ARG_NAME,
    ARG_VERSION,
    ARG_COMPILER,
    ARG_LIB,
    ARG_FORCE,
    ARG_CFLAG,
    ARG_REMOVE_CFLAG,
    ARG_REMOVE_LIB
]

def log(level, value):
    print(f"[MMAKE][{level}] {value}")

def info(value):
    log("INFO",value)

def warn(value):
    log("WARN",value)

def error(value):
    log("ERROR",value)

def fileExists(path):
    return os.path.isfile(path)

def readYaml(path):

    with openYaml(path,mode="r") as file:
        try:
            return yaml.safe_load(file)
        except yaml.YAMLError as e:
            error(f"Error loading {path}:\n{e}")
            
def openYaml(path, mode="w"):
    return open(path, mode)

def importConfig():
    return readYaml(CONFIG_PATH)

def getArgValue(arg, args):
    if (len(args) > 0):
        if (args[0] not in ARGS):
            return args[0].strip()
    error(f"{arg} requires a value!")
    quit()

if __name__ == "__main__":
    configs = importConfig()

    force = False

    depsExists = fileExists(DEPS_PATH)

    deps = {
        FIELD_NAME:configs[DEFAULT_NAME],
        FIELD_VERSION:configs[DEFAULT_VERSION],
        FIELD_COMPILER:configs[DEFAULT_COMPILER],
        FIELD_CFLAGS:configs[DEFAULT_CFLAGS]
    }

    if (depsExists):
        deps = readYaml(DEPS_PATH)

    args = [arg for i, arg in enumerate(sys.argv) if i > 0]

    for i in range(len(args)):
        if (args[i] in SHORTS.keys()):
            args[i] = SHORTS[args[i]]

    noArgs = True

    while len(args) > 0:
        noArgs = False
        arg = args[0]
        if (arg in ARGS):
            if (arg == ARG_FORCE):
                force = True

            elif (arg == ARG_NAME):
                args = args[1:]
                deps[FIELD_NAME] = getArgValue(ARG_NAME,args)
            
            elif (arg == ARG_COMPILER):
                args = args[1:]
                deps[FIELD_COMPILER] = getArgValue(ARG_COMPILER,args)
            
            elif (arg == ARG_VERSION):
                args = args[1:]
                deps[FIELD_VERSION] = getArgValue(ARG_VERSION,args)
            
            elif (arg == ARG_LIB):
                args = args[1:]
                if (not FIELD_LIBS in deps.keys()):
                    deps[FIELD_LIBS] = []
                deps[FIELD_LIBS].append(getArgValue(ARG_LIB,args))

            elif (arg == ARG_CFLAG):
                args = args[1:]
                if (not FIELD_CFLAGS in deps.keys()):
                    deps[FIELD_CFLAGS] = []
                deps[FIELD_CFLAGS].append(getArgValue(ARG_CFLAG,args))
            
            elif (arg == ARG_REMOVE_LIB):
                args = args[1:]
                remove = getArgValue(ARG_REMOVE_LIB,args)
                if (not FIELD_LIBS in deps.keys()):
                    warn(f"No libs found to remove!")
                else:
                    while remove in deps[FIELD_LIBS]:
                        deps[FIELD_LIBS].remove(remove)

            elif (arg == ARG_REMOVE_CFLAG):
                args = args[1:]
                remove = getArgValue(ARG_REMOVE_CFLAG,args)
                if (not FIELD_CFLAGS in deps.keys()):
                    warn(f"No clfags to remove!")
                else:
                    while remove in deps[FIELD_CFLAGS]:
                        deps[FIELD_CFLAGS].remove(remove)
                

        else:
            error(f"Unknown arg: '{arg}'")
            quit()

        if (len(args) > 0):
            args = args[1:]

    if (depsExists):
        if (not force):
            warn("deps.yaml already exists! This will be recreated if you continue.\nHit Enter to continue")
            input()
        os.remove(DEPS_PATH)
    with openYaml(DEPS_PATH) as file:
        yaml.safe_dump(deps,file)

    if (os.path.isfile(MAKE_PATH)):
        if (not force):
            warn("Makefile already exists! This will be recreated if you continue.\nHit Enter to continue")
            input()
        os.remove(MAKE_PATH)

    libs = ""
    oFiles = ""
    cflags = ""

    for file in os.listdir("."):
        filename = os.fsdecode(file)
        if (filename.endswith(".cpp")):
            oFiles += filename.replace(".cpp",".o") + " "

    if (not FIELD_LIBS in deps.keys()):
        deps[FIELD_LIBS] = []
    for i in deps[FIELD_LIBS]:
        libs += f"-l{i} "
    
    for i in deps[FIELD_CFLAGS]:
        cflags += f"-{i} "

    

    with open("Makefile","w") as makefile:

        makefile.write(f"CC={deps[FIELD_COMPILER]}\n")
        makefile.write(f"CFLAGS={cflags} -std={deps[FIELD_VERSION]} -g -O\n")
        makefile.write(f"LIBS={libs}\n")
        makefile.write(f"\n.default: all\nall: {deps[FIELD_NAME]}\n\n")
        makefile.write(f"clean:\n\trm -rf {deps[FIELD_NAME]} *.o\n\n")
        makefile.write(f"{deps[FIELD_NAME]}: {oFiles}\n\t$(CC) $(CFLAGS) -o $@ $^ $(LIBS)\n\n")
        makefile.write(f"%.o: %.cpp\n\t$(CC) $(CFLAGS) -c $^ $(LIBS)\n")

        makefile.close()
