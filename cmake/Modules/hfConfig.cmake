INCLUDE(FindPkgConfig)
PKG_CHECK_MODULES(PC_HF hf)

FIND_PATH(
    HF_INCLUDE_DIRS
    NAMES hf/api.h
    HINTS $ENV{HF_DIR}/include
        ${PC_HF_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    HF_LIBRARIES
    NAMES gnuradio-hf
    HINTS $ENV{HF_DIR}/lib
        ${PC_HF_LIBDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/lib
          ${CMAKE_INSTALL_PREFIX}/lib64
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
)

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(HF DEFAULT_MSG HF_LIBRARIES HF_INCLUDE_DIRS)
MARK_AS_ADVANCED(HF_LIBRARIES HF_INCLUDE_DIRS)

