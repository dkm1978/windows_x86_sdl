My custom platform for PlatformIO based on https://registry.platformio.org/platforms/platformio/windows_x86 <br>
I added "Resource Hacker" to the toolchain to allow changing the icon of the compiled program.

additionally the toolchain contains UPX : the Ultimate Packer for eXecutables - https://upx.github.io/
Additional option in the platformio.ini configuration file:

custom_upx_file = false ; true | false

with this option the compiled program will be compressed using UPX.

The examplex directory contains the example program.
