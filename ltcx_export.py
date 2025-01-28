import bpy


#Takes a blender node object and returns a nodegroup string
def vert_to_node(node, id):
    return('\n\t\t<node id="' + str(id) + '" x="-1" y="-1" z="-1"/>')
    
#Takes a blender edge object and returns a beamgroup string
def edge_to_beam(beam, id):
    return('\n\t\t<beam id="' + str(id) + '" n1="0" n2="1"/>')

def ltcx_settings(name, units, type):
    return('\n<graph id="0" name="' + name + '" units="' + units + '" type="' + type + '">')

#use this section to write to file
def write_some_data(context, filepath, type):
    print("running ltcx exporter...")
    f = open(filepath, 'w', encoding='utf-8')
    
    #Write Header and settings
    f.write('<?xml version="1.0" encoding="utf-8"?>')
    f.write('\n<!---->')
    f.write(ltcx_settings("cube unit", type, "rnd"))
    
    
    #Write lines for Nodes
    f.write('\n\t<nodegroup>')
    for x in range(5):
        f.write(vert_to_node(1,x))   
    f.write('\n\t</nodegroup>')
    
    #Write lines for beams
    f.write('\n\t<beamgroup>')
    for x in range(5):
        f.write(edge_to_beam(1,x))   
    f.write('\n\t</beamgroup>')
    
    f.write('\n</graph>')
    
    f.close()

    return {'FINISHED'}


# ExportHelper is a helper class, defines filename and
# invoke() function which calls the file selector.
from bpy_extras.io_utils import ExportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty
from bpy.types import Operator


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



    # List of operator properties, the attributes will be assigned
    # to the class instance from the operator settings before calling.
    use_setting: BoolProperty(
        name="Example Boolean",
        description="Example Tooltip",
        default=True,
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
        return write_some_data(context, self.filepath, self.type)


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
