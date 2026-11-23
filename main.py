import os
import os.path
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QDockWidget, QMainWindow

## Nom du fichier contenant les secteurs
SECTEUR_FILE="secteurs.txt" # "secteur.csv"

## Nom des vols
VOLS_FILE = "vols.txt"


def main():
    """Main function."""
    # Load files

    pln_file = os.path.join(data_dir, PLN_FILE)


    ## Traffic considered for simulation
    

    # Create the simulation
    ## Initial simulation 
    
    # Initialize Qt
    ## Main application
    app = QApplication(sys.argv)

    # Create the radar view and the time navigation interface
    rad = RadarView(sim)
    # Create the QMainWindow to hold radar view
    win = QMainWindow()
   
    win.setCentralWidget(rad)
    # The QMainWindow is the root widget of this QApplication, so it must be explicitly shown...
    win.showMaximized()  # application en full screen

    # Enter the main loop
    app.exec()


if __name__ == "__main__":
    main()

