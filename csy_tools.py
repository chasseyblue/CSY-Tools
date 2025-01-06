bl_info = {
    "name": "CSY Tools (N-Panel)",
    "blender": (2, 83, 0),
    "category": "3D View",
    "description": "Tools for creating bounds, exporting objects, and managing mesh data in the N-Panel",
    "author": "chasseyblue.com",
    "version": (1, 8, 0),
    "location": "View3D > Sidebar > CSY Tools",
    "support": "COMMUNITY",
}

import bpy
import bmesh
from mathutils import Vector


class OBJECT_OT_CreateSimpleBound(bpy.types.Operator):
    """Create a Simple Bounding Box"""
    bl_idname = "csy_tools.create_simple_bound"
    bl_label = "Create BOUND"
    bl_options = {'REGISTER', 'UNDO'}

    # Property for minimal loop cuts
    loop_cuts: bpy.props.IntProperty(
        name="Loop Cuts",
        default=1,
        min=0,
        max=5,
        description="Number of loop cuts for basic geometry",
    )

    def execute(self, context):
        print("Starting simple BOUND creation...")
        reference = context.object
        if not reference:
            self.report({'WARNING'}, "No active object selected.")
            return {'CANCELLED'}

        # Ensure the reference object has valid geometry
        if not reference.data or not hasattr(reference.data, 'polygons'):
            self.report({'WARNING'}, "Selected object does not have valid geometry.")
            return {'CANCELLED'}

        # Get bounding box dimensions
        bbox_corners = [reference.matrix_world @ Vector(corner) for corner in reference.bound_box]
        min_corner = Vector(map(min, zip(*bbox_corners)))
        max_corner = Vector(map(max, zip(*bbox_corners)))
        bbox_center = (min_corner + max_corner) / 2
        bbox_size = max_corner - min_corner

        # Add a cube
        bpy.ops.mesh.primitive_cube_add(location=bbox_center)
        cube = context.object

        # Rename the cube
        cube.name = "BOUND"
        cube.scale = bbox_size / 2

        if self.loop_cuts > 0:
            # Switch to Edit Mode
            bpy.ops.object.mode_set(mode='EDIT')
            print("Entering Edit Mode...")

            # Add minimal loop cuts
            mesh = bmesh.from_edit_mesh(cube.data)
            print(f"Adding {self.loop_cuts} loop cuts along each axis...")
            for _ in range(self.loop_cuts):
                bmesh.ops.subdivide_edges(
                    mesh,
                    edges=[e for e in mesh.edges if abs(e.verts[0].co.y - e.verts[1].co.y) < 0.0001 and abs(e.verts[0].co.z - e.verts[1].co.z) < 0.0001],
                    cuts=1,
                )
                bmesh.ops.subdivide_edges(
                    mesh,
                    edges=[e for e in mesh.edges if abs(e.verts[0].co.x - e.verts[1].co.x) < 0.0001 and abs(e.verts[0].co.z - e.verts[1].co.z) < 0.0001],
                    cuts=1,
                )
                bmesh.ops.subdivide_edges(
                    mesh,
                    edges=[e for e in mesh.edges if abs(e.verts[0].co.x - e.verts[1].co.x) < 0.0001 and abs(e.verts[0].co.y - e.verts[1].co.y) < 0.0001],
                    cuts=1,
                )
            bmesh.update_edit_mesh(cube.data)
            bpy.ops.object.mode_set(mode='OBJECT')
            print("Exiting Edit Mode.")

        self.report({'INFO'}, f"Simple BOUND created with {self.loop_cuts} loop cuts.")
        print("Simple BOUND creation complete.")
        return {'FINISHED'}


class OBJECT_OT_ApplyOriginAndTransform(bpy.types.Operator):
    """Apply Origin to 3D Cursor and Apply Transformations"""
    bl_idname = "csy_tools.apply_origin_and_transform"
    bl_label = "Apply Origin and Transformations"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        print("Applying origin to 3D cursor and transformations...")
        obj = context.object
        if not obj:
            self.report({'WARNING'}, "No active object selected.")
            return {'CANCELLED'}

        # Set origin to 3D cursor
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')
        print("Origin set to 3D cursor.")

        # Apply all transformations
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
        print("All transformations applied.")

        self.report({'INFO'}, "Origin and transformations applied for export.")
        return {'FINISHED'}


class OBJECT_OT_ApplyRotationScaleAndSetOrigin(bpy.types.Operator):
    """Apply Rotation & Scale and Set Origin to Center of Mass (Surface)"""
    bl_idname = "csy_tools.apply_rotation_scale_and_origin"
    bl_label = "Apply Rotation & Scale + Origin"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        print("Applying rotation & scale and setting origin to center of mass (surface)...")
        obj = context.object
        if not obj:
            self.report({'WARNING'}, "No active object selected.")
            return {'CANCELLED'}

        # Apply rotation & scale
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
        print("Applied rotation and scale.")

        # Set origin to center of mass (surface)
        bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS', center='MEDIAN')
        print("Set origin to center of mass (surface).")

        self.report({'INFO'}, "Applied rotation & scale and set origin to center of mass.")
        return {'FINISHED'}


