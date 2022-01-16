project(cppgit2)
cmake_minimum_required(VERSION 3.8)

set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)

include(CMakePackageConfigHelpers)

if(EXISTS ${CMAKE_CURRENT_BINARY_DIR}/conanbuildinfo_multi.cmake)
    include(${CMAKE_CURRENT_BINARY_DIR}/conanbuildinfo_multi.cmake)
    conan_basic_setup()
else()
    include(${CMAKE_CURRENT_BINARY_DIR}/conanbuildinfo.cmake)
    conan_basic_setup(NO_OUTPUT_DIRS)
endif()

# Sources for cppgit2
file(GLOB CPPGIT2_SOURCES "cppgit2/src/*.cpp")
file(GLOB CPPGIT2_HEADERS "cppgit2/include/cppgit2/*.hpp")

# Version information
set(CPPGIT2_VERSION_MAJOR 0)
set(CPPGIT2_VERSION_MINOR 1)
set(CPPGIT2_VERSION_REV 0)
set(CPPGIT2_VERSION_STRING "${CPPGIT2_VERSION_MAJOR}.${CPPGIT2_VERSION_MINOR}.${CPPGIT2_VERSION_REV}")

# Build shared library
if (BUILD_SHARED)
    message("<<<<<< BUILDING SHARED VERSION >>>>>>")
    add_library(CPPGIT2_SHARED SHARED ${CPPGIT2_SOURCES} ${CPPGIT2_HEADERS})
    target_include_directories(CPPGIT2_SHARED PUBLIC "cppgit2/include")
    set_target_properties(CPPGIT2_SHARED PROPERTIES 
        OUTPUT_NAME cppgit2
        POSITION_INDEPENDENT_CODE 1
        )
    set_target_properties(CPPGIT2_SHARED PROPERTIES VERSION ${CPPGIT2_VERSION_STRING} SOVERSION ${CPPGIT2_VERSION_MINOR})
    set_target_properties(CPPGIT2_SHARED PROPERTIES CXX_STANDARD 11)
    target_link_libraries(CPPGIT2_SHARED git2)
    if (CMAKE_CXX_COMPILER_ID STREQUAL "MSVC")
        target_compile_definitions(CPPGIT2_SHARED PRIVATE -D_CRT_SECURE_NO_WARNINGS)
    endif()
    conan_target_link_libraries(CPPGIT2_SHARED)
endif()

# Build static library
if (BUILD_STATIC)
    message("<<<<<< BUILDING STATIC VERSION >>>>>>")
    add_library(CPPGIT2_STATIC STATIC ${CPPGIT2_SOURCES} ${CPPGIT2_HEADERS})
    target_include_directories(CPPGIT2_STATIC PUBLIC "cppgit2/include")
    set_target_properties(CPPGIT2_STATIC PROPERTIES OUTPUT_NAME cppgit2)
    set_target_properties(CPPGIT2_STATIC PROPERTIES CXX_STANDARD 11)
    target_link_libraries(CPPGIT2_STATIC git2)
    if (CMAKE_CXX_COMPILER_ID STREQUAL "MSVC")
        target_compile_definitions(CPPGIT2_STATIC PRIVATE -D_CRT_SECURE_NO_WARNINGS)
    endif()
    conan_target_link_libraries(CPPGIT2_STATIC)
endif()



