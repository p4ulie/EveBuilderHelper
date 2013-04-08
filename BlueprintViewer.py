'''
Created on 5.4.2013

@author: RIDB10157
'''

import Tkinter as tk
from Config import *
from EveInvType import *
from EveInvGroup import *
from EveInvCategory import *


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
        self.categoriesList.bind('<<ListboxSelect>>', self.categoriesListClick)
        self.categoriesList.grid(row=1, column=0, rowspan=3)

        self.groupsLabel = tk.Label(self, text="Groups:").grid(row=4, column=0)
        self.groupsList = tk.Listbox(self)
        self.groupsList.bind('<<ListboxSelect>>', self.groupsListClick)
        self.groupsList.grid(row=5, column=0, rowspan=3)

        self.invTypesLabel = tk.Label(self, text="Types:").grid(row=0, column=1)
        self.invTypesList = tk.Listbox(self)
        self.invTypesList.grid(row=1, column=1, rowspan=7, columnspan=30, sticky='NSE')

    def categoriesListClick(self, evt):
        # Note here that Tkinter passes an event object to onselect()
        w = evt.widget
        index = int(w.curselection()[0])
        value = w.get(index)
        self.populateGroupsList(value)
        self.populateInvTypesList(self.groupsList.get(0))

    def groupsListClick(self, evt):
        # Note here that Tkinter passes an event object to onselect()
        w = evt.widget
        index = int(w.curselection()[0])
        value = w.get(index)
        self.populateInvTypesList(value)

    def populateCategoriesList(self):
        category = EveInvCategory(DB)
        for cat in category.getInvCategoriesList():
            self.categoriesList.insert(tk.END, cat[1])

    def populateGroupsList(self, categoryName=''):
        group = EveInvGroup(DB)
        category = EveInvCategory(DB)
        if categoryName is '':
            groupsList = group.getInvGroupsList()
        else:
            category.getInvCategoryByName(categoryName)
            groupsList = group.getInvGroupsList(category.categoryID)
        self.groupsList.delete(0, tk.END)
        for grp in groupsList:
            self.groupsList.insert(tk.END, grp[2])

    def populateInvTypesList(self, groupName=''):
        invType = EveInvType(DB)
        group = EveInvGroup(DB, groupName=groupName)
        if groupName is '':
            invTypesList = invType.getInvTypesList()
        else:
            invTypesList = invType.getInvTypesList(group.groupID)
        self.invTypesList.delete(0, tk.END)
        for iT in invTypesList:
            self.invTypesList.insert(tk.END, iT[2])

    def populateWidgets(self):
        self.populateCategoriesList()
        self.populateGroupsList(self.categoriesList.get(0))
        self.populateInvTypesList(self.groupsList.get(0))


def main():
    app = Application()
    app.master.title('Eve Online Blueprint Viewer')
    app.mainloop()

if __name__ == '__main__':
    main()
