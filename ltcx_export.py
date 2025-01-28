bl_info = {
    "name" : "LTCX Export",
    "blender" : (2, 80, 0),
    "category" : "Import-Export",

}


import bpy
import bmesh

# ExportHelper is a helper class, defines filename and
# invoke() function which calls the file selector.
from bpy_extras.io_utils import ExportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty
from bpy.types import Operator


#Takes a blender node object and returns a nodegroup string
def vert_to_node(vert):
    x = str(vert.co.x)
    y = str(vert.co.y)
    z = str(vert.co.z)
    
    return('\n\t\t<node id="' + str(vert.index) + '" x="' + x + '" y="' + y + '" z="' + z + '"/>')
    
#Takes a blender edge object and returns a beamgroup string
#n1 and n2 represent the vertex indices
def edge_to_beam(edge):
    v1 = str(str(edge.verts[0].index))
    v2 = str(str(edge.verts[1].index))   
    
    return('\n\t\t<beam id="' + str(edge.index) + '" n1="' + v1 + '" n2="' + v2 + '"/>')

def ltcx_settings(name, units, type):
    return('\n<graph id="0" name="' + name + '" units="' + units + '" type="' + type + '">')

#use this section to write to file
def write_some_data(bm, context, filepath, type):
    print("running ltcx exporter...")
    f = open(filepath, 'w', encoding='utf-8')
    
    #Write Header and settings
    f.write('<?xml version="1.0" encoding="utf-8"?>')
    f.write('\n<!---->')
    f.write(ltcx_settings("cube unit", type, "rnd"))
    
    
    vertCount = 0
    edgeCount = 0
    #Write lines for Nodes    
    f.write('\n\t<nodegroup>')
    for v in bm.verts:
        f.write(vert_to_node(v))
        vertCount+1  
    f.write('\n\t</nodegroup>')
    
    
    #Write lines for beams
    f.write('\n\t<beamgroup>')
    for e in bm.edges:
        f.write(edge_to_beam(e))
        edgeCount+1    
    f.write('\n\t</beamgroup>')
    
    f.write('\n</graph>')
    
    f.close()

    return {'FINISHED'}


class ExportLtcx(Operator, ExportHelper):
    """This appears in the tooltip of the operator and in the generated docs"""
    bl_idname = "export_ltcx.lattice"  # important since its how bpy.ops.import_test.some_data is constructed
    bl_label = "Export ltcx file"

    # ExportHelper mix-in class uses this.
    filename_ext = ".ltcx"

    filter_glob: StringProperty(
        default="*.ltcx",
        options={'HIDDEN'},
        maxlen=255,  # Max internal buffer length, longer would be clamped.
    )

    
    #Example property with dropdown menu
    type: EnumProperty(
        name="Units",
        description="Choose lattice units",
        items=(
            ('mm', "mm", "Sets units to millimeters"),
            ('cm', "cm", "Sets units to centimeters"),
            ('in', "in", "Sets units to inches"),
        ),
        default='mm',
    )
    

    def execute(self, context):
        #Get the currently selected object
        me = bpy.context.object.data
        
        #Create a bmesh from the currently selected mesh, this helps get edge and vertex data
        bm = bmesh.new()
        bm.from_mesh(me)

        return write_some_data(bm, context, self.filepath, self.type)


# Only needed if you want to add into a dynamic menu
def menu_func_export(self, context):
    self.layout.operator(ExportLtcx.bl_idname, text="LTCX file (.ltcx)")


# Register and add to the "file selector" menu (required to use F3 search "Text Export Operator" for quick access).
def register():
    bpy.utils.register_class(ExportLtcx)
    bpy.types.TOPBAR_MT_file_export.append(menu_func_export)


def unregister():
    bpy.utils.unregister_class(ExportLtcx)
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)


if __name__ == "__main__":
    register()

    # test call
    bpy.ops.export_ltcx.lattice('INVOKE_DEFAULT')
