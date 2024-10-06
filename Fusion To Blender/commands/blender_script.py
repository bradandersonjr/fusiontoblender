import bpy

if "Cube" in bpy.data.objects:
    bpy.data.objects.remove(bpy.data.objects["Cube"], do_unlink=True)
    print("Default cube deleted.")
else:
    print("No default cube found.")
    
# Create a new collection
new_collection = bpy.data.collections.new("Fusion Group")
bpy.context.scene.collection.children.link(new_collection)

print("Importing meshes...")
file_paths = {file_paths}
for file_path in file_paths:
    bpy.ops.wm.stl_import(filepath=file_path, global_scale=0.0254)
    imported_object = bpy.context.selected_objects[0]
    bpy.ops.collection.objects_remove_all()
    new_collection.objects.link(imported_object)
       
    print(f"Imported: {{file_path}} and added to Fusion Group collection")

# Apply flat shading to all objects
for obj in new_collection.objects:
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.shade_flat()
    obj.select_set(False)

print("All meshes imported, scaled down, and flat shading applied!")

# Deselect all objects
bpy.ops.object.select_all(action='DESELECT')

# Select all objects in the new collection
for obj in new_collection.objects:
    obj.select_set(True)

# Set the active object to one of the objects in the collection
if new_collection.objects:
    bpy.context.view_layer.objects.active = new_collection.objects[0]

# Ensure you are in the 3D View area
for area in bpy.context.screen.areas:
    if area.type == 'VIEW_3D':
        for region in area.regions:
            if region.type == 'WINDOW':
                with bpy.context.temp_override(area=area, region=region):
                    bpy.ops.view3d.view_selected(use_all_regions=False)
                break

bpy.context.scene.unit_settings.system = 'IMPERIAL'
bpy.context.scene.unit_settings.scale_length = 1
bpy.context.scene.unit_settings.length_unit = 'INCHES' 