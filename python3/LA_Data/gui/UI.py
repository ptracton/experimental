
import json
import sqlalchemy
import sqlalchemy.ext.declarative
import sqlalchemy.orm

import PyQt5
import PyQt5.QtWidgets
import UI_CentralWidget

import ORM
import LACityData
import NYCityData
import ChicagoCityData
import tools


class UI(PyQt5.QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        """
        """

        super(UI, self).__init__(parent)

        Session = sqlalchemy.orm.sessionmaker(ORM.db)
        self.session = Session()
        ORM.base.metadata.create_all(ORM.db)

        exitAction = PyQt5.QtWidgets.QAction(
            PyQt5.QtGui.QIcon('src/application-exit.png'),
            '&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(PyQt5.QtWidgets.qApp.quit)
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAction)

        aboutAction = PyQt5.QtWidgets.QAction('&About', self)
        helpMenu = menubar.addMenu('&Help')
        helpMenu.addAction(aboutAction)

        self.central = UI_CentralWidget.UI_CentralWidget()
        self.central.CityComboBox.currentIndexChanged.connect(
            self.CityComboBoxCurrentIndexChanged)
        self.central.DataSelectionComboBox.currentIndexChanged.connect(
            self.DataSelectionComboBoxCurrentIndexChanged)
        self.central.GetDataButton.clicked.connect(
            self.GetDataPushButtonClicked)

        self.setCentralWidget(self.central)
        self.statusBar().showMessage('Status Bar')
        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('QT GUI and Stuff')
        self.show()

    def CityComboBoxCurrentIndexChanged(self, selection):
        #print(selection)
        #print(self.central.CityComboBox.currentText())
        return

    def DataSelectionComboBoxCurrentIndexChanged(self, selection):
        #print(selection)
        #print(self.central.DataSelectionComboBox.currentText())
        return

    def GetDataPushButtonClicked(self):
        #print("Button Pushed")
        city = self.central.CityComboBox.currentText()
        database = self.central.DataSelectionComboBox.currentText()
        #print("City {} Database {}".format(city, database))

        if city == 'Los Angeles':
            self.statusBar().showMessage('Getting LA Data')
            LALibraryBranches = LACityData.LACityData('a4nt-4gca')
            LALibraryBranches.get_data()
            #print(LALibraryBranches.data)
            for library in LALibraryBranches.data:
                branch = ORM.LALibraryBranches()
                branch.BranchName = library['branch_name']
                branch.PhoneNumber = library['phone_number']
                branch.Email = library['email']
                branch.CouncilDistrict = library['council_district']
                human_address = json.loads(library['location']['human_address'])
                branch.Address = human_address['address']
                branch.City = human_address['city']
                branch.State = human_address['state']
                branch.Zip = human_address['zip']
                try:
                    self.session.add(branch)
                    self.session.commit()
                except:
                    print("Failed On {}".format(library['branch_name']))
                    self.session.rollback()
                del (branch)
        
            self.statusBar().showMessage('Done LA Data')

        if city == 'Queens':
            self.statusBar().showMessage('Getting Queens Data')
            QueensLibraryBranches = NYCityData.NYCityData('swsf-ed7j')
            QueensLibraryBranches.get_data()
            for library in QueensLibraryBranches.data:
                branch = ORM.QueensLibraryBranches()
                branch.BranchName = library['name']
                branch.PhoneNumber = library['phone']
                branch.Address = library['address']
                branch.City = library['city']
                branch.Zip = library['postcode']
                branch.Burough = library['borough']
                try:
                    branch.CommunityCouncil = library['community_council']
                except:
                    branch.CommunityCouncil = 0
                    
                try:
                    self.session.add(branch)
                    self.session.commit()
                except:
                    self.session.rollback()
                del (branch)                

                #print(tools.remove_non_ascii(library['name'].encode('utf-8')))
            self.statusBar().showMessage('Done Queens Data')

        if city == 'Chicago':
            self.statusBar().showMessage('Getting Chicago Data')
            ChicagoLibraryBranches = ChicagoCityData.ChcagoCityData('x8fc-8rcq')
            ChicagoLibraryBranches.get_data()
            #print(ChicagoLibraryBranches.data)
            for library in ChicagoLibraryBranches.data:
                branch = ORM.ChicagoLibraryBranches()
                branch.BranchName = library['name_']
                branch.PhoneNumber = library['phone']
                branch.Address = library['address']
                branch.City = library['city']
                branch.Zip = library['zip']
                branch.Website = library['website']['url']
                try:
                    self.session.add(branch)
                    self.session.commit()
                except:
                    print("Chicago Failed {} ".format(library))
                    self.session.rollback()
                del(branch)
                
            self.statusBar().showMessage('Done Chicago Data')
            

        return
