# Build ledger on Windows
## Overview and versions
Three ways to build ledger on Windows are presented in this directory. All the steps are essentially the same in all the three, the difference is how, when and where they are executed.

- The easy way is just download the binary from the Releases page in this GitHub repository. This binary is built with [GitHub Actions](https://github.com/features/actions) on GitHub hardware and software. 
- You can build the binary yourself by installing the prerequisites, cloning the repository and running a provided PowerShell script.
- The hard way is to run all the commands from the command line - this way you will know exactly what you are doing.

The steps to compile ledger that the three ways mentioned above execute are:

1. Install [Visual Studio 2019](https://www.visualstudio.com/downloads/). GitHub Actions use Visual Studio Enterprise. The PowerShell script and the Hard Way were tested on the Community Edition, but should work with other editions too.
2. Install [CMake](https://cmake.org/download/) 3.17.0 was tested for manual installs. Actions use their own current version.
3. Clone [this repository](https://github.com/maxwell-k/ledger-windows-build)
4. Build [Boost](http://www.boost.org/users/download/) 1.72.0 was tested for manual installs. Actions use their own current version.
5. Build [MPIR](http://mpir.org/) (master)
6. Build [MPFR](http://www.mpfr.org/mpfr-current/#download) (master)
7. Build [ledger](http://ledger-cli.org/) (master)

## Automated Build with GitHub Actions

This section is intended for repository maintainers, and those who would like to educate themselves. If you just want the binary, head to the Releases page and be done with it.

GitHub provides some software and libraries in its Actions environment, notably Visual Studio, CMake and boost. It's nice that you do not need to download and install / build those, but it also means that you cannot choose versions, you get what is already there. Since GitHub constantly updates their environment templates it can potentially break the automated build in future.

At the moment of writing, the repository contains three different actions, only one of them is in use:

- [build.yaml](.github/workflows/build.yaml) - this action is in use, and is build automatically upon tagging a commit (see below). It uses the same [build.ps1](build.ps1) script as the manual process uses
- [build-with-boost.yaml](.github/workflows/build-with-boost.yaml) - this action does not use the boost library provided by GitHub build environment, instead it pulls boost sources and builds them. This makes for a very long build (about 60 minutes comparing to 10 minutes build when using pre-built libraries). This action can be used as a template if in future there is an incompatibility with boost version
- [build-without-boost.yaml](.github/workflows/build-without-boost.yaml) - this action does not use the `build.ps1` script and instead uses Action Steps to perform the same tasks the PowerShell script provides. It can be used for reference in case of future incompatibilities around the PowerShell script.

In order to kick off a new releases follow these steps:

- Clone the repository with `--recursive` flag

- Update submodules:

  ```powershell
  cd ledger
  git checkout <tag>
  cd ../mpir
  git checkout master
  cd ../mpfr
  git checkout master
  ```

  *<u>Note</u>, that you have to replace `<tag>` above with tag, branch or commit number of the ledger repository commit you would like to build.*

  *<u>Note</u>, that other commits of those three submodules  than those in this repository may require a different build process.*

- Commit your changes, push the commit, tag it and push the tag:

  ```bash
  git commit -m "Updating to <tag>" -a
  git push
  git tag <tag>
  git push origin --tags
  ```
  

At this point, the GitHub Actions will kick in and you will be able to watch it build, on the Actions tab of this repo. When the build succeeds a release will be created automatically corresponding to the tag name you specified above.

*<u>Note on forks:</u> when this repo is forked, GitHub will ask you whether or not you would like to enable Actions. Generally Actions are free for public repositories, but it's your responsibility to check if this is so in your case.*

## Prerequisites for manual build

These instructions were tested on **Windows 10**. They may also work on other flavors of Windows as long the software below is installed. Visual Studio 2019 cannot be installed on some older versions of Windows.

- [Download](https://visualstudio.microsoft.com/thank-you-downloading-visual-studio/?sku=Community&rel=16), install Visual Studio Community 2019. When installing make sure to install "Desktop development with C++" payload and "Git for Windows" component. Make sure that `git` is available on your `PATH`.

- [Download](https://github.com/Kitware/CMake/releases/download/v3.17.0/cmake-3.17.0-win64-x64.msi) and install CMake; adding it to the `PATH`

- If you are using up-to-date Windows 10, you most likely already have `curl.exe` on your path. If not, [download](https://curl.haxx.se/windows/) it and put on your path.

  *<u>Note:</u> these instructions were tested with curl.exe that comes with Windows 10.*

  *<u>Note:</u> PowerShell has alias `curl` which is different from `curl.exe` when you check if you have curl, make sure that you are checking for `curl.exe`, not for `curl` alias.*

- [Download](https://www.7-zip.org/download.html), install 7zip, and make sure it's on `PATH`. `7z` boost archive is expanded much faster than `zip`

- Clone the repository recursively:

  ```powershell
  git clone https://github.com/maxwell-k/ledger-windows-build --recursive
  ```

  *<u>Note:</u> Use a different URL above if you are using a fork of the original instructions.*

## Using PowerShell script to build ledger

Open `Developer PowerShell for VS 2019` and make sure that the current folder is the root of this recursively cloned repo. Run:

```powershell
.\build.ps1
```

The build time can be an hour or more, depending on your machine. If there was no errors you should end up with `ledger.exe` in your current folder, when the build finishes.

## Building Ledger the Hard Way

*In the steps below 'at the command prompt' means use the `Developer PowerShell for VS 2019` to execute the commands listed, starting with the current directory as the repository root.*

[Download](https://dl.bintray.com/boostorg/release/1.72.0/source/boost_1_72_0.zip) and extract `boost_1_72_0` to the root of this repository, then build Boost using the following at the command prompt::

```powershell
mv boost_1_72_0 boost
cd boost
.\bootstrap.bat
.\b2.exe link=static runtime-link=static threading=multi -- layout=versioned
cd ..
```

At the command prompt run the following to build `mpir`:

    cd mpir\msvc\vs19
    msbuild.exe /p:Platform=win32 /p:Configuration=Release .\lib_mpir_gc\lib_mpir_gc.vcxproj
    msbuild.exe /p:Platform=win32 /p:Configuration=Release .\lib_mpir_cxx\lib_mpir_cxx.vcxproj
    cd ..\..\..

At the command prompt run the following to build `mpfr`:

    cd mpfr\build.vs19\lib_mpfr
    msbuild /p:Configuration=Release lib_mpfr.vcxproj
    cd ..\..\..

At the command prompt run the following to build ``ledger.exe``:

    cd ledger
    cmake `
      '-DCMAKE_BUILD_TYPE:STRING=Release' `
      '-DBUILD_LIBRARY=OFF' `
      '-DMPFR_LIB:FILEPATH=../../mpfr/build.vs19/lib/Win32/Release/mpfr' `
      '-DGMP_LIB:FILEPATH=../../mpir/lib/win32/Release/mpir' `
      '-DMPFR_PATH:PATH=../mpfr/lib/Win32/Release' `
      '-DGMP_PATH:PATH=../mpir/lib/win32/Release' `
      '-DBUILD_DOCS:BOOL=0' `
      '-DHAVE_GETPWUID:BOOL=0' `
      '-DHAVE_GETPWNAM:BOOL=0' `
      '-DHAVE_IOCTL:BOOL=0' `
      '-DHAVE_ISATTY:BOOL=0' `
      '-DBOOST_ROOT:PATH=../boost/' `
      '-DBoost_USE_STATIC_LIBS:BOOL=1' `
      '-DBoost_USE_STATIC_RUNTIME:BOOL=1' `
      '-DCMAKE_CXX_FLAGS_RELEASE:STRING=/MT /Zi /Ob0 /Od' `
      -A Win32 `
      -G "Visual Studio 16"
    msbuild /p:Configuration=Release src\ledger.vcxproj
    cd ..
    cp ledger\Release\ledger.exe ledger.exe

You should now have `ledger.exe` at your current folder in the root of the cloned repository.

## Notes

- These instructions were initially derived from the [wiki page](https://github.com/ledger/ledger/wiki/Build-instructions-for-Microsoft-Visual-C---11-(2012)) by Tim Crews.
- Boost is time consuming to build, especially as we have to build all of the libraries to build the unit test framework; the other libraries can be built at the same time.
- Thanks to [Andrew Savinykh](https://github.com/AndrewSav) for recent updates.

## Licenses

### Boost

    Distributed under the Boost Software License, Version 1.0. (See accompanying file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)

### MPIR

    Copyright 1993, 1994, 1995, 1996, 1997, 2000, 2001, 2002, 2003, 2005 Free
    Software Foundation, Inc.
    
    Copyright 2009 B R Gladman
    
    This file is part of the GNU MP Library.
    
    The GNU MP Library is free software; you can redistribute it and/or modify
    it under the terms of the GNU Lesser General Public License as published by
    the Free Software Foundation; either version 2.1 of the License, or (at
    your option) any later version.
    
    The GNU MP Library is distributed in the hope that it will be useful, but
    WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
    or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public
    License for more details.
    
    You should have received a copy of the GNU Lesser General Public License
    along with the GNU MP Library; see the file COPYING.LIB.  If not, write to
    the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor,
    Boston, MA 02110-1301, USA.

### MPFR

    Copyright 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010,
    2011, 2012, 2013 Free Software Foundation, Inc. Contributed by the AriC and
    Caramel projects, INRIA.
    
    The GNU MPFR Library is free software; you can redistribute it and/or
    modify it under the terms of the GNU Lesser General Public License as
    published by the Free Software Foundation; either version 3 of the License,
    or (at your option) any later version.
    
    The GNU MPFR Library is distributed in the hope that it will be useful, but
    WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
    or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public
    License for more details.
    
    You should have received a copy of the GNU Lesser General Public License
    along with the GNU MPFR Library; see the file COPYING.LESSER.  If not, see
    http://www.gnu.org/licenses/ or write to the Free Software Foundation,
    Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301, USA.

### Ledger

    Copyright (c) 2003-2009, John Wiegley.  All rights reserved.
    
    Redistribution and use in source and binary forms, with or without
    modification, are permitted provided that the following conditions are met:
    
    - Redistributions of source code must retain the above copyright notice,
      this list of conditions and the following disclaimer.
    
    - Redistributions in binary form must reproduce the above copyright notice,
      this list of conditions and the following disclaimer in the documentation
      and/or other materials provided with the distribution.
    
    - Neither the name of New Artisans LLC nor the names of its
      contributors may be used to endorse or promote products derived from
      this software without specific prior written permission.
    
    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
    AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
    IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
    ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
    LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
    CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
    SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
    INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
    CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
    ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
    POSSIBILITY OF SUCH DAMAGE.
