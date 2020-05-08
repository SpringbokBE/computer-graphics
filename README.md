# Computer Graphics
E016712 - Computer Graphics, Project - Faculty of Engineering and Architecture, UGent

## About
Neuroimaging Visualization Tool using VTK and PyQt.

This tool is able to:

1. Interactively visualize smooth isosurfaces of volumetric CT/MRI data/images along with orthogonal planes (sagittal, coronal, transverse) that slice through the volume.

2. Interactively visualize a smooth brain model on which electrode activity can be simulated by assigning random weights to them and by interpolating the values in between.

3. Visualize a time series of CT/MRI images on which blood flow vs. time is modeled through coloring.

Most of the important settings and file paths are tweaked in the `Neuroviz.ini` file. More information on this file is found [here](Documentation/Neuroviz.md). The application consists of three tabbed widgets that each perform one of the tasks. A detailed description of those scenes can be found [here](#scenes).

## Scenes

The __first scene__ visualizes a head contour, some other contours of brain tissue/lesions and allows to place orthogonal planes that cut through this volumetric data. The active contour, the opacity and the position of the planes can be controlled from the (draggable) dock widget.

The scene comprises three modes:

1. "_Opacity_" mode, in which the full model of the head is shown with variable opacity, to be able to see other tissues.

2. "_Interactive_" mode, in which the full model of the head is shown, but middle-clicking any part of the head will toggle its (variable) opacity.

3. "_Automatic_" mode, in which the full model of the head is shown, but the part of the head facing the camera will be completely removed, such that the underlying tissue can be seen.

Screenshot of "_Basic Visualization_" scene in "_Opacity_", "_Interactive_" and "_Automatic_" mode:

<p style = "float:left;">
<img src = "Documentation/ScreenBasicOpacity.png" width = "290px" alt = "Basic Visualization, Opacity mode">
<img src = "Documentation/ScreenBasicInteractive.png" width = "290px" alt = "Basic Visualization, Interactive mode">
<img src = "Documentation/ScreenBasicAutomatic.png" width = "290px" alt = "Basic Visualization, Automatic mode">
</p>

The __second scene__ simulates electrode behaviour by allowing the user to pick locations on the head on which an electrode is placed. The electrodes are assigned random values and can vary in time if animations are enabled through the (draggable) dock widget. The contour is colored using values that represent the brain activity at those points. An inverse distance weighting (IDW, Shepard) interpolation function is used. The user can control the animation speed by adjusting the "Update interval" on the (draggable) dock widget.

The user can pick electrodes by middle-clicking anywhere on the head. Up to 8 electrodes can be added; picking more than 8 will discard the oldest one. The value of each electrode is shown in XY-charts under the scene.

The __third scene__ merges information from greyscale CT/MRI frames into a single frame in which the variation of the blood flow vs. time is visualized using colors. The HSV color space is used to map time values onto colors.

Different datasets are provided and can be selected through a dropdown menu. When having selected a dataset, the merged image is shown. Due to the variation of the datasets, further tweaking is made possible. The options in the (draggable) dock widget are disabled until the user picks two extreme points by middle-clicking: one with a very low hue (red/yellow/light green) which represents blood flow in the early frames, and one with a very high hue (dark blue/purple) which represents blood flow in the last frames. After having selected two points, the image will be updated and (if correctly picked) will use more of the hue spectrum.

Even further tweaking is made possible by either picking two new points (middle-clicking) or by tweaking the three provided parameters:

1. "_Color range_" or "_Hue multiplier_", which will increase the hue range by multiplying all hue values by this factor. This will probably shift the used spectrum upwards and will result in some clipping.

2. "_Color offset_" or "_Hue constant_", which will decrease the hue values by subtracting this value. This will shift the spectrum back downwards. The hue values are normalized between 0.0 and 1.0. This can result in additional clipping.

3. "_Detail_" or "_Value multiplier_", which will increase the value by multiplying all values (of HSV) with this factor. This will result in a brighter scene in which more details are visible.

Screenshot of "_EEG Visualization_" and "_DSA Visualization_" scene:
<p style = "float:left;">
<img src = "Documentation/ScreenEEG.png" height = "330px" alt = "EEG Visualization">
<img src = "Documentation/ScreenDSA.png" height = "330px" alt = "DSA Visualization">
</p>

## Requirements

Note: these requirements are merely an indication, using different versions of the software required might work. The application is tested on Kubuntu 18.10 using:

* `Python 3.7`
* `VTK 8.2.0 with Python wrapping`
* `PyQt 5.9.2`
* `Numpy 1.16.2`
* `Matplotlib 3.0.3`

## Installation

Run `Code/Main.py`. All configuration is done through the `Code/Neuroviz.ini` file (see [this](Documentation/Neuroviz.md)).

## Folder structure

```
Code              // Contains the scripts.
|- Main.py        // Main application.
|- Neuroviz.ini   // Main configuration file.
|- Neuroviz/      // Contains the scripts.
Data              // Contains datasets used in the application.
|- MHD/           // Currently not in use.
|- PNG/           // Contains PNG slices to be used in all tasks.
|- VTK/           // Contains VTK files to be used in the first and second task.
Documentation     // Contains screenshots and additional information.
UI                // Contains the native .ui files that make up the GUI.
```
## Application structure

To get an overview of all classes and methods, see [this](Documentation/ClassesAndMethods.md).

## Authors

* **Gerbrand De Laender** (gerbrand.delaender@ugent.be)
* **Toon Dilissen** (toon.dilissen@ugent.be)
* **Peter Vercoutter** (peter.vercoutter@ugent.be)
