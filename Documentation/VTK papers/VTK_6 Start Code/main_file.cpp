/**************************************************************************
 Simple VTK Medical Application

 Author: Danilo Babin
 File name: "main_file.cpp"
***************************************************************************/



#define vtkRenderingCore_AUTOINIT 4(vtkInteractionStyle,vtkRenderingFreeType,vtkRenderingFreeTypeOpenGL,vtkRenderingOpenGL)
#define vtkRenderingVolume_AUTOINIT 1(vtkRenderingVolumeOpenGL)

//ATTENTION! THE LIBRARIES BELLOW ARE USED WHEN VTK IS BUILT WITH Qt AND FREETYPE SUPPORT!
// IF YOU BUILT VTK WITH ANOTHER CONFIGURATION, EXCLUDE/INCLUDE YOUR NEEDED LIBS.

#pragma comment(lib,"vtkalglib-6.0.lib")
#pragma comment(lib,"vtkChartsCore-6.0.lib")
#pragma comment(lib,"vtkCommonColor-6.0.lib")
#pragma comment(lib,"vtkCommonComputationalGeometry-6.0.lib")
#pragma comment(lib,"vtkCommonCore-6.0.lib")
#pragma comment(lib,"vtkCommonDataModel-6.0.lib")
#pragma comment(lib,"vtkCommonExecutionModel-6.0.lib")
#pragma comment(lib,"vtkCommonMath-6.0.lib")
#pragma comment(lib,"vtkCommonMisc-6.0.lib")
#pragma comment(lib,"vtkCommonSystem-6.0.lib")
#pragma comment(lib,"vtkCommonTransforms-6.0.lib")
#pragma comment(lib,"vtkDICOMParser-6.0.lib")
#pragma comment(lib,"vtkDomainsChemistry-6.0.lib")
#pragma comment(lib,"vtkexoIIc-6.0.lib")
#pragma comment(lib,"vtkexpat-6.0.lib")
#pragma comment(lib,"vtkFiltersAMR-6.0.lib")
#pragma comment(lib,"vtkFiltersCore-6.0.lib")
#pragma comment(lib,"vtkFiltersExtraction-6.0.lib")
#pragma comment(lib,"vtkFiltersFlowPaths-6.0.lib")
#pragma comment(lib,"vtkFiltersGeneral-6.0.lib")
#pragma comment(lib,"vtkFiltersGeneric-6.0.lib")
#pragma comment(lib,"vtkFiltersGeometry-6.0.lib")
#pragma comment(lib,"vtkFiltersHybrid-6.0.lib")
#pragma comment(lib,"vtkFiltersHyperTree-6.0.lib")
#pragma comment(lib,"vtkFiltersImaging-6.0.lib")
#pragma comment(lib,"vtkFiltersModeling-6.0.lib")
#pragma comment(lib,"vtkFiltersParallel-6.0.lib")
#pragma comment(lib,"vtkFiltersParallelImaging-6.0.lib")
#pragma comment(lib,"vtkFiltersProgrammable-6.0.lib")
#pragma comment(lib,"vtkFiltersSelection-6.0.lib")
#pragma comment(lib,"vtkFiltersSources-6.0.lib")
#pragma comment(lib,"vtkFiltersStatistics-6.0.lib")
#pragma comment(lib,"vtkFiltersTexture-6.0.lib")
#pragma comment(lib,"vtkFiltersVerdict-6.0.lib")
#pragma comment(lib,"vtkfreetype-6.0.lib")
#pragma comment(lib,"vtkftgl-6.0.lib")
#pragma comment(lib,"vtkGeovisCore-6.0.lib")
#pragma comment(lib,"vtkgl2ps-6.0.lib")
#pragma comment(lib,"vtkGUISupportQt-6.0.lib")
#pragma comment(lib,"vtkGUISupportQtOpenGL-6.0.lib")
#pragma comment(lib,"vtkGUISupportQtSQL-6.0.lib")
#pragma comment(lib,"vtkGUISupportQtWebkit-6.0.lib")
#pragma comment(lib,"vtkhdf5-6.0.lib")
#pragma comment(lib,"vtkhdf5_hl-6.0.lib")
#pragma comment(lib,"vtkImagingColor-6.0.lib")
#pragma comment(lib,"vtkImagingCore-6.0.lib")
#pragma comment(lib,"vtkImagingFourier-6.0.lib")
#pragma comment(lib,"vtkImagingGeneral-6.0.lib")
#pragma comment(lib,"vtkImagingHybrid-6.0.lib")
#pragma comment(lib,"vtkImagingMath-6.0.lib")
#pragma comment(lib,"vtkImagingMorphological-6.0.lib")
#pragma comment(lib,"vtkImagingSources-6.0.lib")
#pragma comment(lib,"vtkImagingStatistics-6.0.lib")
#pragma comment(lib,"vtkImagingStencil-6.0.lib")
#pragma comment(lib,"vtkInfovisCore-6.0.lib")
#pragma comment(lib,"vtkInfovisLayout-6.0.lib")
#pragma comment(lib,"vtkInteractionImage-6.0.lib")
#pragma comment(lib,"vtkInteractionStyle-6.0.lib")
#pragma comment(lib,"vtkInteractionWidgets-6.0.lib")
#pragma comment(lib,"vtkIOAMR-6.0.lib")
#pragma comment(lib,"vtkIOCore-6.0.lib")
#pragma comment(lib,"vtkIOEnSight-6.0.lib")
#pragma comment(lib,"vtkIOExodus-6.0.lib")
#pragma comment(lib,"vtkIOExport-6.0.lib")
#pragma comment(lib,"vtkIOGeometry-6.0.lib")
#pragma comment(lib,"vtkIOImage-6.0.lib")
#pragma comment(lib,"vtkIOImport-6.0.lib")
#pragma comment(lib,"vtkIOInfovis-6.0.lib")
#pragma comment(lib,"vtkIOLegacy-6.0.lib")
#pragma comment(lib,"vtkIOLSDyna-6.0.lib")
#pragma comment(lib,"vtkIOMINC-6.0.lib")
#pragma comment(lib,"vtkIOMovie-6.0.lib")
#pragma comment(lib,"vtkIONetCDF-6.0.lib")
#pragma comment(lib,"vtkIOParallel-6.0.lib")
#pragma comment(lib,"vtkIOPLY-6.0.lib")
#pragma comment(lib,"vtkIOSQL-6.0.lib")
#pragma comment(lib,"vtkIOVideo-6.0.lib")
#pragma comment(lib,"vtkIOXML-6.0.lib")
#pragma comment(lib,"vtkIOXMLParser-6.0.lib")
#pragma comment(lib,"vtkjpeg-6.0.lib")
#pragma comment(lib,"vtkjsoncpp-6.0.lib")
#pragma comment(lib,"vtklibxml2-6.0.lib")
#pragma comment(lib,"vtkmetaio-6.0.lib")
#pragma comment(lib,"vtkNetCDF-6.0.lib")
#pragma comment(lib,"vtkNetCDF_cxx-6.0.lib")
#pragma comment(lib,"vtkoggtheora-6.0.lib")
#pragma comment(lib,"vtkParallelCore-6.0.lib")
#pragma comment(lib,"vtkpng-6.0.lib")
#pragma comment(lib,"vtkproj4-6.0.lib")
#pragma comment(lib,"vtkRenderingAnnotation-6.0.lib")
#pragma comment(lib,"vtkRenderingContext2D-6.0.lib")
#pragma comment(lib,"vtkRenderingCore-6.0.lib")
#pragma comment(lib,"vtkRenderingFreeType-6.0.lib")
#pragma comment(lib,"vtkRenderingFreeTypeOpenGL-6.0.lib")
#pragma comment(lib,"vtkRenderingGL2PS-6.0.lib")
#pragma comment(lib,"vtkRenderingHybridOpenGL-6.0.lib")
#pragma comment(lib,"vtkRenderingImage-6.0.lib")
#pragma comment(lib,"vtkRenderingLabel-6.0.lib")
#pragma comment(lib,"vtkRenderingLOD-6.0.lib")
#pragma comment(lib,"vtkRenderingOpenGL-6.0.lib")
#pragma comment(lib,"vtkRenderingQt-6.0.lib")
#pragma comment(lib,"vtkRenderingVolume-6.0.lib")
#pragma comment(lib,"vtkRenderingVolumeAMR-6.0.lib")
#pragma comment(lib,"vtkRenderingVolumeOpenGL-6.0.lib")
#pragma comment(lib,"vtksqlite-6.0.lib")
#pragma comment(lib,"vtksys-6.0.lib")
#pragma comment(lib,"vtktiff-6.0.lib")
#pragma comment(lib,"vtkverdict-6.0.lib")
#pragma comment(lib,"vtkViewsContext2D-6.0.lib")
#pragma comment(lib,"vtkViewsCore-6.0.lib")
#pragma comment(lib,"vtkViewsGeovis-6.0.lib")
#pragma comment(lib,"vtkViewsInfovis-6.0.lib")
#pragma comment(lib,"vtkViewsQt-6.0.lib")
#pragma comment(lib,"vtkzlib-6.0.lib")


