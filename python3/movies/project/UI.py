"""
This is the top level UI for the Python Movies Project
At this level we instantiate the Central Window which has the
GUI elements.  This is also the level of handling signal/slot connections.
"""
import json
import logging

import PyQt5
import PyQt5.QtWidgets

import ORM
import UI_CentralWindow


class UI(PyQt5.QtWidgets.QMainWindow):
    """
    Top level UI class
    """

    def __init__(self, parent=None):
        super(UI, self).__init__(parent)
        # Create Main Window Elements
        self.statusBar().showMessage('Status Bar')
        self.setWindowTitle('Python Movie Project')

        # Create our central widget
        self.centralWidget = UI_CentralWindow.UI_CentralWindow()
        self.setCentralWidget(self.centralWidget)

        # Connect signals and slots
        self.centralWidget.enterMoviePushButton.clicked.connect(
            self.enterMoviePushButtonClicked)
        # Display
        self.show()

    def enterMoviePushButtonClicked(self):
        """
        Callback function for the enterMoviePushButton button object is clicked
        """

        # Read the movie title from the GUI.  This is UNSAFE data.  Never trust a USER!
        movieTitle = self.centralWidget.enterMovieLineEdit.text()
        print("Movie Title {}".format(movieTitle))

        # Query the database for all movies with this title
        movieTitleInstance = ORM.session.query(
            ORM.Movies).filter(ORM.Movies.title == movieTitle).all()

        # If no movies have this title, log it and return since we are done processing the request
        if (len(movieTitleInstance) == 0):
            logging.info("enterMoviePushButtonClicked Movie {} not in database".format(movieTitle))
            return 

        #There must be at least 1 movie with this title, look up the credits for this title.
        movieCreditsInstance = ORM.session.query(
            ORM.Credits).filter(ORM.Credits.title == movieTitle)

        # Try to get the cast and crew informatioon
        try:
            cast = json.loads(movieCreditsInstance[0].cast)
            crew = json.loads(movieCreditsInstance[0].crew)
        except:
            logging.error("enterMoviePushButtonClicked: Failed to retrieve movie or credits")
            return

        director = "NONE"
        for x in crew:
            if x['job'] == 'Director':
                director = x['name']
                
        for x in movieTitleInstance:
            print("FILM: {:20} TAGLINE: {:40} STARING {:15} DIRECTOR {:15} ".format(x.title, x.tagline, cast[0]['name'], director ))
        return
