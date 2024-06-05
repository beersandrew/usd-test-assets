# Info on building USD in Debug mode

## macOS

### CLion

1. Clone repo
2. Build OpenUSD with the python build script
    - `python3 build_scripts/build_usd.py -v <build_script_build_dir>`
    - `-v` here is used to get the CMake options below
3. Add CMake options
```
-DCMAKE_INSTALL_PREFIX="<install_dir>" -DCMAKE_PREFIX_PATH="<install_dir>" -DCMAKE_BUILD_TYPE=Debug -DCMAKE_MACOSX_RPATH=ON   -DPXR_PREFER_SAFETY_OVER_SPEED=ON -DPXR_ENABLE_PYTHON_SUPPORT=ON -DPXR_USE_DEBUG_PYTHON=OFF -DPython3_EXECUTABLE="/Users/andrewbeers/.pyenv/versions/3.9.8/bin/python3" -DPython3_LIBRARY="/Users/andrewbeers/.pyenv/versions/3.9.8/lib/libpython3.9.dylib" -DPython3_INCLUDE_DIR="/Users/andrewbeers/.pyenv/versions/3.9.8/include/python3.9" -DBUILD_SHARED_LIBS=ON -DTBB_USE_DEBUG_BUILD=OFF -DPXR_BUILD_DOCUMENTATION=OFF -DPXR_BUILD_HTML_DOCUMENTATION=OFF -DPXR_BUILD_PYTHON_DOCUMENTATION=OFF -DPXR_BUILD_TESTS=OFF -DPXR_BUILD_EXAMPLES=ON -DPXR_BUILD_TUTORIALS=ON -DPXR_BUILD_USD_TOOLS=ON -DPXR_BUILD_IMAGING=ON -DPXR_ENABLE_PTEX_SUPPORT=OFF -DPXR_ENABLE_OPENVDB_SUPPORT=OFF -DPXR_BUILD_EMBREE_PLUGIN=OFF -DPXR_BUILD_PRMAN_PLUGIN=OFF -DPXR_BUILD_OPENIMAGEIO_PLUGIN=OFF -DPXR_BUILD_OPENCOLORIO_PLUGIN=OFF -DPXR_BUILD_USD_IMAGING=ON -DPXR_BUILD_USDVIEW=ON -DPXR_BUILD_ALEMBIC_PLUGIN=OFF -DPXR_BUILD_DRACO_PLUGIN=OFF -DPXR_ENABLE_MATERIALX_SUPPORT=ON -DPXR_BUILD_MAYAPY_TESTS=OFF -DPXR_BUILD_ANIMX_TESTS=OFF -DBoost_NO_BOOST_CMAKE=On -DBoost_NO_SYSTEM_PATHS=True -DBoost_INCLUDE_DIR="<build_script_build_dir>/include" -DCMAKE_XCODE_ATTRIBUTE_ONLY_ACTIVE_ARCH=YES -DCMAKE_OSX_ARCHITECTURES=arm64 "<clone_dir>/OpenUSD""
```

You can get the above list by running the OpenUSD build script with -v for verbose, the CMake options will be printed in the terminal.

4. Add Build options
```
--target install -j10
```
5. Update `cmake/modules/FindOpenSubdiv.cmake`
    - add <build_script_build_dir>/lib under
    ```SET(_opensubdiv_SEARCH_DIRS
        ${OPENSUBDIV_ROOT_DIR}
        <build_script_build_dir>/lib
    ...
    ```
6. Build CMake project to generate build configurations
    - this creates <cmake_build_dir> which should be thought of as a 'staging' area and not a running / debugging dir
7. Click Debug on the build configuration / scheme you want to debug, this will run the install job
    - This should trigger an error of not finding `libboost_python39.dylib` but it generates <install_dir>
8. Copy all non usd libs from <build_script_build_dir>/lib to <install_dir>/lib
    - this includes `libboost_python39.dylib` and other dependencies pulled in by the build script
9. Edit the build configuration / scheme you want to debug and change the exe to correct exe file which is <install_dir>/bin, by default it will select <cmake_build_dir>


Thread for this question is (here)[https://forum.aousd.org/t/setting-up-debugging-usd-code-in-clion-on-macos/1542]