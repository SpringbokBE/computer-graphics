
//ATTENTION! THE LIBRARIES BELLOW ARE USED WHEN VTK IS BUILT WITH Qt AND FREETYPE SUPPORT!
// IF YOU BUILT VTK WITH ANOTHER CONFIGURATION, EXCLUDE/INCLUDE YOUR NEEDED LIBS.

#ifdef _MSC_VER // VC++ specific
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
#endif

#define vtkRenderingCore_AUTOINIT 4(vtkInteractionStyle,vtkRenderingFreeType,vtkRenderingFreeTypeOpenGL,vtkRenderingOpenGL)
#define vtkRenderingVolume_AUTOINIT 1(vtkRenderingVolumeOpenGL)




#include <vtkConeSource.h>
#include <vtkActor.h>
#include <vtkCamera.h>
#include <vtkContourFilter.h>
#include <vtkOutlineFilter.h>
#include <vtkPolyDataMapper.h>
#include <vtkPolyDataNormals.h>
#include <vtkRenderWindow.h>
#include <vtkRenderWindowInteractor.h>
#include <vtkRenderer.h>
#include <vtkVolume16Reader.h>
#include <vtkStructuredPointsReader.h>
#include <vtkProperty.h>
#include <vtkCamera.h>
#include <vtkSmartPointer.h>






int main( int argc, char *argv[] )
{
	//Create source object 
	vtkSmartPointer<vtkConeSource> cone = vtkSmartPointer<vtkConeSource>::New();
	cone->SetHeight( 3.0 );
	cone->SetRadius( 1.0 );
	cone->SetResolution( 10 );

	//Mapper for the object
	vtkSmartPointer<vtkPolyDataMapper> coneMapper = vtkSmartPointer<vtkPolyDataMapper>::New();
	coneMapper->SetInputConnection( cone->GetOutputPort() );

	//Actor
	vtkSmartPointer<vtkActor> coneActor = vtkSmartPointer<vtkActor>::New();
	coneActor->SetMapper( coneMapper );

	//Renderer
	vtkSmartPointer<vtkRenderer> ren1 = vtkSmartPointer<vtkRenderer>::New();
	ren1->AddActor( coneActor );
	ren1->SetBackground( 0.1, 0.2, 0.4 );

	//Render Rindow
	vtkSmartPointer<vtkRenderWindow> renWin = vtkSmartPointer<vtkRenderWindow>::New();
	renWin->AddRenderer( ren1 );
	renWin->SetSize( 300, 300 );

	//Render the image
	renWin->Render();
	
	//Initialize and start the interactor
	vtkSmartPointer<vtkRenderWindowInteractor> iren = vtkSmartPointer<vtkRenderWindowInteractor>::New();
	iren->SetRenderWindow(renWin);
	iren->Initialize();
	iren->Start();


	return 0;
}

