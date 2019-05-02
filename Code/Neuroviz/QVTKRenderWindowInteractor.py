"""
File name:  QVTKRenderWindowInteractor.py
Author:     Gerbrand De Laender
Date:       01/05/2019
Email:      gerbrand.delaender@ugent.be
Brief:      E016712, Project, Neuroviz
About:      Class used to display VTK contents in an OpenGL widget. Originally
            created by Prabhu Ramachandran.
"""

################################################################################
################################################################################

from logging import getLogger

from PyQt5.QtCore import QEvent, QObject, QSize, Qt, QTimer
from PyQt5.QtGui import QCursor
from PyQt5.QtOpenGL import QGLWidget
from PyQt5.QtWidgets import QApplication, QSizePolicy, QWidget

from vtkmodules.vtkRenderingCore import (vtkGenericRenderWindowInteractor,
                                         vtkRenderWindow)

logger = getLogger( __name__ )

################################################################################
################################################################################

class QVTKRenderWindowInteractor( QGLWidget ):

    """
    QVTKRenderWindowInteractor adapted from
    vtk/Wrapping/Python/vtkmodules/qt/QVTKRenderWindowInteractor.py,
    but is derived from a QGLWidget to prevent rendering issues.
    """

    _CURSOR_MAP = {
        0:  Qt.ArrowCursor,
        1:  Qt.ArrowCursor,
        2:  Qt.SizeBDiagCursor,
        3:  Qt.SizeFDiagCursor,
        4:  Qt.SizeBDiagCursor,
        5:  Qt.SizeFDiagCursor,
        6:  Qt.SizeVerCursor,
        7:  Qt.SizeHorCursor,
        8:  Qt.SizeAllCursor,
        9:  Qt.PointingHandCursor,
        10: Qt.CrossCursor
    }

    _KEY_MAP = {
        Qt.Key_Backspace: 'BackSpace',
        Qt.Key_Tab: 'Tab',
        Qt.Key_Backtab: 'Tab',
        Qt.Key_Return: 'Return',
        Qt.Key_Enter: 'Return',
        Qt.Key_Shift: 'Shift_L',
        Qt.Key_Control: 'Control_L',
        Qt.Key_Alt: 'Alt_L',
        Qt.Key_Pause: 'Pause',
        Qt.Key_CapsLock: 'Caps_Lock',
        Qt.Key_Escape: 'Escape',
        Qt.Key_Space: 'space',
        Qt.Key_End: 'End',
        Qt.Key_Home: 'Home',
        Qt.Key_Left: 'Left',
        Qt.Key_Up: 'Up',
        Qt.Key_Right: 'Right',
        Qt.Key_Down: 'Down',
        Qt.Key_SysReq: 'Snapshot',
        Qt.Key_Insert: 'Insert',
        Qt.Key_Delete: 'Delete',
        Qt.Key_Help: 'Help',
        Qt.Key_0: '0',
        Qt.Key_1: '1',
        Qt.Key_2: '2',
        Qt.Key_3: '3',
        Qt.Key_4: '4',
        Qt.Key_5: '5',
        Qt.Key_6: '6',
        Qt.Key_7: '7',
        Qt.Key_8: '8',
        Qt.Key_9: '9',
        Qt.Key_A: 'a',
        Qt.Key_B: 'b',
        Qt.Key_C: 'c',
        Qt.Key_D: 'd',
        Qt.Key_E: 'e',
        Qt.Key_F: 'f',
        Qt.Key_G: 'g',
        Qt.Key_H: 'h',
        Qt.Key_I: 'i',
        Qt.Key_J: 'j',
        Qt.Key_K: 'k',
        Qt.Key_L: 'l',
        Qt.Key_M: 'm',
        Qt.Key_N: 'n',
        Qt.Key_O: 'o',
        Qt.Key_P: 'p',
        Qt.Key_Q: 'q',
        Qt.Key_R: 'r',
        Qt.Key_S: 's',
        Qt.Key_T: 't',
        Qt.Key_U: 'u',
        Qt.Key_V: 'v',
        Qt.Key_W: 'w',
        Qt.Key_X: 'x',
        Qt.Key_Y: 'y',
        Qt.Key_Z: 'z',
        Qt.Key_Asterisk: 'asterisk',
        Qt.Key_Plus: 'plus',
        Qt.Key_Minus: 'minus',
        Qt.Key_Period: 'period',
        Qt.Key_Slash: 'slash',
        Qt.Key_F1: 'F1',
        Qt.Key_F2: 'F2',
        Qt.Key_F3: 'F3',
        Qt.Key_F4: 'F4',
        Qt.Key_F5: 'F5',
        Qt.Key_F6: 'F6',
        Qt.Key_F7: 'F7',
        Qt.Key_F8: 'F8',
        Qt.Key_F9: 'F9',
        Qt.Key_F10: 'F10',
        Qt.Key_F11: 'F11',
        Qt.Key_F12: 'F12',
        Qt.Key_F13: 'F13',
        Qt.Key_F14: 'F14',
        Qt.Key_F15: 'F15',
        Qt.Key_F16: 'F16',
        Qt.Key_F17: 'F17',
        Qt.Key_F18: 'F18',
        Qt.Key_F19: 'F19',
        Qt.Key_F20: 'F20',
        Qt.Key_F21: 'F21',
        Qt.Key_F22: 'F22',
        Qt.Key_F23: 'F23',
        Qt.Key_F24: 'F24',
        Qt.Key_NumLock: 'Num_Lock',
        Qt.Key_ScrollLock: 'Scroll_Lock'
        }

    ############################################################################

    def __init__( self, parent = None, **kwargs ):
        """
        Initialize a custom QVTKRenderWindowInteractor for Python and Qt5.
        Uses a vtkGenericRenderWindowInteractor to handle the interactions.
        """
        logger.info( f"Creating {__class__.__name__}..." )

        self.__saveX = 0
        self.__saveY = 0
        self.__saveModifiers = Qt.NoModifier
        self.__saveButtons = Qt.NoButton
        self.__wheelDelta = 0
        self._activeButton = Qt.NoButton

        QGLWidget.__init__( self, parent )

        self.setAttribute( Qt.WA_OpaquePaintEvent )
        self.setAttribute( Qt.WA_PaintOnScreen )
        self.setMouseTracking( True )
        self.setFocusPolicy( Qt.WheelFocus )
        self.setSizePolicy( QSizePolicy( QSizePolicy.Expanding, QSizePolicy.Expanding ) )

        self._RenderWindow = vtkRenderWindow()
        self._RenderWindow.SetWindowInfo( str( int( self.winId() ) ) )
        self._RenderWindow.AddObserver( "CursorChangedEvent", self.onCursorChanged )

        self._interactor = vtkGenericRenderWindowInteractor()
        self._interactor.SetRenderWindow( self._RenderWindow )
        self._interactor.AddObserver( "CreateTimerEvent", self.onCreateTimer )
        self._interactor.AddObserver( "DestroyTimerEvent", self.onDestroyTimer )

        self._timer = QTimer( self )
        self._timer.timeout.connect( self.onTimeout )

        # Create hidden child widget to allow for cleanup of the VTK elements,
        # since child widget will be destroyed before its parent.
        self._hidden = QWidget( self )
        self._hidden.hide()
        self._hidden.destroyed.connect( self.onDestruction )

    ############################################################################

    def __getattr__( self, attr ):
        """
        Makes the object behave like a vtkGenericRenderWindowInteractor.
        """
        if attr == "__vtk__":
            return lambda t = self._interactor: t
        elif hasattr( self._interactor, attr ):
            return getattr( self._interactor, attr )
        else:
            raise AttributeError( self.__class__.__name__ + " has no attribute named " + attr)

    ############################################################################

    def onDestruction( self ):
        """
        Call internal cleanup method on VTK objects.
        """
        self._RenderWindow.Finalize()

    ############################################################################

    def onCreateTimer( self, obj, evt ):
        """
        Start the timer.
        """
        self._timer.start( 10 )

    ############################################################################

    def onDestroyTimer( self, obj, evt ):
        """
        Stop the timer.
        """
        self._timer.stop()
        return 1

    ############################################################################

    def onTimeout( self ):
        """
        On timeout.
        """
        self._interactor.TimerEvent()

    ############################################################################

    def onCursorChanged( self, obj, evt ):
        """
        Called when the CursorChangedEvent fires on the render window. This
        indirection is needed since when the event fires, the current cursor is
        not yet set so we defer this by which time the current cursor should
        have been set.
        """
        QTimer.singleShot( 0, self.ShowCursor )

    ############################################################################

    def HideCursor( self ):
        """
        Hides the cursor.
        """
        self.setCursor( Qt.BlankCursor )

    ############################################################################

    def ShowCursor( self ):
        """
        Shows the cursor.
        """
        vtkCursor = self._interactor.GetRenderWindow().GetCurrentCursor()
        qtCursor = self._CURSOR_MAP.get( vtkCursor, Qt.ArrowCursor )
        self.setCursor( qtCursor )

    ############################################################################

    def closeEvent( self, evt ):
        """
        When the widget is about to be closed.
        """
        self.onDestruction()

    ############################################################################

    def sizeHint( self ):
        """
        Recommended widget size.
        """
        return QSize(400, 400)

    ############################################################################

    def paintEngine( self ):
        """
        Paint engine used for drawing on the device (done by VTK internally).
        """
        return None

    ############################################################################

    def paintEvent( self, evt ):
        """
        Render the scene when a paintEvent is fired.
        """
        self._interactor.Render()

    ############################################################################

    def resizeEvent( self, ev ):
        """
        Resize the widget.
        """
        h, w = self.height(), self.width()
        vtkRenderWindow.SetSize( self._RenderWindow, w, h )
        self._interactor.SetSize( w, h )
        self._interactor.ConfigureEvent()
        self.update()

    ############################################################################

    def _GetCtrlShift( self, ev ):
        """
        Recognize Ctrl + Shift key combinations.
        """
        ctrl = shift = False

        if hasattr( ev, "modifiers" ):
            if ev.modifiers() & Qt.ShiftModifier: shift = True
            if ev.modifiers() & Qt.ControlModifier: ctrl = True
        else:
            if self.__saveModifiers & Qt.ShiftModifier: shift = True
            if self.__saveModifiers & Qt.ControlModifier: ctrl = True

        return ctrl, shift

    ############################################################################

    @staticmethod
    def _getPixelRatio():
        """
        Source = https://stackoverflow.com/a/40053864/3388962
        """
        pos = QCursor.pos()

        for screen in QApplication.screens():
            rect = screen.geometry()
            if rect.contains( pos ):
                return screen.devicePixelRatio()

        # Should never happen, but try to find a good fallback.
        return QApplication.devicePixelRatio()

    ############################################################################

    def _setEventInformation (self, x, y, ctrl, shift, key, repeat = 0, keysum = None ):
        """
        Sets information about the event.
        """
        scale = self._getPixelRatio()
        self._interactor.SetEventInformation( int( round( x * scale ) ),
                                              int( round( (self.height() - y - 1) * scale ) ),
                                              ctrl, shift, key, repeat, keysum )

    ############################################################################

    def enterEvent(self, ev):
        """
        When entering an event.
        """
        self._setEventInformation( self.__saveX, self.__saveY, *self._GetCtrlShift( ev ), chr( 0 ), 0, None )
        self._interactor.EnterEvent()

    ############################################################################

    def leaveEvent(self, ev):
        """
        When leaving an event.
        """
        self._setEventInformation( self.__saveX, self.__saveY, *self._GetCtrlShift( ev ), chr( 0 ), 0, None )
        self._interactor.LeaveEvent()

    ############################################################################

    def mousePressEvent( self, ev ):
        """
        When the mouse has been pressed.
        """
        repeat = 0
        if ev.type() == QEvent.MouseButtonDblClick: repeat = 1

        self._setEventInformation( ev.x(), ev.y(), *self._GetCtrlShift( ev ), chr( 0 ), repeat, None )

        self._activeButton = ev.button()

        if self._activeButton == Qt.LeftButton: self._interactor.LeftButtonPressEvent()
        elif self._activeButton == Qt.RightButton: self._interactor.RightButtonPressEvent()
        elif self._activeButton == Qt.MidButton: self._interactor.MiddleButtonPressEvent()

    ############################################################################

    def mouseReleaseEvent( self, ev ):
        """
        When the mouse has been released.
        """
        self._setEventInformation( ev.x(), ev.y(), *self._GetCtrlShift( ev ), chr( 0 ), 0, None )

        if self._activeButton == Qt.LeftButton: self._interactor.LeftButtonReleaseEvent()
        elif self._activeButton == Qt.RightButton: self._interactor.RightButtonReleaseEvent()
        elif self._activeButton == Qt.MidButton: self._interactor.MiddleButtonReleaseEvent()

    ############################################################################

    def mouseMoveEvent( self, ev ):
        """
        When the mouse has moved.
        """
        self.__saveModifiers, self._saveButtons = ev.modifiers(), ev.buttons()
        self.__saveX, self.__saveY = ev.x(), ev.y()

        self._setEventInformation( ev.x(), ev.y(), *self._GetCtrlShift(ev), chr( 0 ), 0, None)
        self._interactor.MouseMoveEvent()

    ############################################################################

    def keyPressEvent( self, ev ):
        """
        When a key has been pressed.
        """
        ctrl, shift = self._GetCtrlShift( ev )

        if ev.key() < 256: key = str( ev.text() )
        else: key = chr( 0 )

        keySymbol = self._KEY_MAP.get( ev.key(), None )

        if shift and len( keySymbol ) == 1 and keySymbol.isalpha():
            keySymbol = keySymbol.upper()

        self._setEventInformation( self.__saveX, self.__saveY, ctrl, shift, key, 0, keySymbol )
        self._interactor.KeyPressEvent()
        self._interactor.CharEvent()

    ############################################################################

    def keyReleaseEvent( self, ev ):
        """
        When a key is released.
        """
        ctrl, shift = self._GetCtrlShift( ev )

        if ev.key() < 256: key = str( ev.text() )
        else: key = chr( 0 )

        self._setEventInformation(self.__saveX, self.__saveY, ctrl, shift, key, 0, None )
        self._interactor.KeyReleaseEvent()

    ############################################################################

    def wheelEvent( self, ev ):
        """
        When scrolling mouse wheel.
        """
        if hasattr( ev, "delta" ): self.__wheelDelta += ev.delta()
        else: self.__wheelDelta += ev.angleDelta().y()

        if self.__wheelDelta >= 120:
            self._interactor.MouseWheelForwardEvent()
            self.__wheelDelta = 0
        elif self.__wheelDelta <= -120:
            self._interactor.MouseWheelBackwardEvent()
            self.__wheelDelta = 0

    ############################################################################

    def GetRenderWindow( self ):
        """
        get the current render window.
        """
        return self._RenderWindow

    ############################################################################

    def Render( self ):
        """
        Update the scene.
        """
        self.update()

################################################################################
################################################################################
