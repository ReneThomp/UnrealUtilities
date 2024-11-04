import tkinter.filedialog
from unreal import ToolMenus, uclass, ufunction, ToolMenuEntryScript, ToolMenuContext
import os
import sys
import importlib
import tkinter

srcPath = os.path.dirname(os.path.abspath(__file__))
if srcPath not in sys.path:
    sys.path.append(srcPath)

import UnrealUtilities
importlib.reload(UnrealUtilities)

@uclass()
class BuildBaseMaterialEntryScript(ToolMenuEntryScript):
    @ufunction(override = True)
    def execute(self,context: ToolMenuContext) -> None:
        UnrealUtilities.UnrealUtility().FindOrBuildBaseMaterial()

@uclass()
class LoadMeshEntryScript(ToolMenuEntryScript):
    @ufunction(override=True)
    def execute(self, context) -> None:
        window = tkinter.Tk()
        window.withdraw()
        importPath = tkinter.filedialog.askdirectory()
        window.destroy()
        UnrealUtilities.UnrealUtility.ImportFromDir(importdir) 



class UnrealSubstancePlugin:
    def __init__(self):
        self.submenuName="UnrealSubstancePlugin"
        self.submenuLabel ="Unreal Substance Plugin"
        self.CreateMenu()

    def CreateMenu(self):
        mainMenu = ToolMenus.get().find_menu("LevelEditor.MainMenu")


        existing = ToolMenus.get().find_menu(f"LevelEditor.MainMenu.{self.submenuName}")
        if existing:
            print(f"deleted existing menu: {existing}")
            ToolMenus.get().remove_menu(existing.menu_name)
        
        self.submenu = mainMenu.add_sub_menu(mainMenu.menu_name, "", "UnrelSubstancePlugin", "Unreal Substance Plugin" )
        self.AddEntrycript("BuilBaseMaterial", "build Base Material" , BuildBaseMaterialEntryScript())
        ToolMenus.get().refresh_all_widgets()

    def AddEntrycript(self, name, label , script: ToolMenuEntryScript):
        script.init_entry(self.submenu.menu_name, self.submenu.menu_name, "" , name,label)
        script.register_menu_entry()



UnrealSubstancePlugin()