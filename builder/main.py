# Copyright 2014-present PlatformIO <contact@platformio.org>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
    Builder for Windows x86 / 32bit + SDL2
"""
import os,subprocess

from pathlib import Path
from SCons.Script import AlwaysBuild, Default, DefaultEnvironment
from platformio.util import get_systype

env = DefaultEnvironment()

env.Replace(
    _BINPREFIX="",
    AR="${_BINPREFIX}ar",
    AS="${_BINPREFIX}as",
    CC="${_BINPREFIX}gcc",
    CXX="${_BINPREFIX}g++",
    GDB="${_BINPREFIX}gdb",
    OBJCOPY="${_BINPREFIX}objcopy",
    RANLIB="${_BINPREFIX}ranlib",
    SIZETOOL="${_BINPREFIX}size",

    SIZEPRINTCMD='$SIZETOOL $SOURCES',
    PROGSUFFIX=".exe"
)

env.Append(
    CXXFLAGS=[
        "-std=c++14"
        ],
    CCFLAGS=[
        "-std=c++14"
        ],
    LINKFLAGS=[
        "-static",
        "-static-libgcc",
        "-static-libstdc++",
        "-Llib",
        "-lmingw32",
        "-lSDL2main",
        "-lSDL2",
        "-lm",
        "-ldinput8",
        "-ldxguid",
        "-ldxerr8",
        "-luser32",
        "-lgdi32",
        "-lwinmm",
        "-limm32",
        "-lole32",
        "-loleaut32",
        "-lshell32",
        "-lsetupapi",
        "-lversion",
        "-luuid"
    ]
)

if get_systype() == "darwin_x86_64":
    env.Replace(
        _BINPREFIX="i586-mingw32-"
    )
elif get_systype() in ("linux_x86_64", "linux_i686"):
    env.Replace(
        _BINPREFIX="i686-w64-mingw32-"
    )


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    UP = '\033[1A'

def post_program_action(source, target, env): 
    
    if os.path.exists("binary")==False:os.mkdir("binary", 0o666)
    objdump="@copy "
    src_elf=env.subst("\"${BUILD_DIR}\\${PROGNAME}.exe\"")
    new_name=os.path.basename(os.path.normpath(env.subst('${PROJECT_DIR}'))).strip()
    cmd=objdump+src_elf+" \"${PROJECT_DIR}\\binary\\"+new_name+".exe\" > nul"  
    env.Execute(cmd)
    objdump="@del "
    src_elf=env.subst("\"${BUILD_DIR}\\${PROGNAME}.exe\"")
    cmd=" ".join([objdump,src_elf])  
    env.Execute(cmd)
    print("\n"+bcolors.OKGREEN+"Adding icon resource...",end="")
    polecenie=env.subst("@rh.exe -open \"${PROJECT_DIR}\\binary\\"+new_name+".exe\" -save \"${PROJECT_DIR}\\binary\\"+new_name+".exe\" -resource \"dafault.ico\" -mask ICONGROUP,MAINICON, -action addoverwrite -log NUL")
    process = subprocess.Popen(polecenie, shell=True, stdout=subprocess.PIPE)
    process.wait()
    print("DONE.")
    try:
        paker = env.GetProjectOption("custom_upx_file")
    except: 
        paker=""
    if paker=="true" or paker=="True":
      print(bcolors.OKCYAN+"Crunching..."),
      polecenie=env.subst("@upx.exe -f -q \"${PROJECT_DIR}\\binary\\"+new_name+".exe\"")
      process = subprocess.Popen(polecenie, shell=True, stdout=subprocess.PIPE)
      process.wait()
      print(bcolors.OKCYAN+bcolors.UP+"Crunching...DONE.")
      
    os.chdir("binary")
    print(bcolors.HEADER+"Starting application:\n")
    polecenie=env.subst("@"+new_name+".exe")
    process = subprocess.Popen(polecenie, shell=True, stdout=subprocess.PIPE)
    process.wait()
    print("\n"+bcolors.OKBLUE+"Application ended.\n\n")

env.AddPostAction("$BUILD_DIR/program.exe", post_program_action)

#
# Target: Build executable program
#

target_bin = env.BuildProgram()

#
# Target: Print binary size
#

target_size = env.Alias("size", target_bin, env.VerboseAction(
    "$SIZEPRINTCMD", "Calculating size $SOURCE"))
AlwaysBuild(target_size)


#
# Default targets
#

Default([target_bin])




