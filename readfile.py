from java.awt import *
from java.awt.event import ActionListener, ActionEvent
from java.lang import Object
from java.lang import Runnable
from java.net import URL
from java.util import Collection,HashSet,LinkedList,List,Set
from javax.swing import *
from javax.swing.table import AbstractTableModel
from javax.swing.table import DefaultTableModel
from org.openstreetmap.josm import Main
from org.openstreetmap.josm.data import Preferences;

Main.pref =  Preferences()

from org.openstreetmap.josm.data.osm import *;
from org.openstreetmap.josm.data.validation import *;
from org.openstreetmap.josm.tools import *;
from org.openstreetmap.josm.tools.I18n.tr import *
import org.openstreetmap.josm.Main as Main
import org.openstreetmap.josm.command as Command
import org.openstreetmap.josm.data.coor.LatLon as LatLon
import org.openstreetmap.josm.data.osm.BBox as BBox
import org.openstreetmap.josm.data.osm.DataSet as DataSet
import org.openstreetmap.josm.data.osm.Node as Node
import org.openstreetmap.josm.data.osm.TagCollection as TagCollection
import org.openstreetmap.josm.data.osm.Way as Way
import time
from org.openstreetmap.josm.tools.I18n.tr import *
import java.awt.Component
import java.io.File as File;
import java.io.FileInputStream as FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.util.Collection;
import org.openstreetmap.josm.data.Preferences as Preferences;
import org.openstreetmap.josm.data.osm.OsmPrimitive as OsmPrimitive;
import org.openstreetmap.josm.data.projection.Projection;
import org.openstreetmap.josm.Main as Main;
import org.openstreetmap.josm.gui.layer.OsmDataLayer;
import org.openstreetmap.josm.gui.progress.NullProgressMonitor as NullProgressMonitor;
import org.openstreetmap.josm.gui.progress.ProgressMonitor;
import org.openstreetmap.josm.io.IllegalDataException;
import org.openstreetmap.josm.io.OsmImporter as OsmImporter;
import org.openstreetmap.josm.io.OsmImporter.OsmImporterData;
import org.openstreetmap.josm.gui.preferences.projection.ProjectionChoice;
import org.openstreetmap.josm.gui.preferences.projection.ProjectionPreference as ProjectionPreference;
from sets import Set

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
#        print "row count %d " %  n
        return n
    def getColumnClass(self, columnIndex):
        return basestring
#        return self.__columns__[columnIndex][1]
    def getColumnName(self, columnIndex):
        return self.__columns__[columnIndex][0]
    def setValueAt(self, aValue, rowIndex, columnIndex):
        self[rowIndex][columnIndex] = aValue
    def refresh(self):
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
        for i, row in enumerate(self):
            if row == obj:
                return i
        return - 1
    def getSelectedObject(self, table):
        assert table.model is self
        if table.selectedRow >= 0:
            modelRow = table.convertRowIndexToModel(table.selectedRow)
            return self[modelRow]
    def getSelectedObjects(self, table):
        assert table.model is self
        selected = []
        for viewRow in table.selectedRows:
            modelRow = table.convertRowIndexToModel(viewRow)
            selected.append(self[modelRow])
        return selected

    def getVisibleObjects(self, table):
        assert table.model is self
        visible = []
        for viewRow in xrange(table.rowCount):
            modelRow = table.convertRowIndexToModel(viewRow)
            visible.append(self[modelRow])
        return visible

#def EventListener():
    
def DisplayTable (collection):
    columns=list(
        (
            ("Street","addr:street"),
            ("Num","addr:housenumber")
            )
        )
    tm= ObjectTableModel(collection,columns)
    frame = JFrame("Street Table")
    frame.setSize(800, 1200)
    frame.setLayout(BorderLayout())
    table = JTable(tm)
    table.setAutoResizeMode(JTable.AUTO_RESIZE_ALL_COLUMNS)
    header = table.getTableHeader()
    header.setUpdateTableInRealTime(True)
    header.setReorderingAllowed(True);
    scrollPane = JScrollPane()
    scrollPane.getViewport().setView((table))
    frame.add(scrollPane)
    frame.pack();
    frame.setSize(frame.getPreferredSize());
    frame.show()


def DisplayStreetTable (collection):
    columns=list(
        (
            ("Name","name"),
            )
        )
    tm= ObjectTableModel(collection,columns)
    frame = JFrame("Street Table")
    frame.setSize(800, 1200)
    frame.setLayout(BorderLayout())
    table = JTable(tm)
    table.setAutoResizeMode(JTable.AUTO_RESIZE_ALL_COLUMNS)
    header = table.getTableHeader()
    header.setUpdateTableInRealTime(True)
    header.setReorderingAllowed(True);
    scrollPane = JScrollPane()
    scrollPane.getViewport().setView((table))
    frame.add(scrollPane)
    frame.pack();
    frame.setSize(frame.getPreferredSize());
    frame.show()


