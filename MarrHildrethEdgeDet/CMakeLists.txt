cmake_minimum_required(VERSION 3.0.0)
project( MarrHildreth )
find_package( OpenCV REQUIRED )
include_directories( ${OpenCV_INCLUDE_DIRS} )
add_executable( MarrHildreth MarrHildrethEdgeDet.cpp )
target_link_libraries( MarrHildreth ${OpenCV_LIBS} )
