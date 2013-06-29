=======================
Build ledger on Windows
=======================

Overview and versions
=====================

#.  Install `Visual Studio Express 2012
    <http://www.microsoft.com/visualstudio/eng>`__
#.  Install `CMake <http://www.cmake.org/>`__ 2.8.11
#.  Install `Yasm <http://yasm.tortall.net/>`__ 1.2.0
#.  Build `Boost <http://www.boost.org/users/download/>`__ 1.53.0
#.  Build `MPIR <http://mpir.org/>`__ 2.6.0
#.  Build `MPFR <http://www.mpfr.org/mpfr-current/#download>`__ 3.1.2
#.  Download and extract `ledger <http://ledger-cli.org/>`__ (master)
#.  Download and extract `utfcpp <http://utfcpp.sourceforge.net/>`__ 2.3.4
#.  Build `ledger`

Detail
======

#.  `Download <http://www.microsoft.com/visualstudio/
    eng/downloads#d-express-windows-desktop>`__, install and register Visual
    Studio Express 2012 for Windows Desktop

#.  `Download <http://www.tortall.net/projects/
    yasm/releases/vsyasm-1.2.0-win32.zip>`__ the Visual Studio version of
    `yasm`, and extract everything except `readme.txt` into the system `PATH`,
    for example into `C:\\Program Files (x86)\\Microsoft Visual Studio
    11.0\\VC\\BIN`

#.  `Download <http://www.cmake.org/files/v2.8/cmake-2.8.11.1-win32-x86.exe>`__
    and install CMake; adding it to the `PATH`

*In each step below choose to extract the package contents into the root of
this repository. 'At the command prompt, run' means use the `VS2012 x86 Native
Tools Command Prompt` to execute the commands listed, starting with the current
directory as the repository root.*

4.  `Download <http://sourceforge.net/projects/boost/files/boost/1.53.0/
    boost_1_53_0.zip/download>`__ and extract `boost_1_53_0`, then at the
    command prompt, run::

        cd boost_1_53_0
        .\bootstrap.bat
        .\b2.exe link=static runtime-link=static threading=multi ^
            --layout-tagged

#.  `Download <http://mpir.org/mpir-2.6.0.tar.bz2>`__ and extract `mpir-2.6.0`,
    then at the command prompt, run::

        cd mpir-2.6.0\win
        .\configure.bat
        .\make.bat

#.  `Download <http://www.mpfr.org/mpfr-current/mpfr-3.1.2.zip>`__ and extract
    `mpfr-3.1.2`, then at the command prompt, run::

        msbuild /p:Configuration=Release lib_mpfr.vcxproj
        del /Q Release

    to build the library and remove the object files.

#.  `Download <https://github.com/ledger/ledger/archive/master.zip>`_ and
    extract `ledger-master`

#.  `Download <http://sourceforge.net/projects/utfcpp/files/
    utf8cpp_2x/Release%202.3.4/utf8_v2_3_4.zip/download>`__ and extract
    `source` and `doc`, then at the command prompt, run::

        move source ledger-master\lib\utfcpp
        del /Q doc

    to move it into the `ledger` build tree and delete the documentation

#.  At the command prompt, run the following to build `ledger.exe`::

        cd ledger-master
        cmake ^
            -DCMAKE_BUILD_TYPE:STRING="Release" ^
            -DMPFR_LIB:FILEPATH="../../mpfr" ^
            -DGMP_LIB:FILEPATH="../../mpir-2.6.0/win/mpir" ^
            -DMPFR_PATH:PATH="../mpfr-3.1.2/src" ^
            -DGMP_PATH:PATH="../mpir-2.6.0" ^
            -DBUILD_DOCS:BOOL="0" ^
            -DHAVE_REALPATH:BOOL="0" ^
            -DHAVE_GETPWUID:BOOL="0" ^
            -DHAVE_GETPWNAM:BOOL="0" ^
            -DHAVE_ISATTY:BOOL="0" ^
            -DBOOST_ROOT:PATH="../boost_1_53_0/" ^
            -DBoost_USE_STATIC_LIBS:BOOL="1" ^
            -DCMAKE_CXX_FLAGS_RELEASE:STRING="/MT /Zi /Ob0 /Od" ^
            -G "Visual Studio 11"
        msbuild /p:Configuration=Release /p:OutDir=..\.. src\ledger.vcxproj
        del /Q ..\ledger.lib

Notes
=====

-   These instructions are based upon the `wiki page
    <https://github.com/ledger/ledger/wiki/
    Build-instructions-for-Microsoft-Visual-C---11-(2012)>`__ by Tim Crews
-   The Visual Studio project file for `mpfr` is based on the version provided
    by `Brian Gladman
    <http://gladman.plushost.co.uk/oldsite/computing/gmp4win.php>`__
-   Boost is time consuming to build, especially as we have to build all of
    the libraries to build the unit test framework; the other libraries can be
    built at the same time

Future ideas
============

-   Build tests without errors, including for example::

        msbuild /p:Configuration=Release ALL_BUILD.vcxproj

-   Build `python` bindings

-   Display Unicode output correctly on the terminal

Licenses
========

Yasm
----

::

    Libyasm is 2-clause or 3-clause BSD licensed, with the exception of
    bitvect, which is triple-licensed under the Artistic license, GPL, and
    LGPL. Libyasm is thus GPL and LGPL compatible.  In addition, this also
    means that libyasm is free for binary-only distribution as long as theterms
    of the 3-clause BSD license and Artistic license (as it applies tobitvect)
    are fulfilled.

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

utfcpp
------

::

    Copyright 2006 Nemanja Trifunovic

    Permission is hereby granted, free of charge, to any person or organization
    obtaining a copy of the software and accompanying documentation covered by
    this license (the "Software") to use, reproduce, display, distribute,
    execute, and transmit the Software, and to prepare derivative works of the
    Software, and to permit third-parties to whom the Software is furnished to
    do so, all subject to the following:

    The copyright notices in the Software and this entire statement, including
    the above license grant, this restriction and the following disclaimer,
    must be included in all copies of the Software, in whole or in part, and
    all derivative works of the Software, unless such copies or derivative
    works are solely in the form of machine-executable object code generated by
    a source language processor.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE, TITLE AND NON-INFRINGEMENT. IN NO EVENT
    SHALL THE COPYRIGHT HOLDERS OR ANYONE DISTRIBUTING THE SOFTWARE BE LIABLE
    FOR ANY DAMAGES OR OTHER LIABILITY, WHETHER IN CONTRACT, TORT OR OTHERWISE,
    ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
    DEALINGS IN THE SOFTWARE.

.. vim: ft=rst
