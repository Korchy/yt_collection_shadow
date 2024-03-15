# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#    https://github.com/Korchy/yt_collection_shadow

import bpy
from bpy.app.handlers import persistent
# from . import collection_shadow_ops
from .addon import Addon
from .collection_shadow import CollectionShadow


bl_info = {
    'name': 'Collection Shadow',
    'category': 'All',
    'author': 'Yuriy Tudgin, Nikita Akimov',
    'version': (1, 0, 1),
    'blender': (4, 0, 0),
    'location': '',
    'doc_url': 'https://github.com/Korchy/yt_collection_shadow',
    'tracker_url': 'https://github.com/Korchy/yt_collection_shadow',
    'description': 'When the user creates new collection, disables it in all other View Layers'
}


@persistent
def collection_shadow_register():
    # register CollectionShadow
    print('collection shadow init')
    if bpy.context and hasattr(bpy.context, 'scene'):
        CollectionShadow.register(context=bpy.context)
    else:
        return 0.25


def register():
    if not Addon.dev_mode():
        print('wait for 5 sec')
        bpy.app.timers.register(
            function=collection_shadow_register,
            # first_interval=0.25
            first_interval=5    # Yuri Tudgin: try to increase init delay to remove excluding collections on load err
        )
    else:
        print('It seems you are trying to use the dev version of the '
              + bl_info['name']
              + ' add-on. It may work not properly. Please download and use the release version')


def unregister():
    if not Addon.dev_mode():
        CollectionShadow.unregister()


if __name__ == '__main__':
    register()
