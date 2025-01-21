import os
from scripting import *

# Connect to CityEngine
ce = CE()

# Set paths
project_path = ce.toFSPath("Project")
point_file_path = os.path.join(project_path, "data/points.shp")  # Path to point data
terrain_layer_name = "terrain"  # Name of the DEM layer in your scene
cga_rule_path = os.path.join(project_path, "rules", "your_rule.cga")  # Path to CGA file
output_fgdb_path = os.path.join(project_path, "output", "models.gdb")  # Output FGDB path
output_fgdb_name = "MultipatchModels"  # Output feature class name

# Step 1: Import point data
def import_point_data():
    print("Importing point data...")
    ce.importFile(point_file_path, ce.scene)
    print("Point data imported.")

# Step 2: Snap points to DEM terrain
def snap_points_to_terrain():
    print("Snapping points to DEM terrain...")
    # Find the terrain layer
    terrain = ce.getObjectsFrom(ce.scene, ce.isTerrainLayer)[0]
    if terrain.getName() != terrain_layer_name:
        print("Error: Specified terrain layer not found.")
        return
    
    # Iterate over all imported point shapes and snap to terrain
    for shape in ce.getObjectsFrom(ce.scene, ce.isShape):
        if shape.isPoint():
            ce.snapToTerrain(shape)
    print("Points snapped to terrain.")

# Step 3: Assign CGA rule and generate 3D models
def apply_cga_and_generate_models():
    print("Assigning CGA rule and generating 3D models...")
    for shape in ce.getObjectsFrom(ce.scene, ce.isShape):
        if shape.isPoint():
            ce.setRuleFile(shape, cga_rule_path)  # Assign CGA rule
            ce.setRuleParam(shape, "Height", 10)  # Example parameter
            ce.generateModels(shape)  # Generate 3D models
    print("CGA rule applied and 3D models generated.")

# Step 4: Export models to FGDB multipatch
def export_to_fgdb():
    print("Exporting 3D models to FGDB multipatch...")
    export_settings = {
        "outputPath": output_fgdb_path,
        "outputName": output_fgdb_name,
        "format": "FileGDB",
        "includeAttributes": True,
        "multipatch": True
    }
    ce.export(export_settings)
    print(f"Models exported to {output_fgdb_path} as {output_fgdb_name}.")

# Main workflow execution
def main():
    import_point_data()
    snap_points_to_terrain()
    apply_cga_and_generate_models()
    export_to_fgdb()

# Run the script
if __name__ == "__main__":
    main()