def isBuilding(p):
    v = p.get("building");
    if v is not None and v != "no" and v != "entrance":
        return True
    else:
        return False

class BuildingInBuilding :

    BUILDING_INSIDE_BUILDING = 2001;

    def __init__ (self):
        self.primitivesToCheck = LinkedList();
        self.index = QuadBuckets();
        print 'building in building'
        #super(tr("Building inside building"), tr("Checks for building areas inside of buildings."));
  
    def visitn(self,n) :
#        print "visitn:"
#        print n
        if (n.isUsable() and isBuilding(n)) :
            if not self.primitivesToCheck.contains(n):
#                print "adding  :"  n 
                self.primitivesToCheck.add(n);
            else:
                print "duplicate p :" 
#                print n

    def visitw(self,w) :
        print "visitw:"
#        print w
        if (w.isUsable() and w.isClosed() and isBuilding(w)) :
            self.primitivesToCheck.add(w)
            self.index.add(w)
            print "added"

    def isInPolygon(n, polygon) :
        return Geometry.nodeInsidePolygon(n, polygon);
    
    def sameLayers( w1, w2) :
        if w1.get("layer") is not None :
            l1 = w1.get("layer") 
        else :
            l1 = "0";
        if  w2.get("layer") is not None :
            l2 = w2.get("layer") 
        else : 
            l2 ="0";
        return l1.equals(l2);
    
    def evaluateNode(self,p,obj):
        print "te"
#        print p
#        print obj

    def endTest2(self):
        for p in self.primitivesToCheck :
            collection = self.index.search(p.getBBox())
            for object in collection:
                if (not p.equals(object)):              
                    if (isinstance(p,Node)):
                        self.evaluateNode(p, object)
                    else :
                        print p
            #         else if (p instanceof Way)
            #             return evaluateWay((Way) p, object);
            #         else if (p instanceof Relation)
            #             return evaluateRelation((Relation) p, object);
            #         return false;

    def endTest(self) :
        print "end"
#        bbox =  BBox(-180,-90,180,90)
        bbox =  BBox(-1000,-900,1800,900)
        print self.index
        collection = self.index.search(bbox)
#        print collection
                

def projection() :
    print "projection"
    pc = ProjectionPreference.mercator
    id = pc.getId()
    pref = None
    Main.pref.putCollection("projection.sub."+id, pref)
    pc.setPreferences(pref)
    proj = pc.getProjection()
    Main.setProjection(proj)
		
def prefs() :
    print "prefs"
    Main.pref =  Preferences()
    Main.pref.put("tags.reversed_direction", "false")

class JythonWay():
    def __init__(self,x):
        self.way=x
        self.subobjects=[]
        pass

# todo:
    def lookup(self) :
        # lookup this street name on the internet
        print "ToDO"

# todo:
    def merge(self) :
        # merge these two streets, fix the names
        print "ToDO fix the streets"

    def get (self,k):
        return self.way.get(k)

    def name(self):
        return self.way.get('name')

    def addsubobject(self, other):
        return self.subobjects.append(other)

import re
pattern = re.compile(r'\s+')



def streetlist(objs) :
    objs2 = []
    streets = {}
    for p in objs:
        if (not isinstance(p,Way)):
            continue
        s=p.get('name')
        hw=p.get('highway')        
        if (s is  None):
            continue        
        if (hw is  None):
            continue        

        s = s.lower()
        s=re.sub(pattern, '', s) #remove whitespace       
        if not s in streets :
            print "%s is new" % s
            streets[s]=JythonWay(p)
        else :
            streets[s].addsubobject(p)
#            print streets.values()
    objs3= sorted(streets.values(),(lambda x, y: (cmp(x.name(), y.name())))) 
    DisplayStreetTable(objs3)

	
def main ():
    print "main"
    prefs();
    projection();
    importer =  OsmImporter()
    fileObj=  File('/home/mdupont/experiments/josm/topeka/noto.osm')
    inobj = FileInputStream(fileObj);
    data = importer.loadLayer(inobj, fileObj, fileObj.getName(), NullProgressMonitor.INSTANCE)
    s = data.toString();
#    print s
    primitives = data.getLayer().data.allPrimitives();
#    print primitives
    objs= primitives.toArray()
    #DisplayTable(obj)
    streetlist(objs)
# make a list of the street objects

main();
