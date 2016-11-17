=======================
Build ledger on Windows
=======================

Overview and versions
=====================

#.  Install `Guthub Desktop Windows 
    <https://desktop.github.com/>`__
#.  Install `Visual Studio Express 2015
    <https://www.visualstudio.com/downloads/download-visual-studio-vs#d-express-windows-desktop>`__
#.  Install `CMake <https://cmake.org/download/>`__ 3.7.0
#.  Clone this repository
#.  Build `Boost <http://www.boost.org/users/download/>`__ 1.62.0
#.  Build `MPIR <http://mpir.org/>`__ (master)
#.  Build `MPFR <http://www.mpfr.org/mpfr-current/#download>`__ (master)
#.  Build `ledger <http://ledger-cli.org/>`__ (master)

Detail
======

#.  `Download <https://github-windows.s3.amazonaws.com/GitHubSetup.exe>`__, install Guthub Desktop Windows

#.  `Download <https://go.microsoft.com/fwlink/?LinkId=691984>`__, install Visual
    Studio Express 2015 for Windows Desktop


#.  `Download <https://cmake.org/files/v3.7/cmake-3.7.0-win32-x86.msi>`__
    and install CMake; adding it to the `PATH`

#.  Run in Git shell:: 

        git clone https://github.com/AndrewSav/ledger-windows-build.git --recursive

  Make sure to double check the url in case of forked repo

*In each step below choose to extract the package contents into the root of
this repository. 'At the command prompt, run' means use the `VS2015 x86 Native
Tools Command Prompt` to execute the commands listed, starting with the current
directory as the repository root.*

5.  `Download <http://sourceforge.net/projects/boost/files/boost/1.62.0/
    boost_1_62_0.zip/download>`__ and extract `boost_1_60_0`, then at the
    command prompt, run::

        cd ..
        ren boost_1_62_0 boost
        cd boost
        .\bootstrap.bat
        .\b2.exe link=static runtime-link=static threading=multi ^
           --layout=versioned
   
    Note that the ``boost`` folder should be at the same level as ``ledger-windows-build`` folder (sibling)

#.  At the command prompt, run::

        cd mpir\build.vc14
        .\msbuild.bat gc LIB Win32 Release

#.  At the command prompt, run::

        cd mpfr\build.vc14\lib_mpfr
        msbuild /p:Configuration=Release lib_mpfr.vcxproj

#.  At the command prompt, run the following to build `ledger.exe`::

        cd ledger
        cmake ^
            -DCMAKE_BUILD_TYPE:STRING="Release" ^
            -DBUILD_LIBRARY=OFF ^
            -DMPFR_LIB:FILEPATH="../../mpfr/build.vc14/lib/Win32/Release/mpfr" ^
            -DGMP_LIB:FILEPATH="../../mpir/lib/win32/Release/mpir" ^
            -DMPFR_PATH:PATH="../mpfr/lib/Win32/Release" ^
            -DGMP_PATH:PATH="../mpir/lib/win32/Release" ^
            -DBUILD_DOCS:BOOL="0" ^
            -DHAVE_REALPATH:BOOL="0" ^
            -DHAVE_GETPWUID:BOOL="0" ^
            -DHAVE_GETPWNAM:BOOL="0" ^
            -DHAVE_IOCTL:BOOL="0" ^
            -DHAVE_ISATTY:BOOL="0" ^
            -DBOOST_ROOT:PATH="../../boost/" ^
            -DBoost_USE_STATIC_LIBS:BOOL="1" ^
            -DCMAKE_CXX_FLAGS_RELEASE:STRING="/MT /Zi /Ob0 /Od" ^
            -G "Visual Studio 14"
        msbuild /p:Configuration=Release src\ledger.vcxproj
        copy Release\ledger.exe ..\

    Note that the error message about not being able to find Python can be safely ignored. Python is only used for running tests, which is not part of the process described here


Updating to a later version of ledger/mpir/mpfr
===============================================

Run these commands from Git shell to update pull a later commit of ledger/mpir/mpfr to build off::

    cd ledger
    git checkout master
    cd ../mpir
    git checkout master
    cd ../mpfr
    git checkout master

Note, you can use any appropirate branch or commit number instead of ``master``. You might need to fix the build process after executing the above if it breaks.


Notes
=====

-   These instructions are based upon the `wiki page
    <https://github.com/ledger/ledger/wiki/
    Build-instructions-for-Microsoft-Visual-C---11-(2012)>`__ by Tim Crews
-   Boost is time consuming to build, especially as we have to build all of
    the libraries to build the unit test framework; the other libraries can be
    built at the same time

Licenses
========

Boost
-----

::

    Distributed under the Boost Software License, Version 1.0. (See
    accompanying file LICENSE_1_0.txt or copy at
    http://www.boost.org/LICENSE_1_0.txt)

MPIR
----

::

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

MPFR
----

::

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

Ledger
------

::

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

.. vim: ft=rst
