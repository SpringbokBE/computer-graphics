# Overview of classes and their methods.

Provided is an overview of the different classes that are used in the application, along with their methods. Private methods are marked with a `[-]`, public methods with a `[+]`.

## Main
`[+] setupLogger()`  
`[+] setupFileLogger( settings )`  
`[+] setupConsoleLogger( settings )`  
`[+] setupModulesToLog( settings )`  

## App( QApplication )
`[-] __init__( *args, **kwargs )`  

## Gui( QMainWindow )
`[-] __init__( *args, **kwargs )`  
`[-] _recompileUi()`  
`[-] _onTabWidgetCurrentChanged( index )`  

## BasicWidget( QWidget )
`[-] __init__( dockWidget ,*args, **kwargs )`  
`[+] activate()`  
`[-] _createLayout()`  

## EEGWidget( QWidget )
`[-] __init__( dockWidget, *args, **kwargs )`  
`[+] activate()`  
`[-] _createLayout()`  

## DSAWidget( QWidget )
`[-] __init__( dockWidget, *args, **kwargs )`  
`[+] activate()`  
`[-] _createLayout()`  

## QVTKRenderWindowInteractor( QGLWidget )
`[-] __init__( parent = None, **kwargs )`  
`[-] __getattr__( attr )`  
`[+] onDestruction()`  
`[+] onCreateTimer( obj, evt )`  
`[+] onDestroyTimer( obj, evt )`  
`[+] onTimeout()`  
`[+] onCursorChanged( obj, evt )`  
`[+] HideCursor()`  
`[+] ShowCursor()`  
`[+] closeEvent( evt )`  
`[+] sizeHint()`  
`[+] paintEngine()`  
`[+] paintEvent( evt )`  
`[+] resizeEvent( ev )`  
`[-] _GetCtrlShift( ev )`  
`[-] _getPixelRatio()`  
`[-] _setEventInformation ( x, y, ctrl, shift, key, repeat = 0, keysum = None )`  
`[+] enterEvent( ev )`  
`[+] leaveEvent( ev )`  
`[+] mousePressEvent( ev )`  
`[+] mouseReleaseEvent( ev )`  
`[+] mouseMoveEvent( ev )`  
`[+] keyPressEvent( ev )`  
`[+] keyReleaseEvent( ev )`  
`[+] wheelEvent( ev )`  
`[+] GetRenderWindow()`  
`[+] Render()`  

## BasicSceneAndInteractor( QObject )
`[-] __init__( ui, *args, **kwargs )`  
`[+] activate()`  
`[-] _updateInteractorFromScene()`  
`[-] _updateSceneFromInteractor()`  
`[-] _connectSignalsToSlots()`  
`[-] _onComboBoxInteractionStyleActivated( index )`  
`[-] _onComboBoxActiveContourActivated( index )`  
`[-] _onSliderGroupChanged( _ )`  
`[-] _onSliderGroupToggled( _ )`  
`[-] _onSliderOpacityChanged( value )`  
`[-] _onSliderGroupTimeout()`  

## EEGSceneAndInteractor( QObject )
`[-] __init__( ui, *args, **kwargs )`  
`[+] activate()`  
`[-] _updateSceneFromInteractor()`  
`[-] _connectSignalsToSlots()`  
`[-] _onSliderGroupAnimationsToggled( state )`  
`[-] _onSliderGroupAnimationsChanged( value )`  

## DSASceneAndInteractor( QObject )
`[-] __init__( ui, *args, **kwargs )`  
`[+] activate()`  
`[-] _initializeInteractor()`  
`[-] _connectSignalsToSlots()`  
`[-] _onComboBoxDataSetActivated( index )`  
`[-] _onSpinBoxChanged( _ )`  
`[-] _onSpinBoxTimeout()`  
`[-] _onHuePicked( hueMultiplier, hueConstant )`  

