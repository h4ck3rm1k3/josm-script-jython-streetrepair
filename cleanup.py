from javax.swing import JOptionPane, JDialog
from java.awt.event import ActionListener, ActionEvent
from org.openstreetmap.josm import Main
import org.openstreetmap.josm.command as Command
import org.openstreetmap.josm.data.osm.Node as Node
import org.openstreetmap.josm.data.osm.Way as Way
import org.openstreetmap.josm.data.osm.TagCollection as TagCollection
import org.openstreetmap.josm.data.osm.DataSet as DataSet
import time

def getMapView():
    if Main.main and Main.main.map:
        return Main.main.map.mapView
    else:
        return None

def buildingway_in_buildingway():
    print "find building nodes inside buildings and merge them"


def housenumber_same():
    print "find nodes with the same house number"


def streetname_and_house_streetname_similar():
    print "find all the nodes with mispelled streets "

def main():
    if Main.main and Main.main.map:
        mv= Main.main.map.mapView
        print mv.editLayer

        if mv.editLayer and mv.editLayer.data:
            selectedWays = mv.editLayer.data.getSelectedWays()
            if not(selectedWays):
                JOptionPane.showMessageDialog(Main.parent, "Please select a set of ways")
            else:
                print "going to output ways";
                for way in selectedWays:
                    #is there a 
                    housenumber=way.get('addr:housenumber')
                    street=way.get('addr:street')
                    if(housenumber):
                        print 'house box:', street, housenumber


main()
