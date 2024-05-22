# Info on building USD in Debug mode

## macOS

### CLion

1. Download and install [CLion](https://www.jetbrains.com/clion/)
2. Clone [OpenUSD](https://github.com/PixarAnimationStudios/OpenUSD)
3. Build USD through the command line
    1. `python3 build_scripts/build_usd.py <build_dir>`
    2. (The purpose of this is to have references for dependencies)
4. Set the following Environment Variables
    1. `TBBROOT="<build_dir>/include"`
    2. `LIBRARY_PATH="<build_dir>/lib"`
    3. `OPENSUBDIV_ROOT_DIR="<build_dir>/include"`
5. Update `cmake/defaults/Packages.cmake`
    1. Unless I do this, CMake will not find the Python that I want it to find, anyway to set this environmentally would be great!
    2.  `set(PYTHON_EXECUTABLE <path_to_python_executable>)`
        1. Example: `set(PYTHON_EXECUTABLE "/Users/andrewbeers/.pyenv/versions/3.9.8/bin/python3.9")`
    3. `set(PYTHON_INCLUDE_DIRS <path_to_python_include_folder>)`
        1. Example: `set(PYTHON_INCLUDE_DIRS "/Users/andrewbeers/.pyenv/versions/3.9.8/include/python3.9")`
    4. `set(PYTHON_VERSION_MAJOR <major_python_version>)` 
        1. Example: `set(PYTHON_VERSION_MAJOR "3")`
    5. `set(PYTHON_VERSION_MINOR <minor_python_version>)`
        1. Example: `set(PYTHON_VERSION_MINOR "9")`
6. Open CLion
7. Open CMakeLists.txt, use this as the CMake Profile
8. The project should build



### Issues

When trying to run `usdcat` to debug and step through the code, I run into an issue with plugins not loading properly. It appears this happens because the way CMake builds the code is not the same as how the `build_usd.py` build script does. 

Specifically, when using build_usd.py I get a structure that looks like `lib/path1/path2/resources/plugInfo.json` where that plugInfo.json will reference a lib in lib, something like:

```
"LibraryPath": "../../libusd_usd.dylib", 
"Name": "usd", 
"ResourcePath": "resources", 
"Root": "..", 
"Type": "library"
```

Where on disk it looks like:

- <build_dir>
    - lib
        - usd
            - usd
                - resources
                    - plugInfo.json
        - libusd_usd.dylib

When building with CMake I get a completely different structure. 

`cmake-build-debug` gets created at the root level of the project but there is no lib folder, thus no resources folders, so even including the plugInfo.json paths in PXR_PLUGIN_PATH does not work since the relative paths within the plugInfo.json's do not lead to the actual lib paths, and manually copying lib files to where they should be does not seem to work either.