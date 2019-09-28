# Armory 3D Engine
# https://github.com/armory3d/armory
bl_info = {
    "name": "Armory",
    "category": "Render",
    "location": "Properties -> Render -> Armory Player",
    "description": "3D Game Engine for Blender",
    "author": "Armory3D.org",
    "version": (2019, 9, 0),
    "blender": (2, 80, 0),
    "wiki_url": "https://github.com/armory3d/armory/wiki",
    "tracker_url": "https://github.com/armory3d/armory/issues"
}

import os
import sys
import stat
import shutil
import webbrowser
import subprocess
import threading
import bpy
import platform
from bpy.types import Operator, AddonPreferences
from bpy.props import *
from bpy.app.handlers import persistent

def get_os():
    s = platform.system()
    if s == 'Windows':
        return 'win'
    elif s == 'Darwin':
        return 'mac'
    else:
        return 'linux'

class ArmoryAddonPreferences(AddonPreferences):
    bl_idname = __name__

    def sdk_path_update(self, context):
        if self.skip_update:
            return
        self.skip_update = True
        self.sdk_path = bpy.path.reduce_dirs([bpy.path.abspath(self.sdk_path)])[0] + '/'
        if ArmAddonStartButton.running:
            return
        bpy.ops.arm_addon.start()

    def ide_path_update(self, context):
        if self.skip_update:
            return
        self.skip_update = True
        self.ide_path = bpy.path.reduce_dirs([bpy.path.abspath(self.ide_path)])[0]

    def ffmpeg_path_update(self, context):
        if self.skip_update or self.ffmpeg_path == '':
            return
        self.skip_update = True
        self.ffmpeg_path = bpy.path.reduce_dirs([bpy.path.abspath(self.ffmpeg_path)])[0]

    def renderdoc_path_update(self, context):
        if self.skip_update or self.renderdoc_path == '':
            return
        self.skip_update = True
        self.renderdoc_path = bpy.path.reduce_dirs([bpy.path.abspath(self.renderdoc_path)])[0]

    sdk_bundled: BoolProperty(name="Bundled SDK", default=True)
    sdk_path: StringProperty(name="SDK Path", subtype="FILE_PATH", update=sdk_path_update, default="")
    ide_path: StringProperty(name="VS Code Path", subtype="FILE_PATH", update=ide_path_update, default="", description="Path to VS Code or Kode Studio folder")
    show_advanced: BoolProperty(name="Show Advanced", default=False)
    code_editor: EnumProperty(
        items = [('kodestudio', 'VS Code', 'kodestudio'),
                 ('default', 'System Default', 'default')],
        name="Code Editor", default='kodestudio', description='Use this editor for editing scripts')
    ui_scale: FloatProperty(name='UI Scale', description='Adjust UI scale for Armory tools', default=1.0, min=1.0, max=4.0)
    khamake_threads: IntProperty(name='Khamake Threads', description='Allow Khamake to spawn multiple processes for faster builds', default=4, min=1)
    compilation_server: BoolProperty(name='Compilation Server', description='Allow Haxe to create a local compilation server for faster builds', default=True)
    renderdoc_path: StringProperty(name="RenderDoc Path", description="Binary path", subtype="FILE_PATH", update=renderdoc_path_update, default="")
    ffmpeg_path: StringProperty(name="FFMPEG Path", description="Binary path", subtype="FILE_PATH", update=ffmpeg_path_update, default="")
    save_on_build: BoolProperty(name="Save on Build", description="Save .blend", default=False)
    legacy_shaders: BoolProperty(name="Legacy Shaders", description="Attempt to compile shaders runnable on older hardware, use this for WebGL1 or GLES2 support in mobile render path", default=False)
    relative_paths: BoolProperty(name="Generate Relative Paths", description="Write relative paths in khafile", default=False)
    viewport_controls: EnumProperty(
        items=[('qwerty', 'qwerty', 'qwerty'),
               ('azerty', 'azerty', 'azerty')],
        name="Viewport Controls", default='qwerty', description='Viewport camera mode controls')
    skip_update: BoolProperty(name="", default=False)

    def draw(self, context):
        self.skip_update = False
        layout = self.layout
        layout.label(text="Welcome to Armory!")
        p = bundled_sdk_path()
        if os.path.exists(p):
            layout.prop(self, "sdk_bundled")
            if not self.sdk_bundled:
                layout.prop(self, "sdk_path")
        else:
            layout.prop(self, "sdk_path")
        sdk_path = get_sdk_path(context)
        if os.path.exists(sdk_path + '/armory') or os.path.exists(sdk_path + '/armory_backup'):
            sdk_exists = True
        else:
            sdk_exists = False
        if not sdk_exists:
            layout.label(text="The directory will be created.")
        else:
            layout.label(text="")
        box = layout.box().column()
        box.label(text="Armory SDK Manager")
        box.label(text="Note: Development version may run unstable!")
        row = box.row(align=True)
        row.alignment = 'EXPAND'
        row.operator("arm_addon.help", icon="URL")
        sdk_path = get_sdk_path(context)
        if sdk_exists:
            row.operator("arm_addon.update", icon="FILE_REFRESH")
        else:
            row.operator("arm_addon.install", icon="IMPORT")
        row.operator("arm_addon.restore")
        box.label(text="Check console for download progress. Please restart Blender after successful SDK update.")
        layout.prop(self, "show_advanced")
        if self.show_advanced:
            box = layout.box().column()
            box.prop(self, "code_editor")
            box.prop(self, "ide_path")
            box.prop(self, "renderdoc_path")
            box.prop(self, "ffmpeg_path")
            box.prop(self, "viewport_controls")
            box.prop(self, "ui_scale")
            box.prop(self, "khamake_threads")
            box.prop(self, "compilation_server")
            box.prop(self, "save_on_build")
            box.prop(self, "legacy_shaders")
            box.prop(self, "relative_paths")

