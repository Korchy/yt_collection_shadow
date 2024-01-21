# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#    https://github.com/Korchy/yt_collection_shadow

from bpy.types import Operator
from bpy.utils import register_class, unregister_class
from .collection_shadow import CollectionShadow


class COLLECTION_SHADOW_OT_main(Operator):
    bl_idname = 'collection_shadow.disable_collection'
    bl_label = 'Disable collection'
    bl_description = 'Disable collection'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        CollectionShadow.disable_collection(
           context=context
        )
        return {'FINISHED'}

    @classmethod
    def poll(cls, context):
        return True


def register():
    register_class(COLLECTION_SHADOW_OT_main)


def unregister():
    unregister_class(COLLECTION_SHADOW_OT_main)
