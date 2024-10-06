import adsk.core
import adsk.fusion
import traceback
import tempfile
import os
import subprocess
import threading
from .commands import fusion_export
from .commands import blender_import

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface
        
        # Get the active document
        product = app.activeProduct
        design = adsk.fusion.Design.cast(product)
        
        if not design:
            ui.messageBox('No active Fusion design')
            return

        # Create a temporary folder
        temp_folder = tempfile.mkdtemp()
        
        # Export visible bodies as STL using FusionExport module
        exported_files = fusion_export.export_stl(design, temp_folder)

        if exported_files:
            # Open the STL files in Blender in a separate thread
            thread = threading.Thread(target=blender_import.open_stl_in_blender, args=(exported_files,))
            thread.start()

            # Remove this line to get rid of the message box
            # ui.messageBox(f'Exported {len(exported_files)} bodies.\nOpening them in Blender...')
        else:
            ui.messageBox('No bodies were exported.')

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))