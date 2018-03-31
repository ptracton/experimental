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
            PyQt5.QtGui.QIcon('src/application-exit.png'), '&Exit', self)
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
        self.central.GetDataButton.clicked.connect(
            self.GetDataPushButtonClicked)
        self.central.ViewDataButton.clicked.connect(
            self.ViewDataPushButtonClicked)

        self.setCentralWidget(self.central)
        self.statusBar().showMessage('Status Bar')
        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('QT GUI and Stuff')
        self.show()

    def ViewDataPushButtonClicked(self):
        city = self.central.CityComboBox.currentText()
        database = self.central.DataSelectionComboBox.currentText()
        validCity = False

        if city == 'Los Angeles':
            validCity = True
            columns = ORM.LALibraryBranches.__table__.columns.keys()
            query = self.session.query(ORM.LALibraryBranches).all()

        if city == 'Queens':
            validCity = True
            columns = ORM.QueensLibraryBranches.__table__.columns.keys()
            query = self.session.query(ORM.QueensLibraryBranches).all()

        if city == "Chicago":
            validCity = True
            columns = ORM.ChicagoLibraryBranches.__table__.columns.keys()
            query = self.session.query(ORM.ChicagoLibraryBranches).all()

        self.central.TableWidget.setColumnCount(len(columns))
        self.central.TableWidget.setVerticalHeaderLabels(["H1"])
        print(columns)

        self.central.TableWidget.setHorizontalHeaderLabels(columns)
        self.central.TableWidget.setRowCount(len(query))
        self.central.TableWidget.setColumnCount(len(columns))
        
        row = 0
        for x in query:
            print("ROW {} Branch {} PhoneNumber {} Email {} Council {} Adresss {} City {} State {} Zip {}".format(row, x.BranchName, x.PhoneNumber, x.Email, x.CouncilDistrict, x.Address, x.City, x.State, x.Zip))
            
            self.central.TableWidget.setItem(row, 0, PyQt5.QtWidgets.QTableWidgetItem(x.BranchName))
            self.central.TableWidget.setItem(row, 1, PyQt5.QtWidgets.QTableWidgetItem(x.PhoneNumber))
            self.central.TableWidget.setItem(row, 2, PyQt5.QtWidgets.QTableWidgetItem(x.Email))
            self.central.TableWidget.setItem(row, 3, PyQt5.QtWidgets.QTableWidgetItem(x.CouncilDistrict))
            self.central.TableWidget.setItem(row, 4, PyQt5.QtWidgets.QTableWidgetItem(x.Address))
            self.central.TableWidget.setItem(row, 5, PyQt5.QtWidgets.QTableWidgetItem(x.City))
            self.central.TableWidget.setItem(row, 6, PyQt5.QtWidgets.QTableWidgetItem(x.State))
            self.central.TableWidget.setItem(row, 7, PyQt5.QtWidgets.QTableWidgetItem(x.Zip))
            
            
            row = row + 1
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
                human_address = json.loads(
                    library['location']['human_address'])
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
            ChicagoLibraryBranches = ChicagoCityData.ChcagoCityData(
                'x8fc-8rcq')
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
                del (branch)

            self.statusBar().showMessage('Done Chicago Data')

        return