## BasicScene( QObject )
`[-] __init__( renderWindow, *args, **kwargs )`  
`[+] initializeScene( fileName = None, interactionStyle = None )`  
`[+] updateSlices( slices = [None, None, None])`  
`[+] getInteractionStyle()`  
`[+] setInteractionStyle( interactionStyle )`  
`[+] getBounds()`  
`[+] getContourNames()`  
`[+] getActiveContourName()`  
`[+] setActiveContour( contourName )`  
`[+] getOpacity()`  
`[+] setOpacity( value )`  
`[+] resetOpacity()`  
`[-] _createReader( fileName )`  
`[-] _createNamedColors()`  
`[-] _createOutlineActor()`  
`[-] _readContourInfo()`  
`[-] _createContours()`  
`[-] _createContourActors()`  
`[-] _createOctants()`  
`[-] _createOctantActors()`  
`[-] _createImageResliceActors()`  
`[-] _createRendererAndInteractor()`  
`[-] _createEmptyRenderer()`  
`[-] _updateOctantActors()`  
`[-] _updateOctantActorsVisibility( DOP = None, force = False )`  
`[-] _updateImageResliceActors()`  
`[-] _onCameraMoved( camera, event )`  

## MouseInteractorToggleOpacity( vtkInteractorStyleTrackballCamera )
`[-] __init__( renderer, octants, slices, parent = None )`  
`[+] updateSlices( slices )`  
`[+] getOpacity()`  
`[+] setOpacity( value )`  
`[-] _onMiddleButtonPress( object, event )`  
`[-] _onMiddleButtonRelease( object, event )`  

## EEGScene( QObject )
`[-] __init__( renderWindow, chartXYWindow, *args, **kwargs )`  
`[+] initializeScene( fileName = None )`  
`[+] addElectrode( position )`  
`[+] getBounds()`  
`[+] setUpdateInterval( interval = None )`  
`[-] _createReader( fileName )`  
`[-] _createNamedColors()`  
`[-] _createOutlineActor()`  
`[-] _readContourInfo()`  
`[-] _createContour()`  
`[-] _smoothContour()`  
`[-] _interpolateContour()`  
`[-] _createContourActor()`  
`[-] _createScalarBarActor()`  
`[-] _createRendererAndInteractor()`  
`[-] _createEmptyRenderer()`  
`[-] _createCharts()`  
`[-] _readElectrodeChoices()`  
`[-] _createElectrodeTextActors()`  
`[-] _updateCharts()`  
`[-] _clearCharts()`  
`[-] _onTimeout()`  

## MouseInteractorAddElectrode( vtkInteractorStyleTrackballCamera )
`[-] __init__( renderer, contour, callback, parent = None )`  
`[-] _onMiddleButtonPress( object, event )`  
`[-] _onMiddleButtonRelease( object, event )`  

## DSAScene( QObject )
`[-] __init__( renderWindow, *args, **kwargs )`  
`[+] readDataSet( fileName = None )`  
`[+] setParameters( hueMultiplier = None, hueConstant = None, valueMultiplier = None )`  
`[+] calculateRGBImage()`  
`[+] showRGBImage()`  
`[-] _initializeScene()`  
`[-] _createNamedColors()`  
`[-] _createEmptyRenderer()`  
`[-] _pickHue( xPos, yPos )`  

## MouseInteractorPickMinMax( vtkInteractorStyleImage )
`[-] __init__( renderer, callback, parent = None )`  
`[-] _onMiddleButtonPress( object, event )`  
`[-] _onMiddleButtonRelease( object, event )`  

## Ui_qmwMain( object )
`[+] setupUi( qmwMain )`  
`[+] retranslateUi( qmwMain )`  

## SliderGroup( QWidget )
`[-] __init__( name, *args, **kwargs )`  
`[+] getEnabled( )`  
`[+] setEnabled( isEnabled )`  
`[+] getChecked()`  
`[+] setChecked( checked )`  
`[+] getValue()`  
`[+] setValue( value )`  
`[+] getText()`  
`[+] setText( text )`  
`[+] getRange()`  
`[+] setRange( minimum, maximum )`  
`[-] _createLayout()`  
`[-] _applyInitialSettings()`  
`[-] _onCheckBoxToggled( isChecked )`  
`[-] _onSliderValueChanged( value )`  
`[-] _onSpinBoxValueChanged( value )`  
