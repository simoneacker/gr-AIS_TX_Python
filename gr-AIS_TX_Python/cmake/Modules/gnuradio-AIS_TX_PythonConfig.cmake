find_package(PkgConfig)

PKG_CHECK_MODULES(PC_GR_AIS_TX_PYTHON gnuradio-AIS_TX_Python)

FIND_PATH(
    GR_AIS_TX_PYTHON_INCLUDE_DIRS
    NAMES gnuradio/AIS_TX_Python/api.h
    HINTS $ENV{AIS_TX_PYTHON_DIR}/include
        ${PC_AIS_TX_PYTHON_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    GR_AIS_TX_PYTHON_LIBRARIES
    NAMES gnuradio-AIS_TX_Python
    HINTS $ENV{AIS_TX_PYTHON_DIR}/lib
        ${PC_AIS_TX_PYTHON_LIBDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/lib
          ${CMAKE_INSTALL_PREFIX}/lib64
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
          )

include("${CMAKE_CURRENT_LIST_DIR}/gnuradio-AIS_TX_PythonTarget.cmake")

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(GR_AIS_TX_PYTHON DEFAULT_MSG GR_AIS_TX_PYTHON_LIBRARIES GR_AIS_TX_PYTHON_INCLUDE_DIRS)
MARK_AS_ADVANCED(GR_AIS_TX_PYTHON_LIBRARIES GR_AIS_TX_PYTHON_INCLUDE_DIRS)
