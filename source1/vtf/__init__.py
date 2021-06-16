import platform


class UnsupportedOS(Exception):
    pass


def is_vtflib_supported():
    platform_name = platform.system()

    if platform_name == "Windows":
        return True
    elif platform_name == "Linux":
        return True
    else:
        return False


if is_vtflib_supported():
    from .import_vtf import import_texture
    from .export_vtf import export_texture
else:
    def import_texture(name, file_object, update=False):
        return


    def export_texture(blender_texture, path, image_format=None, filter_mode=None):
        pass