#include <vtkSmartPointer.h>
#include <vtkActor.h>
#include <vtkInteractorStyleTrackballCamera.h>
#include <vtkPolyDataMapper.h>
#include <vtkRenderWindow.h>
#include <vtkRenderWindowInteractor.h>
#include <vtkRenderer.h>
#include <vtkSphereSource.h>
#include <vtkGenericDataObjectReader.h>
#include <vtkImageData.h>
#include <vtkContourFilter.h>
#include <vtkProperty.h>
#include <vtkImagePlaneWidget.h>
#include <vtkCommand.h>
#include <vtkTextActor.h>
#include <vtkTextProperty.h>
#include <vtkPointPicker.h>





#include "MyImage3D.h"
//#include <iostream>
//#include <strstream>
//#include <fstream>
//#include <assert.h>
//#include <stdlib.h>
#include <sstream>




using namespace std;


int main()
{	
	//Example of creating a new 3-D image and initializing it with 0:
	MyImage3D image3d;
	image3d.Set(10,10,10);
	image3d.FillInWith(0);
	cout<<"3-D image created and filled with 0."<<endl;
	//----------------------------------------------------------------------------------------------

	//Put some voxel values in the image:
	image3d.Index(1,2,3) = 15;
	image3d.Index(4,2,2) = 5;
	image3d.Index(8,6,3) = 7;
	image3d.Index(5,6,8) = 20000;
	image3d.Index(3,3,3) = 1;
	image3d.Index(1,1,1) = 15;

	//Example of going through the whole 3-D image and finding the maximum value:
	unsigned short maximum;
	maximum = image3d.Index(0,0,0);
	int dims_xyz[3];
	image3d.vtk_image_data->GetDimensions(dims_xyz);
	for(int s=0; s<dims_xyz[2]; s++)
	{
		for(int r=0; r<dims_xyz[1]; r++)
		{
			for(int c=0; c<dims_xyz[0]; c++)
			{
				if(image3d.Index(s,r,c)>maximum) maximum = image3d.Index(s,r,c);
			}
		}
	}
	cout<<"Maximum value in the 3-D image is "<<((int)(maximum))<<"."<<endl;
	//----------------------------------------------------------------------------------------------

	//----- General VTK part -----
	vtkSmartPointer<vtkRenderer> renderer = vtkSmartPointer<vtkRenderer>::New();
	vtkSmartPointer<vtkRenderWindow> renWin = vtkSmartPointer<vtkRenderWindow>::New();
	renWin->AddRenderer(renderer);
	vtkSmartPointer<vtkRenderWindowInteractor> iren = vtkSmartPointer<vtkRenderWindowInteractor>::New();
	iren->SetRenderWindow(renWin);	
	vtkSmartPointer<vtkInteractorStyleTrackballCamera> style = vtkSmartPointer<vtkInteractorStyleTrackballCamera>::New();
	iren->SetInteractorStyle(style);
	renWin->SetSize(900, 900);

	//----- Print maximum value on the screen -----
	vtkSmartPointer<vtkTextActor> menu_text_actor = vtkSmartPointer<vtkTextActor>::New();
	vtkTextProperty* text_property = menu_text_actor->GetTextProperty();
	text_property->SetFontFamilyToCourier();
	text_property->ShadowOn();
	text_property->SetLineSpacing(1.0);
	text_property->SetFontSize(15);
	text_property->SetColor(0.4, 1.0, 0.0);
	text_property->SetShadowOffset(0.5, 0.5);
	menu_text_actor->SetDisplayPosition(5, 50);
	std::ostringstream text;
	//std::string text;
	//text.str
	//std::string text;
	//text.append("maximum = ");//text.((int)(maximum))<<endl;
	text<<"maximum = "<<((int)(maximum))<<endl;
	text<<ends;
	menu_text_actor->SetInput(text.str().c_str());
	renderer->AddActor(menu_text_actor);
	//-----

	//===== START THE RENDERING =====
	iren->Initialize();
	renWin->Render();	
	iren->Start();
	//=====

	return 0;
}
