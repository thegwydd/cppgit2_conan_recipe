from conans import ConanFile, CMake, tools
import os, shutil

class ConanPackage(ConanFile):
    name = "cppgit2"
    version = "0.1.0"
    description = "This is a package for cppgit2 by p-ranav on github"
    license = "MIT"  # Indicates license type of the packaged library; please use SPDX Identifiers https://spdx.org/licenses/
    url = "https://github.com/p-ranav/cppgit2"
    settings = ("os", "build_type", "arch", "compiler")
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
    }
    default_options = {
        "shared": False,
        "fPIC": True,
    }
    
    requires=[  
        "libgit2/1.3.0",
        ]

    generators = "cmake"
    cmake = None
    exports_sources = "cmake*", "lib/*", "CMakeLists.txt"

    _source_subfolder = "source_subfolder"

    # Packages the license for the conanfile.py
    exports = ["LICENSE.md"]

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        if self.options.shared:
            del self.options.fPIC
#        del self.settings.compiler.libcxx
#        del self.settings.compiler.cppstd

    def source(self):
#        self.run("git clone -b v" + self.version + " --recurse-submodules -j8 https://github.com/p-ranav/cppgit2.git")
        self.run("git clone -b v" + self.version + " https://github.com/p-ranav/cppgit2.git")

    def build(self):
        cmake = CMake(self)
        if self.options.shared:
            cmake.definitions["BUILD_SHARED"] = "TRUE"
        else:
            cmake.definitions["BUILD_STATIC"] = "TRUE"
        cmake.configure()
        cmake.build()
        
    def package(self):
        self.copy("*.h", dst="include/cppgit2", src=".", keep_path=False)
        self.copy("*.hpp", dst="include/cppgit2", src=".", keep_path=False)
        self.copy("*.lib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)
        self.copy("*.so", dst="bin", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        
    def package_info(self):
        self.cpp_info.name = "cppgit2"
#        self.cpp_info.names["generator_name"] = "<PKG_NAME>"
        self.cpp_info.includedirs = ['include']  # Ordered list of include paths
        self.cpp_info.libs = tools.collect_libs(self)  # The libs to link against
        self.cpp_info.system_libs = []  # System libs to link against
        self.cpp_info.libdirs = ['.', 'lib']  # Directories where libraries can be found
        self.cpp_info.resdirs = ['res']  # Directories where resources, data, etc. can be found
        self.cpp_info.bindirs = ['bin']  # Directories where executables and shared libs can be found
        self.cpp_info.srcdirs = []  # Directories where sources can be found (debugging, reusing sources)
        self.cpp_info.build_modules = []  # Build system utility module files
        self.cpp_info.cflags = []  # pure C flags
        self.cpp_info.cxxflags = []  # C++ compilation flags
        self.cpp_info.sharedlinkflags = []  # linker flags
        self.cpp_info.exelinkflags = []  # linker flags
        self.cpp_info.components  # Dictionary with the different components a package may have
