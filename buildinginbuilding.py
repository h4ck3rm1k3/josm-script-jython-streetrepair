from javax.swing import JOptionPane, JDialog
from java.awt.event import ActionListener, ActionEvent
from org.openstreetmap.josm import Main
import org.openstreetmap.josm.command as Command
import org.openstreetmap.josm.data.osm.Node as Node
import org.openstreetmap.josm.data.osm.Way as Way
import org.openstreetmap.josm.data.osm.TagCollection as TagCollection
import org.openstreetmap.josm.data.osm.DataSet as DataSet
import time
from org.openstreetmap.josm.tools.I18n.tr import *
from java.util import Collection
from java.util import HashSet
from java.util import LinkedList;
from java.util import List;
from java.util import Set;
from org.openstreetmap.josm.data.osm import *;
# from org.openstreetmap.josm.data.osm import OsmPrimitive;
# import org.openstreetmap.josm.data.osm.OsmPrimitiveType;
# import org.openstreetmap.josm.data.osm.QuadBuckets;
# import org.openstreetmap.josm.data.osm.Relation;
# import org.openstreetmap.josm.data.osm.RelationMember;
# import org.openstreetmap.josm.data.osm.Way;
from org.openstreetmap.josm.data.validation import *;
from org.openstreetmap.josm.tools import *;
from org.openstreetmap.josm.tools import *;

#            outers = FilteredCollection(index.search(p.getBBox()),  Predicate() :
 
# class myFilteredCollect :
#     def evaluateNode(n, obj) :
#         x =isInPolygon(n, object.getNodes())
#         if (x):
#             return x
#         x = object.getNodes().contains(n);
#         if (x):
#             return x
#     def evaluateWay(w, obj) :
#         if (w.equals(object)) :
#             return false;                 
#     def evaluate(Way object) {
#         if p.equals(object):
#             return false;
#         else if (p instanceof Node):
#             return evaluateNode((Node) p, object);
#         else if (p instanceof Way):
#             return evaluateWay((Way) p, object);
#         else if (p instanceof Relation) :
#             return evaluateRelation((Relation) p, object);
#         return false;

def isBuilding(p):
    v = p.get("building");
    if v is not None and v != "no" and v != "entrance":
        return True
    else:
        return False

class BuildingInBuilding :

    BUILDING_INSIDE_BUILDING = 2001;
    primitivesToCheck = LinkedList();
    index = QuadBuckets();

    def __init__ (self):
        print 'building in building'
        #super(tr("Building inside building"), tr("Checks for building areas inside of buildings."));
    

    def visitn(self,n) :
        if (n.isUsable() and isBuilding(n)) :
            self.primitivesToCheck.add(n);

    def visitw(self,w) :
        if (w.isUsable() and w.isClosed() and isBuilding(w)):
            self.primitivesToCheck.add(w);
            self.index.add(w);

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
    
 
    def endTest(self) :
        for p in self.primitivesToCheck :
            print p
    #     super.endTest();




def main():
    b=BuildingInBuilding()

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
                         b.visitw(way)
        #                print 'house box:', street, housenumber
        

        b.endTest()
        

main()
