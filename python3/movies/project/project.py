#! /usr/bin/env python3

import logging
import sys

import PyQt5

import ORM
import UI

if __name__ == "__main__":

    logging.basicConfig(filename="movie_project.log",
                        level=logging.DEBUG,
                        format='%(asctime)s,%(levelname)s,%(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p')
    
    logging.info("Program Starting")

    # These are the file unzipped from https://www.kaggle.com/tmdb/tmdb-movie-metadata/data
    moviesCSVFile = "../tmdb-5000-movie-dataset/tmdb_5000_movies.csv"
    creditsCSVFile = "../tmdb-5000-movie-dataset/tmdb_5000_credits.csv"

    # If the tables do not exist, create them
    if not ORM.tableExists(ORM.inspector, "Movies"):
        ORM.csvToTable(moviesCSVFile, tableName="Movies", db=ORM.db)

    if not ORM.tableExists(ORM.inspector, "Credits"):
        ORM.csvToTable(creditsCSVFile, tableName="Credits", db=ORM.db)


    app = PyQt5.QtWidgets.QApplication(sys.argv)
    gui = UI.UI()
    gui.show()
    app.exec_()

        
    # All done, log it and exit
    logging.info("Program Terminated")
    sys.exit(0)
