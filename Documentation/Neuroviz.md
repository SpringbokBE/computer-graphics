# Neuroviz.ini configuration file

Provided is an overview of the different sections that can be tweaked to alter the functionality of the application. Altering the scene and/or interators will also write to this file, so the settings could be overwritten!

## \[Gui]
* `Preload` = _`Bool`_ contains the boolean value that indicates whether all scenes should be loaded at startup (True) or at runtime (False).
* `PyFileName` = _`/Relative/Path/To/PyFile.py`_ contains the relative path (___str___) to the Python file that is to be generated when recompiling the UI from Qt Designer.
* `UiClassName` = _`ClassName`_ contains the name (___str___) of the MainWindow class that is generated in Qt Designer.
* `UiFileName` = _`/Relative/Path/To/UiFile.py`_ contains the relative path (___str___) to the UI file that is to be recompiled when updating the UI from Qt Designer.

## \[Logging]
* `Enabled` = _`Bool`_ contains the boolean value that indicates whether logging should be enabled or disabled.
* `LogToConsole` = _`Bool`_ contains the boolean value that indicates whether logging to a console should be enabled or disabled.
* `LogToConsoleFormat` = _`LogFormat`_ contains the formatting style (___str___) when logging to a console.
* `LogToFile` = _`Bool`_ contains the boolean value that indicates whether logging to a file should be enabled or disabled.
* `LogToFileFormat` = _`LogFormat`_ contains the formatting style (___str___) when logging to a file.
* `LogToFileName`= _`LogFileName`_ contains (a relative path to) the filename (___str___) in which to log when logging to a file is enabled.
* `ModulesToLog` = _`Module1Name->Level1, Module2Name->Level2`_ contains a list of the names (___str___) of the modules to be logged and the minimum level for each of them. Possible levels are "_Debug_", "_Info_", "_Warning_", "_Error_" and "_Critical_" (___str___).

## [BasicScene]
* `ActiveContour` = _`NameOfContour`_ contains the name (___str___) (as specified in `ContourValues`) of the active contour.
* `ContourSmoothings` = _`Name1->Radius/StdDev/Iters/PassBand/Angle, Name2->Radius/StdDev/Iters/PassBand/Angle`_ contains a list of names (___str___) (as specified in `ContourValues`) of the contours along with their smoothing parameters. `Radius` (___int___) and `StdDev` (___float___) are used in the Gaussian smoothing, `Iters` (___int___), `PassBand` (___float___) and `Angle` (___float___) are used in the windowed sinc filtering.
* `ContourValues` = _`Name1->Value1, Name2->Value2`_ contains a list of names (___str___) of the contours along with their isosurface value (___int___), which is the greyscale value that will be used to generate contour.
* `FileName` = _`/Relative/Path/To/VTK/File`_ contains the relative path (___str___) to the volumetric data in VTK file format.
* `InteractionStyle` = _`NameOfInteractionStyle`_ contains the current interaction style (___str___). Can be set to "_Opacity_", "_Interactive_" or "_Automatic_".
* `Opacity` = _`Value`_ contains the current opacity value (___float___) between 0.0 and 1.0.

## [SagittalCut], [CoronalCut], [TransverseCut]
* `Checked` = _`Bool`_ contains the current state (___bool___) of the slider.
* `Max` = _`Value`_ contains the maximum value (___int___) of the slider.
* `Min` = _`Value`_ contains the minimum value (___int___) of the slider.
* `Text` = _`SomeText`_ contains the label (___str___) of the slider.
* `Value` = _`Value`_ contains the current value (___int___) of the slider.

## \[EEGScene]
* `ContourSmoothing` =_`Radius/StdDev/Iters/PassBand/Angle`_ contains the smoothing parameters for the contour. `Radius` (___int___) and `StdDev` (___float___) are used in the Gaussian smoothing, `Iters` (___int___), `PassBand` (___float___) and `Angle` (___float___) are used in the windowed sinc filtering.
* `ContourValue` = _`Value`_ contains the isosurface value (___int___), which is the greyscale value that will be used to generate contour.
* `ElectrodeChoices` = _`Value1, Value2`_ contains a list of values (___float___) between 0.0 and 1.0 from which the electrode values can choose.
* `FileName` = _`/Relative/Path/To/VTK/File`_ contains the relative path (___str___) to the volumetric data in VTK file format.
* `NSamples` = _`Value`_ contains the last 'Value' number of samples (___int___) that need to be shown in the XY charts when animations are enabled.

## [Animations]
* `Checked` = _`Bool`_ contains the current state (___bool___) of the animations.
* `Max` = _`Value`_ contains the maximum value (___int___) of the animation period in ms.
* `Min` = _`Value`_ contains the minimum value (___int___) of the animation period in ms.
* `Text` = _`SomeText`_ contains the label (___str___) of the animation checkbox.
* `Value` = _`Value`_ contains the current value (___int___) of the animation period in ms.

## [DSASceneAndInteractor]
* `DataSetName` = _`/Relative/Path/To/Datasets*/`_ contains a relative path (___str___) to the
folder containing the datasets. Uses a placeholder * to match any following characters.
* `HueConstant` = _`Value`_ contains the value (___float___) that will be multiplied to the current hue.
* `HueMultiplier` = _`Value`_ contains the value (___float___) that will be subtracted from the current hue.
* `ValueMultiplier` = _`Value`_ contains the value (___float___) that will be multiplied with the current value.

## [DSAScene]
* `FileName` = _`/Relative/Path/To/Dataset/*.png`_ contains a relative path (___str___) to a backup dataset in case the datasets could not automatically be fetched. Uses a placeholder * to match any following characters.