def bundled_sdk_path():
    if get_os() == 'mac':
        # SDK on MacOS is located in .app folder due to security
        p = bpy.app.binary_path
        if p.endswith('Contents/MacOS/blender'):
            return p[:-len('Contents/MacOS/blender')] + '/armsdk/'
        else:
            return p[:-len('Contents/MacOS/./blender')] + '/armsdk/'
    elif get_os() == 'linux':
        # /blender
        return bpy.app.binary_path.rsplit('/', 1)[0] + '/armsdk/'
    else:
        # /blender.exe
        return bpy.app.binary_path.replace('\\', '/').rsplit('/', 1)[0] + '/armsdk/'

def get_fp():
    if bpy.data.filepath == '':
        return ''
    s = bpy.data.filepath.split(os.path.sep)
    s.pop()
    return os.path.sep.join(s)

def get_sdk_path(context):
    preferences = context.preferences
    addon_prefs = preferences.addons["armory"].preferences
    p = bundled_sdk_path()
    if os.path.exists(get_fp() + '/armsdk'):
        return get_fp() + '/armsdk'
    elif os.path.exists(p) and addon_prefs.sdk_bundled:
        return p
    else:
        return addon_prefs.sdk_path

def remove_readonly(func, path, excinfo):
    os.chmod(path, stat.S_IWRITE)
    func(path)

def run_proc(cmd, done=None):
    def fn(p, done):
        p.wait()
        if done != None:
            done(0)
    p = None

    try:
        p = subprocess.Popen(cmd)
    except OSError as err:
        if done != None:
            done(1)
        print("Failed running command: " + str(cmd).replace('[', '').replace(']', '').replace(',','').replace("'",'') + '\n')
        if err.errno == 2:
            print("Make sure git is installed: https://git-scm.com/downloads")
        elif err.errno == 12:
            print("Make sure there is enough space for the SDK (at least 500mb)")
        elif err.errno == 13:
            print("Permission denied, try modifying the permission of the sdk folder")
        else:
            print("error: " + str(err))
    except Exception as err:
        if done != None:
            done(1)
        print("Failed running: " + str(cmd).replace('[', '').replace(']', '').replace(',','').replace("'",'') + '\n')
        print("error: " + str(err) + '\n')
    else:
        threading.Thread(target=fn, args=(p, done)).start()

    return p

def git_clone(done, p, gitn, n, recursive=False):
    path = p + '/' + n
    if os.path.exists(path) and not os.path.exists(path + '_backup'):
        os.rename(path, path + '_backup')
    if os.path.exists(path):
        shutil.rmtree(path, onerror=remove_readonly)
    if recursive:
    	run_proc(['git', 'clone', '--recursive', 'https://github.com/' + gitn, path, '--depth', '1', '--shallow-submodules', '--jobs', '4'], done)
    else:
    	run_proc(['git', 'clone', 'https://github.com/' + gitn, path, '--depth', '1'], done)

def restore_repo(p, n):
    if os.path.exists(p + '/' + n + '_backup'):
        if os.path.exists(p + '/' + n):
            shutil.rmtree(p + '/' + n, onerror=remove_readonly)
        os.rename(p + '/' + n + '_backup', p + '/' + n)

class ArmAddonStartButton(bpy.types.Operator):
    '''Start Armory integration'''
    bl_idname = "arm_addon.start"
    bl_label = "Start"
    running = False

    def execute(self, context):
        sdk_path = get_sdk_path(context)
        if sdk_path == "":
            print("Configure Armory SDK path first")
            return {"CANCELLED"}

        scripts_path = sdk_path + "/armory/blender/"
        sys.path.append(scripts_path)
        local_sdk = os.path.exists(get_fp() + '/armsdk')
        import start
        start.register(local_sdk=local_sdk)
        ArmAddonStartButton.running = True

        return {"FINISHED"}

class ArmAddonStopButton(bpy.types.Operator):
    '''Stop Armory integration'''
    bl_idname = "arm_addon.stop"
    bl_label = "Stop"
 
    def execute(self, context):
        import start
        start.unregister()
        ArmAddonStartButton.running = False
        return {"FINISHED"}

