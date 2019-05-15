=======================
Build ledger on Windows
=======================

:Syntax checks: |drone|_
:Build: |appveyor|_

.. note::

    Licenses for software built using these instructions are listed in
    `<./licenses/README.rst>`__

Overview and versions
=====================

*These instructions assume  the ``git`` command line client is available and
on ``$PATH``.*

#.  Install `Visual Studio Community 2019 <https://www.visualstudio.com/
    downloads/>`__
#.  Install `CMake <https://cmake.org/download/>`__ 3.14.4
#.  Clone `this repository <https://github.com/maxwell-k/
    ledger-windows-build/>`__
#.  Build `Boost <http://www.boost.org/users/download/>`__ 1.70.0
#.  Build `MPIR <http://mpir.org/>`__ (master)
#.  Build `MPFR <http://www.mpfr.org/mpfr-current/#download>`__ (master)
#.  Build `ledger <http://ledger-cli.org/>`__ (master)

Detail
======

#.  `Download <https://visualstudio.microsoft.com/
    thank-you-downloading-visual-studio/?sku=Community&rel=16>`__, install
    Visual Studio Community 2019

#.  `Download <https://github.com/Kitware/CMake/releases/download/
    v3.14.4/cmake-3.14.4-win64-x64.msi>`__
    and install CMake; adding it to the `PATH`

*In the steps below 'at the command prompt' means use the `Developer
Command Prompt for VS 2019` to execute the commands listed, starting with the
current directory as the repository root.*

3.  At the command prompt run the following to clone this repository and the
    sub-modules::

        git clone https://github.com/maxwell-k/ledger-windows-build --recursive

    Use a different URL above if you are using a fork of the original
    instructions.

#.  `Download <https://dl.bintray.com/boostorg/release/1.70.0/source/
    boost_1_70_0.zip>`__ and extract ``boost_1_70_0`` to the root of this
    repository, then build Boost using the following at the command prompt::

        ren boost_1_70_0 boost
        cd boost
        .\bootstrap.bat
        .\b2.exe link=static runtime-link=static threading=multi ^
           --layout=versioned



#.  Patch build files for `mpir`:
    On lines 22 and 23 of `mpir\msvc\vs19\msbuild.bat` change `15.0` to `Current`.
    On lines 76 and 85 of `mpir\msvc\vs19\lib_mpir_gc\lib_mpir_gc.vcxproj` change `17` to `19`

#.  At the command prompt run the following to build `mpir`::

        cd mpir\msvc\vs19
        .\msbuild.bat gc LIB Win32 Release

    .. note::

        For unknown reasons, possibly due to a subtle bug in the build script
        the last command may fail on the first two attempts. It ususally works
        at the third attempt or later.

#.  At the command prompt run the following to build `mpfr`::

        cd mpfr\build.vs19\lib_mpfr
        msbuild /p:Configuration=Release lib_mpfr.vcxproj

#.  At the command prompt run the following to build ``ledger.exe``::

        cd ledger
        cmake ^
            -DCMAKE_BUILD_TYPE:STRING="Release" ^
            -DBUILD_LIBRARY=OFF ^
            -DMPFR_LIB:FILEPATH="../../mpfr/build.vs19/lib/Win32/Release/mpfr"^
            -DGMP_LIB:FILEPATH="../../mpir/lib/win32/Release/mpir" ^
            -DMPFR_PATH:PATH="../mpfr/lib/Win32/Release" ^
            -DGMP_PATH:PATH="../mpir/lib/win32/Release" ^
            -DBUILD_DOCS:BOOL="0" ^
            -DHAVE_REALPATH:BOOL="0" ^
            -DHAVE_GETPWUID:BOOL="0" ^
            -DHAVE_GETPWNAM:BOOL="0" ^
            -DHAVE_IOCTL:BOOL="0" ^
            -DHAVE_ISATTY:BOOL="0" ^
            -DBOOST_ROOT:PATH="../boost/" ^
            -DBoost_USE_STATIC_LIBS:BOOL="1" ^
            -DCMAKE_CXX_FLAGS_RELEASE:STRING="/MT /Zi /Ob0 /Od" ^
            -A Win32
            -G "Visual Studio 16"
        msbuild /p:Configuration=Release src\ledger.vcxproj
        copy Release\ledger.exe ..\

    .. note::

        The error message about not being able to find Python can be safely
        ignored. Python is only used for running tests, which is not part
        of the build process described here.


Updating to a later version of ledger, mpir or mpfr
===================================================

To build a more recent version of `ledger`, or either the `mpir` or `mpfr`
dependency, run the following at the command prompt after the initial ``git
clone`` above::

    cd ledger
    git checkout master
    cd ../mpir
    git checkout master
    cd ../mpfr
    git checkout master

.. note::

    To produce a different version or use different dependencies, you can use
    any appropriate branch or commit hash in place of ``master``. Other
    versions may require a different build process to that documented above.

Notes
=====

-   These instructions are based upon the `wiki page
    <https://github.com/ledger/ledger/wiki/
    Build-instructions-for-Microsoft-Visual-C---11-(2012)>`__ by Tim Crews.
-   Boost is time consuming to build, especially as we have to build all of
    the libraries to build the unit test framework; the other libraries can be
    built at the same time.
-   Thanks to `Andrew Savinykh <https://github.com/AndrewSav>`__ for recent
    updates.

.. |drone| image:: https://cloud.drone.io/api/badges/maxwell-k/\
        ledger-windows-build/status.svg
   :alt: Drone CI cloud build status
.. _drone: https://cloud.drone.io/maxwell-k/ledger-windows-build

.. |appveyor| image:: https://ci.appveyor.com/api/projects/status/\
        r8nsgi50ko84njvy?svg=true
    :alt: Appveyor build status
.. _appveyor: https://ci.appveyor.com/project/maxwell-k/ledger-windows-build/

.. vim: ft=rst
