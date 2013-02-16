
from   java.lang      import Runnable;
from   javax.swing    import JFrame;
from   javax.swing    import SwingUtilities;
class ToBeDetermined( Runnable ) :
    def __init__( self ) :
        self.frame = JFrame( 'ToBeDetermined' , defaultCloseOperation = JFrame.EXIT_ON_CLOSE );        
    def run( self ) :
        self.frame.setVisible( 1 );   # Have the application make itself visible

SwingUtilities.invokeLater( ToBeDetermined() );
raw_input();

