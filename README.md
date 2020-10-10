# wilson
Wilson's Algorithm for maze making implemented in Python and intended for use in a 3D Minecraft maze.
https://en.wikipedia.org/wiki/Maze_generation_algorithm#Wilson's_algorithm
I have found an implementation in Ruby here: http://weblog.jamisbuck.org/2011/1/20/maze-generation-wilson-s-algorithm

The program is a command line tool that takes 4 arguments, the x, y, and z dimensions of the maze space, and the name of the outfile.csv
Usage example:
  python wilson.py 5 5 5 fivecellmaze.csv
This will not create a 5x5x5 object, but use 125 cells to create the maze, with wall blocks in-between cells.
The output csv file gives a floor-by-floor schematic of X's and O's, X's being walls and O's being open spaces, from the bottom of the maze to the top.

This is not a very efficient implementation, but it works so far as I can tell, pending an actual construction in Minecraft.