class ArmAddonInstallButton(bpy.types.Operator):
    '''Download and set up Armory SDK'''
    bl_idname = "arm_addon.install"
    bl_label = "Download and set up SDK"
    bl_description = "Download and set up the latest development version"

    def execute(self, context):
        update_sdk(self,context)
        return {"FINISHED"}

class ArmAddonUpdateButton(bpy.types.Operator):
    '''Update Armory SDK'''
    bl_idname = "arm_addon.update"
    bl_label = "Update SDK"
    bl_description = "Update to the latest development version"

    def execute(self, context):
        update_sdk(self,context)
        return {"FINISHED"}

def update_sdk(self,context):
    sdk_path = get_sdk_path(context)
    if sdk_path == "":
        self.report({"ERROR"}, "Configure Armory SDK path first")
        return {"CANCELLED"}

    self.report({'INFO'}, 'Updating Armory SDK, check console for details.')
    print('Armory (add-on v' + str(bl_info['version']) + '): Cloning [armory, iron, haxebullet, haxerecast, zui] repositories')
    if not os.path.exists(sdk_path):
        os.makedirs(sdk_path)
    os.chdir(sdk_path)
    global repos_updated
    global repos_total
    global repos_done
    repos_updated = 0
    repos_done = 0
    repos_total = 9
    def done(error=0):
        global repos_updated
        global repos_total
        global repos_done
        repos_done += 1
        if error == 0:
            repos_updated += 1
        if repos_updated == repos_total:
            print('Armory SDK updated, please restart Blender')
        elif repos_done == repos_total:
            self.report({"ERROR"}, "Failed updating Armory SDK, check console for details.")
    git_clone(done, sdk_path, 'armory3d/armory', 'armory')
    git_clone(done, sdk_path, 'armory3d/iron', 'iron')
    git_clone(done, sdk_path, 'armory3d/haxebullet', 'lib/haxebullet')
    git_clone(done, sdk_path, 'armory3d/haxerecast', 'lib/haxerecast')
    git_clone(done, sdk_path, 'armory3d/zui', 'lib/zui')
    git_clone(done, sdk_path, 'armory3d/armory_tools', 'lib/armory_tools')
    git_clone(done, sdk_path, 'armory3d/Kromx_bin', 'Krom')
    git_clone(done, sdk_path, 'armory3d/Kha', 'Kha', recursive=True)
    git_clone(done, sdk_path, 'armory3d/nodejs_bin/', 'nodejs')

class ArmAddonRestoreButton(bpy.types.Operator):
    '''Update Armory SDK'''
    bl_idname = "arm_addon.restore"
    bl_label = "Restore SDK"
    bl_description = "Restore stable version"
 
    def execute(self, context):
        sdk_path = get_sdk_path(context)
        if sdk_path == "":
            self.report({"ERROR"}, "Configure Armory SDK path first")
            return {"CANCELLED"}
        os.chdir(sdk_path)
        restore_repo(sdk_path, 'armory')
        restore_repo(sdk_path, 'iron')
        restore_repo(sdk_path, 'lib/haxebullet')
        restore_repo(sdk_path, 'lib/haxerecast')
        restore_repo(sdk_path, 'lib/zui')
        restore_repo(sdk_path, 'lib/armory_tools')
        restore_repo(sdk_path, 'Kha')
        restore_repo(sdk_path, 'Krom')
        self.report({'INFO'}, 'Restored stable version')
        return {"FINISHED"}

class ArmAddonHelpButton(bpy.types.Operator):
    '''Updater help'''
    bl_idname = "arm_addon.help"
    bl_label = "Help"
    bl_description = "Git is required for Armory Updater to work"
 
    def execute(self, context):
        webbrowser.open('https://github.com/armory3d/armory/wiki/gitversion')
        return {"FINISHED"}

@persistent
def on_load_post(context):
    if ArmAddonStartButton.running:
        return
    bpy.ops.arm_addon.start()

def register():
    bpy.utils.register_class(ArmoryAddonPreferences)
    bpy.utils.register_class(ArmAddonStartButton)
    bpy.utils.register_class(ArmAddonStopButton)
    bpy.utils.register_class(ArmAddonInstallButton)
    bpy.utils.register_class(ArmAddonUpdateButton)
    bpy.utils.register_class(ArmAddonRestoreButton)
    bpy.utils.register_class(ArmAddonHelpButton)
    bpy.app.handlers.load_post.append(on_load_post)

def unregister():
    bpy.ops.arm_addon.stop()
    bpy.utils.unregister_class(ArmoryAddonPreferences)
    bpy.utils.unregister_class(ArmAddonStartButton)
    bpy.utils.unregister_class(ArmAddonStopButton)
    bpy.utils.register_class(ArmAddonInstallButton)
    bpy.utils.unregister_class(ArmAddonUpdateButton)
    bpy.utils.unregister_class(ArmAddonRestoreButton)
    bpy.utils.unregister_class(ArmAddonHelpButton)
    bpy.app.handlers.load_post.remove(on_load_post)

if __name__ == "__main__":
    register()
