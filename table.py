from java.lang import Object
from javax.swing.table import AbstractTableModel

#from swingutils.models.list import AbstractDelegateList
#from swingutils.beans import MirrorObject
#from swingutils.events import addListSelectionListener, addPropertyListener

from java.awt import Component, GridLayout
from java.awt.event import ActionListener, ActionEvent
from java.lang import Runnable
from java.net import URL
from java.util import Collection,HashSet,LinkedList,List,Set
from javax.swing import *
from org.openstreetmap.josm import Main
from org.openstreetmap.josm.data.osm import *;
from org.openstreetmap.josm.data.validation import *;
from org.openstreetmap.josm.tools import *;
from org.openstreetmap.josm.tools.I18n.tr import *
import org.openstreetmap.josm.Main as Main
import org.openstreetmap.josm.command as Command
import org.openstreetmap.josm.data.osm.DataSet as DataSet
import org.openstreetmap.josm.data.osm.Node as Node
import org.openstreetmap.josm.data.osm.TagCollection as TagCollection
import org.openstreetmap.josm.data.osm.Way as Way
import org.openstreetmap.josm.data.osm.BBox as BBox

import org.openstreetmap.josm.data.coor.LatLon as LatLon
import time
from org.openstreetmap.josm.data import Preferences;
from javax.swing import *
from java.awt import *
from javax.swing.table import DefaultTableModel


class ObjectTableModel(AbstractTableModel):
    __columns__ = ()

    def __init__(self, delegate, columns):
        AbstractTableModel.__init__(self)
        self.__columns__ = columns
        self.delegate= delegate
        self._getters = [None] * len(self.__columns__)
        for index, column in enumerate(self.__columns__):
            self.__columns__[index] = self._validateColumn(column, index)

    def _fireItemsChanged(self, start, end):
        self.fireTableRowsUpdated(start, end)

    def _fireItemsAdded(self, start, end):
        self.fireTableRowsInserted(start, end)

    def _fireItemsRemoved(self, start, end):
        self.fireTableRowsDeleted(start, end)
    
    def setDelegate(self, value):
        self._delegate = value
        self.fireTableDataChanged()

    def getColumnCount(self):
        return len(self.__columns__)

    def getRowCount(self):
        n= len(self.delegate)
        return n


    def getColumnClass(self, columnIndex):
        return basestring
#        return self.__columns__[columnIndex][1]

    def getColumnName(self, columnIndex):
        return self.__columns__[columnIndex][0]

    def setValueAt(self, aValue, rowIndex, columnIndex):
        self[rowIndex][columnIndex] = aValue

    def refresh(self):
        """
        Forces a visual refresh for all rows on related tables.
        Use this method to visually update tables after you have done changes
        that did not fire the appropriate table events.

        """
        if len(self) > 0:
            self.fireTableRowsUpdated(0, len(self) - 1)

    def _validateColumn(self, column, index):
        #column = DelegateTableModel._validateColumn(self, column, index)
        self._getters[index] = lambda row: row.get(column[2])
        return column

    def getValueAt(self, rowIndex, columnIndex):
        #line = self.delegate[rowIndex]
        return self.delegate[rowIndex].get(self.__columns__[columnIndex][1])
        #return self._getters[columnIndex](line)

    def setValueAt(self, aValue, rowIndex, columnIndex):
        attrname = self.__columns__[columnIndex][2]
        setattr(self[rowIndex], attrname, aValue)
        self.fireTableCellUpdated(rowIndex, columnIndex)


    def getObjectIndex(self, obj):
        """
        Returns the row number that contains the object that is equal
        to the given object.

        :return: the row number, or -1 if no match was found

        """
        for i, row in enumerate(self):
            if row == obj:
                return i
        return - 1

    def getSelectedObject(self, table):
        """
        Returns the selected object, or first selected object if the table has
        multi-row selection enabled.

        """
        assert table.model is self
        if table.selectedRow >= 0:
            modelRow = table.convertRowIndexToModel(table.selectedRow)
            return self[modelRow]

    def getSelectedObjects(self, table):
        """
        Returns objects that have been selected in the given table.
        This table model must be the given table's model.

        :return: objects that were selected in the given table
        :rtype: list

        """
        assert table.model is self
        selected = []
        for viewRow in table.selectedRows:
            modelRow = table.convertRowIndexToModel(viewRow)
            selected.append(self[modelRow])
        return selected

    def getVisibleObjects(self, table):
        """
        Returns objects not hidden by any table filters.
        This table model must be the given table's model.

        :return: objects that were visible in the given table
        :rtype: list

        """
        assert table.model is self
        visible = []
        for viewRow in xrange(table.rowCount):
            modelRow = table.convertRowIndexToModel(viewRow)
            visible.append(self[modelRow])
        return visible


def DisplayTable (collection):

    columns=list(
        (
            ("Street","addr:street"),
            ("Num","addr:housenumber")
            )
        )
    tm= ObjectTableModel(collection,columns)

    frame = JFrame("Street Table")
    frame.setSize(400, 150)
    frame.setLayout(BorderLayout())
    table = JTable(tm)
    scrollPane = JScrollPane()
    scrollPane.setPreferredSize(Dimension(300,100))
    scrollPane.getViewport().setView((table))
    panel = JPanel()
    panel.add(scrollPane)
    frame.add(panel, BorderLayout.CENTER)
    frame.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE)
    frame.setVisible(True)


def main() :
    Main.pref= Preferences()
    index = QuadBuckets();
#    bbox =  BBox(-90,-180,90,180)
    bbox =  BBox(-180,-90,180,90)
    node1=Node(2077593610) #id=2077593610,version=5,lat=39.103408052406124,lon=-95.67351809910174
    node1.setCoor(LatLon(39.103408052406124,-95.67351809910174))
    node1.put("addr:street","test")
    node1.put("addr:housenumber","1")

    node2=Node(2077593611) #id=2077593611,version=1,lat=39.1034080,lon=-95.67351809
    node2.setCoor(LatLon(39.1034080,-95.673518))
    node2.put("addr:street","test")
    node2.put("addr:housenumber","2")

    index.add(node1)
    index.add(node2)
    collection = index.search(bbox)
#    print collection
    DisplayTable(collection)
 
main()
