from conans import ConanFile, MSBuild, tools
from shutil import copyfile
import os

class LuaConan(ConanFile):
    name = "lua"
    license = "MIT"
    description = "Lua conan package"
    url = "https://www.lua.org/home.html"

    # Settings and options
    settings = "os", "compiler", "arch"

    options = { "shared": [True, False] }
    default_options = { "shared":True }

    # Additional files to export
    exports_sources = ["premake5.lua"]

    # Iceshard conan tools
    python_requires = "conan-iceshard-tools/0.6.0@iceshard/dev"
    python_requires_extend = "conan-iceshard-tools.IceTools"

    # Initialize the package
    def init(self):
        self.ice_init("premake5")
        self.build_requires = self._ice.build_requires

    # Build both the debug and release builds
    def ice_build(self):
        copyfile("../premake5.lua", "premake5.lua")
        self.ice_generate()

        if self.settings.compiler == "Visual Studio":
            self.ice_build_msbuild("Lua.sln", ["Debug", "Release"])

        else:
            self.ice_build_make(["Debug", "Release"])

    def package(self):

        self.copy("COPYRIGHT", src=self._ice.out_dir, dst="LICENSE")

        # header files
        self.copy("*.hpp", "include", src="{}/etc".format(self._ice.out_dir), keep_path=False)
        for include in ["lua.h", "lualib.h", "lauxlib.h", "luaconf.h"]:
            self.copy(include, "include", src="{}/src".format(self._ice.out_dir), keep_path=False)

        # binaries
        build_dir = os.path.join(self._ice.out_dir, "bin")
        if self.settings.os == "Windows":
            self.copy("*.exe", "bin", build_dir, keep_path=True)
            self.copy("*.lib", "lib", build_dir, keep_path=True)
            if self.options.shared:
                self.copy("*.dll", "bin", build_dir, keep_path=True)
                self.copy("*.pdb", "bin", build_dir, keep_path=True)
            else:
                self.copy("*.pdb", "lib", build_dir, keep_path=True)
        if self.settings.os == "Linux":
            for config in ["Debug", "Release"]:
                self.copy("lua", "bin/{}".format(config), os.path.join(build_dir, config), keep_path=True)
                self.copy("luac", "bin/{}".format(config), os.path.join(build_dir, config), keep_path=True)
            self.copy("*.a", "lib", build_dir, keep_path=True)
            if self.options.shared:
                self.copy("*.so", "bin", build_dir, keep_path=True)


    def package_info(self):
        self.cpp_info.debug.libdirs = [ "lib/Debug" ]
        self.cpp_info.release.libdirs = [ "lib/Release" ]
        self.cpp_info.bindirs = [ "bin/Release" ]
        self.cpp_info.libdirs = []
        self.cpp_info.libs = [ "lua51" ]

        # Enviroment info
        self.env_info.path.append(os.path.join(self.package_folder, "bin/Release"))
