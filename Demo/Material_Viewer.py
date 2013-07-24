#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# generated by wxGlade 0.6.7 (standalone edition) on Tue Jul 23 21:15:22 2013
#

import wx

from Config import *
from EveModules.EveCategory import *
from EveModules.EveGroup import *
from EveModules.EveItem import *
from EveModules.EveBlueprint import *

# begin wxGlade: dependencies
import gettext
# end wxGlade

# begin wxGlade: extracode
# end wxGlade


class MyFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: MyFrame.__init__
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.tree_ctrl_Items = wx.TreeCtrl(self, wx.ID_ANY, style=wx.TR_HAS_BUTTONS | wx.TR_LINES_AT_ROOT | wx.TR_DEFAULT_STYLE | wx.SUNKEN_BORDER)
        self.list_ctrl_Materials = wx.ListCtrl(self, wx.ID_ANY, style=wx.LC_REPORT | wx.SUNKEN_BORDER)

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_TREE_SEL_CHANGED, self.itemSelChanged, self.tree_ctrl_Items)
        # end wxGlade

        rootTree = self.tree_ctrl_Items.AddRoot('Item list')

        category = EveCategory(DB)
        for cat in category.getCategories():
            catTree = self.tree_ctrl_Items.AppendItem(rootTree, cat[1])

            group = EveGroup(DB)
            for grp in group.getGroups(cat[0]):
                grpTree = self.tree_ctrl_Items.AppendItem(catTree, grp[2])
            
                item = EveItem(DB)
                for itm in item.getItems(grp[0]):
                    itmTree = self.tree_ctrl_Items.AppendItem(grpTree, itm[2])

        self.tree_ctrl_Items.Expand(rootTree)

        self.__set_properties()
        self.__do_layout()

    def __set_properties(self):
        # begin wxGlade: MyFrame.__set_properties
        self.SetTitle(_("frame_1"))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: MyFrame.__do_layout
        sizer_1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_1.Add(self.tree_ctrl_Items, 1, wx.EXPAND, 0)
        sizer_1.Add(self.list_ctrl_Materials, 1, wx.EXPAND, 0)
        self.SetSizer(sizer_1)
        sizer_1.Fit(self)
        self.Layout()
        # end wxGlade

    def itemSelChanged(self, event):  # wxGlade: MyFrame.<event_handler>
        self.list_ctrl_Materials.ClearAll()
        self.list_ctrl_Materials.InsertColumn(0, 'Material')
        self.list_ctrl_Materials.InsertColumn(1, 'Quantity')

        if not self.tree_ctrl_Items.ItemHasChildren(event.Item):
            item = EveItem(DB, name=self.tree_ctrl_Items.GetItemText(event.Item))
            bp = item.getBlueprintObject()
            materialList = bp.getManufacturingMaterials(characterSkillLevelME=5)
            for material in materialList:
                matItem = EveItem(DB, itemID=material[0])
                matQuant = material[1]
                self.list_ctrl_Materials.Append([matItem.name, matQuant])
                
        event.Skip()
# end of class MyFrame

if __name__ == "__main__":
    gettext.install("app") # replace with the appropriate catalog name

    app = wx.PySimpleApp(0)
    wx.InitAllImageHandlers()
    MainFrame = MyFrame(None, wx.ID_ANY, "")
    app.SetTopWindow(MainFrame)
    MainFrame.Show()
    app.MainLoop()
    