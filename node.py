from java.lang import Object
from javax.swing.table import AbstractTableModel
from java.awt import Component, GridLayout
from java.awt.event import ActionListener, ActionEvent
from java.lang import Runnable
from java.net import URL
from java.util import Collection,HashSet,LinkedList,List,Set
from javax.swing import *
from org.openstreetmap.josm import Main
from org.openstreetmap.josm.data import Preferences;
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
import time

def main ():
    Main.pref= Preferences()
    print Main.pref
    #Main.pref.set("tags.reversed_direction", False);
    node1=Node(2077593610) #id=2077593610,version=5,lat=39.103408052406124,lon=-95.67351809910174
    print node1

main()
