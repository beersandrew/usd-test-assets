# USD Tools on Windows

## All UsdTools

### Install USD itself
1.  Install Microsoft Visual Studio (https://visualstudio.microsoft.com/)
    - NOTE: this is not Visual Studio Code
1.  Clone USD repo (https://github.com/PixarAnimationStudios/OpenUSD) in some directory, let's call it <usd_repo_directory>
1.  Open x64 Native Tools Command Prompt and go to <usd_repo_directory>
1.  Run `python build_scripts\build_usd.py <usd_dir>` where <usd_dir> is where you want to install USD (maybe something like C:\libs\usd_2405 )
    - NOTE: this can take awhile
1.  Set environment variables. After the previous step succeeds, you'll be shown two paths that need to be set in your envrionment. Type 'environment variables' into the search / start menu on windows and open up `Edit system environment variables`
1.  Find PATH -> Edit -> add the paths given 
    - something like `C:\libs\usd_2405\bin`
    - something like `C:\libs\usd_2405\lib`
1.  Find or create PYTHONPATH -> Edit -> add the path given 
    - something like `C:\libs\usd_2405\lib\python`
1. Restart any terminals / shells / programs you have so they can read the new path variables
1. Opening cmd or any shell now will allow you to run usd tools (usdview, usdzip...etc)
    - All tools can be found [here](https://openusd.org/release/toolset.html)

### Grab binaries from here
1. Clone this repo
1. unzip 2405 in <some_directory>/2405
1. Set environment variables. Type 'environment variables' into the search / start menu on windows and open up `Edit system environment variables`
1.  Find PATH -> Edit -> add the paths given 
    - `<some_directory>\2405\bin`
    - `<some_directory>\2405\lib`
1.  Find or create PYTHONPATH -> Edit -> add the path given 
    - `<some_directory>\2405\lib\python`
1. Restart any terminals / shells / programs you have so they can read the new path variables
1. Opening cmd or any shell now will allow you to run usd tools (usdview, usdzip...etc)
    - All tools can be found [here](https://openusd.org/release/toolset.html)

## UsdView Only

This can be run from Ominverse
- Go to https://www.nvidia.com/en-us/omniverse/
- Download from `Omniverse Kit & Developer Tools`
- After installing open the app
- Go to Exchange
- Go to Apps
- Find USD USDView
- Install
- Open (Now it should be in the Library Tab)
