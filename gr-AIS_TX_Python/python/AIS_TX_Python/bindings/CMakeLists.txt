# Copyright 2020 Free Software Foundation, Inc.
#
# This file is part of GNU Radio
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

########################################################################
# Check if there is C++ code at all
########################################################################
if(NOT AIS_TX_Python_sources)
    MESSAGE(STATUS "No C++ sources... skipping python bindings")
    return()
endif(NOT AIS_TX_Python_sources)

########################################################################
# Check for pygccxml
########################################################################
GR_PYTHON_CHECK_MODULE_RAW(
    "pygccxml"
    "import pygccxml"
    PYGCCXML_FOUND
    )

include(GrPybind)

########################################################################
# Python Bindings
########################################################################

list(APPEND AIS_TX_Python_python_files
    python_bindings.cc)

GR_PYBIND_MAKE_OOT(AIS_TX_Python
   ../../..
   gr::AIS_TX_Python
   "${AIS_TX_Python_python_files}")

# copy in bindings .so file for use in QA test module
add_custom_target(
  copy_bindings_for_tests ALL
  COMMAND
    ${CMAKE_COMMAND} -E copy "${CMAKE_CURRENT_BINARY_DIR}/*.so"
    ${CMAKE_BINARY_DIR}/test_modules/gnuradio/AIS_TX_Python/
  DEPENDS AIS_TX_Python_python)

install(TARGETS AIS_TX_Python_python DESTINATION ${GR_PYTHON_DIR}/gnuradio/AIS_TX_Python COMPONENT pythonapi)
