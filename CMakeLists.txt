project(wasm-setjmp C CXX)
cmake_minimum_required(VERSION 2.8.7)
enable_testing()

if(NOT CMAKE_BUILD_TYPE)
  message(STATUS "No build type selected, default to Release")
  set(CMAKE_BUILD_TYPE "Release")
endif()
string(TOUPPER "${CMAKE_BUILD_TYPE}" uppercase_CMAKE_BUILD_TYPE)
if(CMAKE_BUILD_TYPE AND
    NOT uppercase_CMAKE_BUILD_TYPE MATCHES "^(DEBUG|RELEASE)$")
  message(FATAL_ERROR "Invalid value for CMAKE_BUILD_TYPE: ${CMAKE_BUILD_TYPE}")
endif()

# Support functionality.

function(ADD_COMPILE_FLAG value)
  message(STATUS "Building with ${value}")
  foreach(variable CMAKE_C_FLAGS CMAKE_CXX_FLAGS)
    set(${variable} "${${variable}} ${value}" PARENT_SCOPE)
  endforeach(variable)
endfunction()

function(ADD_LINK_FLAG value)
  message(STATUS "Linking with ${value}")
  foreach(variable CMAKE_EXE_LINKER_FLAGS)
    set(${variable} "${${variable}} ${value}" PARENT_SCOPE)
  endforeach(variable)
endfunction()

add_compile_flag("-Wall")
add_compile_flag("-Werror")
add_compile_flag("-Wextra")
add_compile_flag("-Wno-unused-parameter")
add_compile_flag("-fno-omit-frame-pointer")
if(uppercase_CMAKE_BUILD_TYPE STREQUAL "DEBUG")
  add_compile_flag("-O0")
  add_compile_flag("-g3")
else()
  add_compile_flag("-O2")
endif()

# clang doesn't print colored diagnostics when invoked from Ninja.
if(UNIX AND
   CMAKE_CXX_COMPILER_ID STREQUAL "Clang" AND
   CMAKE_GENERATOR STREQUAL "Ninja")
  add_compile_flag("-fcolor-diagnostics")
endif()

# Tests.

file(GLOB tests "test/*.cc")
foreach(test ${tests})
  string(REGEX REPLACE ".*test/([-a-zA-Z0-9_]+).cc$" "\\1" name "${test}")
  add_executable(test_${name} ${test})
  add_test(
    NAME ${name}
    COMMAND ${CMAKE_SOURCE_DIR}/tools/check-output.py
            --program ${CMAKE_BINARY_DIR}/test_${name}
	    --gold ${CMAKE_SOURCE_DIR}/test/${name}.out
    )
endforeach()
