#!/usr/bin/env python

"""
Benjmain Ziemann
benjamin.ziemann@students.olin.edu

Recieves cube struct from Kevin containing

"""

from __future__ import absolute_import
import numpy
import math
from irl.msg import Grid_Cube, Real_Cube, Real_Structure, Grid_Structure, Cube_Structures
import rospy


class CoordFrames(object):

    def __init__(self):
        #Dimensions of cubes in mm

        self.cubeHeight = 94

        #TODO
        #Camera values. GET THESE FROM FIRST YEAR DATA
        self.pixelX = [-.025, .015, .055, .095, .135]
        self.pixelY = [.580, .540, .500, .460, .420]
        self.pixelZ = [.0185, .0585, .0985, .139, .180]

        self.realX = [-177.8, -88.9, 0, 88.9, 177.8]
        self.realY = [-177.8, -88.9, 0, 88.9, 177.8]
        self.realZ = [47, 141, 237, 329, 423]

    def closest(self, values, val):
        mini = 999999
        min_index = None
        for i in range(5):
            if math.fabs(val-values[i]) < mini:
                mini = math.fabs(val-values[i])
                min_index = i
        return min_index


    def convertBoard(self, cubes):
        """
        Takes in a list of cubes structs and converts it to board model

        Called by Kevin's script for building planning
        """
        #Set Up board
        board = []

        #Add a new z layers
        for i in xrange(5):
            board.append([[None, None, None, None, None],
                            [None, None, None, None, None],
                            [None, None, None, None, None],
                            [None, None, None, None, None],
                            [None, None, None, None, None]])

        #Convert cube data to board dimensions
        #Fill out board according to cube data
        for cube in cubes.building:
            gcube = Grid_Cube()
            gcube.x = self.closest(self.pixelX, cube.x)
            gcube.y = self.closest(self.pixelY, cube.y)
            gcube.z = self.closest(self.pixelZ, cube.z)
            board[gcube.z][gcube.x][gcube.y] = gcube
        return board #3d array with x, y, and z of blocks


    def convertReal(self, cubes):
        """
        Takes in a list of cubes structs and converts it to a real board

        Called by Kevin's script for building planning
        """

        #Fill out board according to cube data
        real_cubes = Real_Structure()
        for cube in cubes.building:
            real_cube = Real_Cube()
            real_cube.x = self.realX[cube.x]
            real_cube.y = self.realY[cube.y]
            real_cube.z = self.realZ[cube.z]
            real_cubes.building.append(real_cube)
        return real_cubes

if __name__ == u"__main__":
    cf = CoordFrames()
