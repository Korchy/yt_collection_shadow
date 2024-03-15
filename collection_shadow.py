# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#    https://github.com/Korchy/yt_collection_shadow

import bpy
from bpy.app.handlers import persistent, depsgraph_update_post
from bpy.types import Collection


class CollectionShadow:

    _collections = []

    @classmethod
    def _disable_collection(cls, collection):
        # disable collection in all other View Layers except current
        active_view_layer = bpy.context.window.view_layer
        for scene in bpy.data.scenes:
            for view_layer in scene.view_layers:
                if view_layer != active_view_layer:
                    # get view_layer collection by name
                    layer_collection = cls._layer_collection(
                        view_layer=view_layer,
                        name=collection.name
                    )
                    if layer_collection:
                        layer_collection.exclude = True

    @classmethod
    def _layer_collection(cls, view_layer, name, _layer_collection=None):
        # get view_layer collection by name
        if _layer_collection is None:
            _layer_collection = view_layer.layer_collection
        if _layer_collection.name == name:
            return _layer_collection
        else:
            for l_col in _layer_collection.children:
                if rez := cls._layer_collection(
                        view_layer=view_layer,
                        name=name,
                        _layer_collection=l_col
                ):
                    return rez

    @staticmethod
    def _existed_collections(scene):
        # get existed collections names list
        cols = [col.name for col in bpy.data.collections]
        cols.append(scene.collection.name)
        return cols

    @classmethod
    def on_depsgraph_update_post(cls, scene, depsgraph):
        # check for creating new collection
        if depsgraph.id_type_updated('COLLECTION'):
            for obj in depsgraph.updates:
                if type(obj.id) is Collection:
                    if (obj.id.name not in cls._collections
                            and len(cls._existed_collections(scene=scene)) > len(cls._collections)):
                        # new collection was added
                        cls._disable_collection(
                            collection=bpy.data.collections[obj.id.name]
                        )
            cls._collections = cls._existed_collections(scene=scene)

    @classmethod
    def monitor_start(cls):
        # start monitor creating collections
        if cls.on_depsgraph_update_post not in depsgraph_update_post:
            depsgraph_update_post.append(cls.on_depsgraph_update_post)

    @classmethod
    def monitor_stop(cls):
        # stop monitor creating collections
        if cls.on_depsgraph_update_post in depsgraph_update_post:
            depsgraph_update_post.remove(cls.on_depsgraph_update_post)

    @classmethod
    def register(cls, context):
        # register
        # save existed collections (names list)
        cls._collections = cls._existed_collections(scene=context.scene)
        # monitor creating collections
        cls.monitor_start()
        # re-register on scene reload
        if collection_shadow_on_scene_load_post not in bpy.app.handlers.load_post:
            bpy.app.handlers.load_post.append(collection_shadow_on_scene_load_post)

    @classmethod
    def unregister(cls):
        # unregister
        # stop monitor creating collections
        cls.monitor_stop()
        # remove re-registering on scene reload
        if collection_shadow_on_scene_load_post in bpy.app.handlers.load_post:
            bpy.app.handlers.load_post.remove(collection_shadow_on_scene_load_post)


@persistent
def collection_shadow_on_scene_load_post(*args):
    # on scene reload
    CollectionShadow.monitor_start()
