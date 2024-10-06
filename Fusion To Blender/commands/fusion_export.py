import adsk.core
import adsk.fusion
import traceback
import os
import json
import multiprocessing

def apply_stl_options(stl_export_options, stl_options):
    # Force set unit
    stl_export_options.unit = (adsk.fusion.DistanceUnits.InchDistanceUnits 
                               if stl_options['unit'] == 'Inch' 
                               else adsk.fusion.DistanceUnits.CentimeterDistanceUnits)
    
    # Force set mesh refinement
    refinement_value = getattr(adsk.fusion.MeshRefinementSettings, f"MeshRefinement{stl_options['refinement']}")
    stl_export_options.meshRefinement = refinement_value
    
    # Force set other numerical values
    stl_export_options.surfaceDeviation = float(stl_options['surfaceDeviation'])
    stl_export_options.normalDeviation = float(stl_options['normalDeviation'])
    stl_export_options.maximumEdgeLength = float(stl_options['maxEdgeLength'])
    stl_export_options.aspectRatio = float(stl_options['aspectRatio'])

    print(f"Forcefully applied STL export options:")
    print(f"Unit: {stl_export_options.unit}")
    print(f"Mesh Refinement: {stl_export_options.meshRefinement}")
    print(f"Surface Deviation: {stl_export_options.surfaceDeviation}")
    print(f"Normal Deviation: {stl_export_options.normalDeviation}")
    print(f"Maximum Edge Length: {stl_export_options.maximumEdgeLength}")
    print(f"Aspect Ratio: {stl_export_options.aspectRatio}")

def export_stl(design, temp_folder, callback=None):
    app = adsk.core.Application.get()
    ui = app.userInterface
    try:
        root_comp = design.rootComponent
        export_mgr = design.exportManager
        
        all_bodies = []
        traverseComponent(root_comp, all_bodies)
        
        visible_bodies = [body for body in all_bodies if body.isVisible]
        
        # Load STL export options
        script_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        json_path = os.path.join(script_dir, 'stl_export_options.json')
        with open(json_path, 'r') as f:
            stl_options = json.load(f)
        print(f"Loaded STL export options: {stl_options}")
        
        # Create progress dialog
        progress = ui.createProgressDialog()
        progress.cancelButtonText = 'Cancel'
        progress.isBackgroundTranslucent = False
        progress.isCancelButtonShown = True
        progress.show('Fusion To Blender', 'Progress: %p%', 0, 100)

        exported_files = []
        total_bodies = len(visible_bodies)
        for i, body in enumerate(visible_bodies):
            if progress.wasCancelled:
                break
            
            file_name = os.path.join(temp_folder, f"{body.name}.stl")
            stl_export_options = export_mgr.createSTLExportOptions(body, file_name)
            stl_export_options.sendToPrintUtility = False
            
            # Apply STL export options
            apply_stl_options(stl_export_options, stl_options)
            
            export_mgr.execute(stl_export_options)
            exported_files.append(file_name)
            
            if i % 5 == 0 or i == total_bodies - 1:  # Update progress every 5 bodies or on the last body
                progress.progressValue = int((i + 1) / total_bodies * 100)
        
        progress.hide()
        return exported_files
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
        return []

def export_body(body, file_name, stl_options, export_mgr):
    stl_export_options = export_mgr.createSTLExportOptions(body, file_name)
    stl_export_options.sendToPrintUtility = False
    
    # Apply STL export options
    stl_export_options.unit = adsk.fusion.DistanceUnits.InchDistanceUnits if stl_options['unit'] == 'Inch' else adsk.fusion.DistanceUnits.CentimeterDistanceUnits
    stl_export_options.meshRefinement = getattr(adsk.fusion.MeshRefinementSettings, f"MeshRefinement{stl_options['refinement']}")
    stl_export_options.surfaceDeviation = float(stl_options['surfaceDeviation'])
    stl_export_options.normalDeviation = float(stl_options['normalDeviation'])
    stl_export_options.maximumEdgeLength = float(stl_options['maxEdgeLength'])
    stl_export_options.aspectRatio = float(stl_options['aspectRatio'])
    
    export_mgr.execute(stl_export_options)
    return file_name

def traverseComponent(component, bodies_list):
    bodies_list.extend(component.bRepBodies)
    for occurrence in component.occurrences:
        traverseComponent(occurrence.component, bodies_list)