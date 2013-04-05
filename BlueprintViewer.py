'''
Created on 5.4.2013

@author: RIDB10157
'''

import Tkinter as tk
from Config import *
import EveDB
from EveDB import EveLists


class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master, padx=5, pady=5)

        self.master.columnconfigure(0, weight=1)
        self.grid(sticky='WENS')

        self.createWidgets()
        self.columnconfigure(2, weight=1)

        self.populateWidgets()

    def createWidgets(self):
        self.categoriesLabel = tk.Label(self, text="Categories:").grid(row=0)
        self.categoriesList = tk.Listbox(self)
#        self.countryList.bind('<<ListboxSelect>>', self.countryListClick)
#        for env in envList:
#            self.countryList.insert(tk.END, env)
        self.categoriesList.grid(row=1, column=0, rowspan=3)

        self.groupsLabel = tk.Label(self, text="Groups:").grid(row=4, column=0)
        self.groupsList = tk.Listbox(self)
        self.groupsList.grid(row=5, column=0, rowspan=3)

        self.invTypesLabel = tk.Label(self, text="Types:").grid(row=0, column=1)
        self.invTypesList = tk.Listbox(self)
        self.invTypesList.grid(row=1, column=1, rowspan=7, sticky='NSE')

    def populateWidgets(self):
        categories = EveDB.EveLists(DB)
        for cat in categories.getCategoriesList():
            self.categoriesList.insert(tk.END, cat[1])

        groups = EveDB.EveLists(DB)
        for grp in groups.getGroupsList():
            self.groupsList.insert(tk.END, grp[2])


#===============================================================================
#         self.hostNameLabel = tk.Label(self, text="Hostname:").grid(row=1, column=1)
#         self.hostNameEntry = tk.Entry(self)
#         self.hostNameEntry.grid(row=1, column=2, sticky='WE')
#
#         self.userNameLabel = tk.Label(self, text="Username:").grid(row=2, column=1)
#         self.userNameEntry = tk.Entry(self)
#         self.userNameEntry.grid(row=2, column=2, sticky='WE')
#
#         self.deployDirLabel = tk.Label(self, text="deployDir:").grid(row=3, column=1)
#         self.deployDirEntry = tk.Entry(self)
#         self.deployDirEntry.grid(row=3, column=2, sticky='WE')
#
#         self.startButton = tk.Button(self, text='Start', command=self.startPreDeployer)
#         self.startButton.grid(row=4, column=2)
#===============================================================================


def main():
    app = Application()
    app.master.title('Eve Online Blueprint Viewer')
    app.mainloop()

if __name__ == '__main__':
    main()
