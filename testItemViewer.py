#!/usr/bin/env python
# -*- coding: utf-8 -*-
# generated by wxGlade 0.6.4 on Wed Jun 19 18:57:49 2013

import wx
from EveItem import *
from EveGroup import *
from EveCategory import *

from Config import *

category = []
group = []

        #=======================================================================
        # invType = EveItem(DB)
        # group = EveGroup(DB, groupName=groupName)
        # if groupName is '':
        #     invTypesList = invType.getItemsInGroup()
        # else:
        #     invTypesList = invType.getItemsInGroup(group.groupID)
        #=======================================================================

# begin wxGlade: extracode
# end wxGlade


class MyFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: MyFrame.__init__
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.lcCategory = wx.ListCtrl(self, -1, style=wx.LC_LIST | wx.LC_REPORT | wx.SUNKEN_BORDER)
        self.lcGroup = wx.ListCtrl(self, -1, style=wx.LC_REPORT | wx.SUNKEN_BORDER)
        self.lcType = wx.ListCtrl(self, -1, style=wx.LC_REPORT | wx.SUNKEN_BORDER)
        self.tcDescription = wx.TextCtrl(self, -1, "", style=wx.TE_MULTILINE)

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.onItemSelectedCategory, self.lcCategory)
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.onItemSelectedGroup, self.lcGroup)
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.onItemSelectedType, self.lcType)
        # end wxGlade

        self.lcCategory.DeleteAllColumns()
        self.lcGroup.DeleteAllColumns()
        self.lcType.DeleteAllColumns()

        self.lcCategory.InsertColumn(0, 'Category')
        self.lcCategory.SetColumnWidth(0, 200)

        category = EveInvCategory(DB)
        for cat in category.getCategories():
            self.lcCategory.Append([cat[1]])


    def __set_properties(self):
        # begin wxGlade: MyFrame.__set_properties
        self.SetTitle("Item Viewer")
        self.lcCategory.SetMinSize((191, 300))
        self.lcGroup.SetMinSize((191, 300))
        self.lcType.SetMinSize((191, 300))
        self.tcDescription.SetMinSize((578, 200))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: MyFrame.__do_layout
        sizer_2 = wx.BoxSizer(wx.VERTICAL)
        sizer_6 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_6.Add(self.lcCategory, 1, 0, 0)
        sizer_6.Add(self.lcGroup, 1, 0, 0)
        sizer_6.Add(self.lcType, 1, 0, 0)
        sizer_2.Add(sizer_6, 1, wx.EXPAND, 0)
        sizer_2.Add(self.tcDescription, 0, wx.EXPAND, 0)
        self.SetSizer(sizer_2)
        sizer_2.Fit(self)
        self.Layout()
        # end wxGlade

    def onItemSelectedCategory(self, event):  # wxGlade: MyFrame.<event_handler>
        currentCategory = event.m_itemIndex
        currentCategoryName = self.lcCategory.GetItemText(currentCategory)
        
        category = EveInvCategory(DB)
        category.getCategoryByName(currentCategoryName)

        self.lcGroup.ClearAll()
        self.lcGroup.InsertColumn(0, 'Group')
        self.lcGroup.SetColumnWidth(0, 200)

        group = EveGroup(DB)

        for gr in category.getGroupsInCategory():
            group.getGroupByID(gr[0])
            self.lcGroup.Append([group.groupName])

        event.Skip()

    def onItemSelectedGroup(self, event):  # wxGlade: MyFrame.<event_handler>
        currentGroup = event.m_itemIndex
        currentGroupName = self.lcGroup.GetItemText(currentGroup)
        
        group = EveGroup(DB)
        group.getGroupByName(currentGroupName)

        self.lcType.ClearAll()
        self.lcType.InsertColumn(0, 'Type')
        self.lcType.SetColumnWidth(0, 200)

        item = EveItem(DB)
        
        for it in group.getItemsInGroup():
            item.getItemByID(it[0])
            self.lcType.Append([item.typeName])

        event.Skip()

    def onItemSelectedType(self, event):  # wxGlade: MyFrame.<event_handler>
        currentItem = event.m_itemIndex
        currentItemName = self.lcGroup.GetItemText(currentItem)

        item = EveItem(DB)
        item.getItemByName(currentItemName)
        
        self.tcDescription.Clear()
        self.tcDescription.AppendText(item.description)
        
        event.Skip()

# end of class MyFrame
if __name__ == "__main__":
    app = wx.PySimpleApp(0)
    wx.InitAllImageHandlers()
    frame_1 = MyFrame(None, -1, "")
    app.SetTopWindow(frame_1)
    frame_1.Show()
    app.MainLoop()