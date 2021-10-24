# Authors: see AUTHORS.md at project root.
# CopyPolicy: released under the terms of the LGPLv2.1, see LICENSE at project root.
# URL: https://github.com/jgvictores/master-ipr

cmake_minimum_required(VERSION 3.12 FATAL_ERROR)

project(MASTER_IPR LANGUAGES CXX)

# C/C++ compile flags.
if(CMAKE_COMPILER_IS_GNUCC OR CMAKE_COMPILER_IS_GNUCXX)
    add_compile_options(-fno-strict-aliasing -Wall)
endif()

# Add suffix for debug libraries.
if(MSVC)
    message(STATUS "Running on windows")
    set(CMAKE_DEBUG_POSTFIX "d")
endif()

# Let the user specify a configuration (only single-config generators).
if(NOT CMAKE_CONFIGURATION_TYPES)
    # Possible values.
    set(_configurations Debug Release MinSizeRel RelWithDebInfo)
    set_property(CACHE CMAKE_BUILD_TYPE PROPERTY STRINGS ${_configurations})

    foreach(_conf ${_configurations})
        set(_conf_string "${_conf_string} ${_conf}")
    endforeach()

    set_property(CACHE CMAKE_BUILD_TYPE PROPERTY HELPSTRING
                 "Choose the type of build, options are:${_conf_string}")

    if(NOT CMAKE_BUILD_TYPE)
        # Encourage the user to specify build type.
        message(STATUS "Setting build type to 'Release' as none was specified.")
        set_property(CACHE CMAKE_BUILD_TYPE PROPERTY VALUE Release)
    endif()
endif()

# Pick up our cmake modules.
list(APPEND CMAKE_MODULE_PATH ${CMAKE_SOURCE_DIR}/cmake/modules)

# Hard dependencies.
find_package(YCM 0.11 REQUIRED)
find_package(YARP 3.3 REQUIRED)

# Configure installation paths for YARP resources.
yarp_configure_external_installation(master-ipr)

# Standard installation directories.
include(GNUInstallDirs)

# Control where libraries and executables are placed during the build.
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/${CMAKE_INSTALL_BINDIR})
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/${CMAKE_INSTALL_LIBDIR})
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/${CMAKE_INSTALL_LIBDIR})

# Add main contents.
yarp_install(DIRECTORY map1 DESTINATION ${MASTER-IPR_DATA_INSTALL_DIR})
yarp_install(DIRECTORY map2 DESTINATION ${MASTER-IPR_DATA_INSTALL_DIR})
yarp_install(DIRECTORY map3 DESTINATION ${MASTER-IPR_DATA_INSTALL_DIR})
yarp_install(DIRECTORY map4 DESTINATION ${MASTER-IPR_DATA_INSTALL_DIR})
yarp_install(DIRECTORY map5 DESTINATION ${MASTER-IPR_DATA_INSTALL_DIR})
yarp_install(DIRECTORY map6 DESTINATION ${MASTER-IPR_DATA_INSTALL_DIR})
yarp_install(DIRECTORY map7 DESTINATION ${MASTER-IPR_DATA_INSTALL_DIR})
yarp_install(DIRECTORY map8 DESTINATION ${MASTER-IPR_DATA_INSTALL_DIR})
yarp_install(DIRECTORY map9 DESTINATION ${MASTER-IPR_DATA_INSTALL_DIR})
yarp_install(DIRECTORY map10 DESTINATION ${MASTER-IPR_DATA_INSTALL_DIR})
yarp_install(DIRECTORY map11 DESTINATION ${MASTER-IPR_DATA_INSTALL_DIR})
yarp_install(DIRECTORY share DESTINATION ${MASTER-IPR_DATA_INSTALL_DIR})
yarp_install(PROGRAMS src/bash/iprSim DESTINATION ${CMAKE_INSTALL_BINDIR})

# Configure and create uninstall target.
include(AddUninstallTarget)