class OBJECT_OT_SetMaterialSpecular(bpy.types.Operator):
    """Set Specular for All Materials to 0.500"""
    bl_idname = "csy_tools.set_material_specular"
    bl_label = "Set Specular to 0.500"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        print("Setting specular to 0.500 for all materials...")
        for obj in context.selected_objects:
            if obj.type == 'MESH':
                for mat in obj.data.materials:
                    if mat and mat.use_nodes:
                        for node in mat.node_tree.nodes:
                            if node.type == 'BSDF_PRINCIPLED':
                                node.inputs['Specular'].default_value = 0.500
                                print(f"Updated specular for material '{mat.name}' in object '{obj.name}'.")
        self.report({'INFO'}, "Specular set to 0.500 for all selected objects.")
        return {'FINISHED'}


class OBJECT_OT_RenameUVAndVertexColors(bpy.types.Operator):
    """Rename UV Maps and Vertex Colors"""
    bl_idname = "csy_tools.rename_uv_and_vertex_colors"
    bl_label = "Rename UVs and VTX Colors"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        print("Renaming UV maps and vertex colors...")
        for obj in context.selected_objects:
            if obj.type == 'MESH':
                # Rename UV maps
                for uv_layer in obj.data.uv_layers:
                    uv_layer.name = "UV"
                    print(f"Renamed UV map for {obj.name} to 'UV'.")

                # Rename Vertex Colors
                for vcol in obj.data.vertex_colors:
                    vcol.name = "VTX"
                    print(f"Renamed Vertex Color for {obj.name} to 'VTX'.")

        self.report({'INFO'}, "Renamed UVs and vertex colors for selected objects.")
        return {'FINISHED'}


class OBJECT_OT_SanityCheckCollection(bpy.types.Operator):
    """Sanity check for required objects in 'Collection'"""
    bl_idname = "csy_tools.sanity_check_collection"
    bl_label = "Sanity Check Collection"
    bl_options = {'REGISTER', 'UNDO'}

    required_objects = [
        "BODY_H",
        "HLIGHT_L",
        "RLIGHT_L",
        "SHADOW_H",
        "TLIGHT_L",
        "WHL0_H",
        "WHL1_H",
        "WHL2_H",
        "WHL3_H",
    ]

    def execute(self, context):
        print("Performing sanity check for 'Collection'...")
        collection_name = "Collection"
        missing_objects = []

        # Check if the 'Collection' exists
        if collection_name not in bpy.data.collections:
            self.report({'ERROR'}, f"'{collection_name}' not found in the scene.")
            return {'CANCELLED'}

        collection = bpy.data.collections[collection_name]

        # Collect names of all objects in 'Collection'
        collection_object_names = [obj.name for obj in collection.objects]

        # Check for missing required objects
        for required_name in self.required_objects:
            if required_name not in collection_object_names:
                missing_objects.append(required_name)

        if missing_objects:
            self.report(
                {'WARNING'},
                f"Sanity check failed. Missing objects: {', '.join(missing_objects)}"
            )
            return {'CANCELLED'}

        self.report({'INFO'}, "Sanity check passed. All required objects are present.")
        return {'FINISHED'}


class CSY_PT_ToolsPanel(bpy.types.Panel):
    """CSY Tools Panel in N-Panel"""
    bl_label = "CSY Tools"
    bl_idname = "CSY_PT_tools_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "CSY Tools"

    def draw(self, context):
        layout = self.layout
        layout.label(text="Bound Tools")
        layout.operator(OBJECT_OT_CreateSimpleBound.bl_idname, text="Create BOUND")
        layout.separator()
        layout.label(text="Export Tools")
        layout.operator(OBJECT_OT_ApplyOriginAndTransform.bl_idname, text="Apply Origin and Transformations")
        layout.operator(OBJECT_OT_ApplyRotationScaleAndSetOrigin.bl_idname, text="Apply Rotation & Scale + Origin")
        layout.operator(OBJECT_OT_SanityCheckCollection.bl_idname, text="Sanity Check Collection")
        layout.separator()
        layout.label(text="Material Tools")
        layout.operator(OBJECT_OT_SetMaterialSpecular.bl_idname, text="Set Specular to 0.500")
        layout.separator()
        layout.label(text="Mesh Tools")
        layout.operator(OBJECT_OT_RenameUVAndVertexColors.bl_idname, text="Rename UVs and VTX Colors")


# Register the add-on
def register():
    bpy.utils.register_class(OBJECT_OT_CreateSimpleBound)
    bpy.utils.register_class(OBJECT_OT_ApplyOriginAndTransform)
    bpy.utils.register_class(OBJECT_OT_ApplyRotationScaleAndSetOrigin)
    bpy.utils.register_class(OBJECT_OT_SetMaterialSpecular)
    bpy.utils.register_class(OBJECT_OT_RenameUVAndVertexColors)
    bpy.utils.register_class(OBJECT_OT_SanityCheckCollection)
    bpy.utils.register_class(CSY_PT_ToolsPanel)


# Unregister the add-on
def unregister():
    bpy.utils.unregister_class(OBJECT_OT_CreateSimpleBound)
    bpy.utils.unregister_class(OBJECT_OT_ApplyOriginAndTransform)
    bpy.utils.unregister_class(OBJECT_OT_ApplyRotationScaleAndSetOrigin)
    bpy.utils.unregister_class(OBJECT_OT_SetMaterialSpecular)
    bpy.utils.unregister_class(OBJECT_OT_RenameUVAndVertexColors)
    bpy.utils.unregister_class(OBJECT_OT_SanityCheckCollection)
    bpy.utils.unregister_class(CSY_PT_ToolsPanel)


if __name__ == "__main__":
    register()
