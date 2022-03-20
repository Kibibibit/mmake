# MMake
Creates makefiles for C++ based on the cpp files
and a dependancy yaml

# Install
Currently has to be run through `[your python3 command] main.py`.

This will be updated in the future


# Usage
The program is run by calling `[your python3 command] [path to this folder]/main.py <args>` in the root directory of your C++ project.

### Arguments

- `--force/-f` - Stops the script for asking for confirmation when recreating files. defaults to `False`
- `--name/-n` - Sets the name of the compiled executable. Defaults to `main`
- `--version/-v` - Sets the C++ version. Defaults to `C++14`
- `--compiler/-c` - Sets the compiler used. Defaults to `g++`
- `--lib/-l` - Adds the given library into the dependancies for the project
- `--cflag/-cf` - Adds the given cflag into the compiler settings. By default the cflags `Wall` and `Werror` are set
- `--remove-lib` - Removes the given dependancy from the project
- `--remove-cflag` - Removes the given cflag from the settings

All of the defaults can be edited in `config.yaml`

## deps.yaml
`deps.yaml` stores all of the settings created from this script, which can be edited manually if you need


