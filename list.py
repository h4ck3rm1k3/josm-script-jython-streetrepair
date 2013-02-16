from javax.swing import *
from java.awt import Component, GridLayout
from java.net import URL
from java.lang import Runnable
from javax.swing import JOptionPane
#from org.openstreetmap.josm import Main
# some ideas copied from http://www.jython.org/jythonbook/en/1.0/GUIApplications.html 

class JyLog(object):
    def __init__(self):
        self.frame = JFrame(
            "Validation"
            )

        self.resultPanel = JPanel()
        self.resultPanel.layout = BoxLayout(self.resultPanel, BoxLayout.Y_AXIS)


        scrollpane = JScrollPane(JScrollPane.VERTICAL_SCROLLBAR_AS_NEEDED,
                                 JScrollPane.HORIZONTAL_SCROLLBAR_NEVER)
        scrollpane.preferredSize = 400, 800
        scrollpane.viewport.view = self.resultPanel

        self.frame.add(scrollpane)


        self.frame.size = 400,800
        self.frame.pack()
        self.show()

    def details(self,item):
        
        print item
        JOptionPane.showMessageDialog(Main.parent, "[Python] Hello World! You have  layer(s)." )

    def nodeDetails(self,item):        
        print item
        JOptionPane.showMessageDialog(Main.parent, "[Python] Hello World! You have  layer(s)." )

    def showItem(self, item):
        p = JPanel()
#        p.add(JLabel(ImageIcon(URL(user.profile_image_url))))
        p.add(JTextArea(text = item,
                        editable = False,
                        wrapStyleWord = True,
                        lineWrap = True,
                        alignmentX = Component.LEFT_ALIGNMENT,
                        size = (300, 1)
             ))

        
        details = JButton('Details',actionPerformed=self.details)
        p.add(details)

        self.resultPanel.add(p)



    def showNode(self, node):
        p = JPanel()
#        p.add(JLabel(ImageIcon(URL(user.profile_image_url))))
        someitem =   node.get('addr:housenumber') + " " +  node.get('addr:street')
        p.add(JTextArea(text = someitem,
                        editable = False,
                        wrapStyleWord = True,
                        lineWrap = True,
                        alignmentX = Component.LEFT_ALIGNMENT,
                        size = (300, 1)
             ))
        
        details = JButton('Details',actionPerformed=self.nodeDetails)
        p.add(details)

        self.resultPanel.add(p)

    def show(self):
        self.frame.visible = True

#
#l=JyLog()
#l.showItem("test")
