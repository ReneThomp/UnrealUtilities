from unreal import ( AssetToolsHelpers, EditorAssetLibrary, AssetTools, Material, MaterialFactoryNew, MaterialEditingLibrary, MaterialExpressionTextureSampleParameter2D as TexSample2d,
        MaterialProperty, AssetImportTask, FbxImportUI)

import os

class UnrealUtility:
    def __init__(self): #the constructor method that initializes the objects attributes
        self.substanceRooDir ='/game/Substance' #sets the root directory for substance assets
        self.substanceBaseMatName = 'M_SubstanceBase' #sets the name for the base material
        self.substanceBaseMatPath = self.substanceRooDir + self.substanceBaseMatName #combines the root dir and the base material name to create the full path
        self.substancetempfolder='/game/Substance/temp' # sets a temporary folder path for substance assets
        self.baseColorName = "BaseColor" #changes base color name to "Base Color" for material properties
        self.normalName = "Normal" #Matrial attribute normal name change to "Normal"
        self.occroughnessMetalic = "OcclusionRoughnessMetalic" #Material attribute OCCRoughnessMetalic name change to OcclusionRoughnessMetalic



    def GetAssetTools(self)->AssetTools: # This defines a method that returns an instance of AssetTools
        return AssetToolsHelpers.get_asset_tools() #a helper funtion to get the asset tools
    
    def ImportFromDir(self, dir): #method takes a dir path as an argument and processes each file in the dir
        for file in os.listdir(dir): #loops through each file directory
            if ".fbx" in file: #checks if the file has an fbx extension
                 self.LoadMeshFromPath(os.path.join(dir, file)) #should load the mesh from the file path

    def LoadMeshFromPath(self, meshPath):
        meshName = os.path.split(meshPath)[-1].replace(".fbx", "")#extracts the mesh name by removing the fbx extension
        importTask = AssetImportTask() #creates a new asset import task
        importTask.replace_existing = True #sets the import task to replace existing assets
        importTask.filename = meshPath #This sets the file name for the import task
        importTask.destination_path = '/game/' + meshName # sets the destination path for the imported asset
        importTask.automated=True #automates the import task
        importTask.save=True #saves your import task

        fbxImportOption = FbxImportUI #creates an instance of FBX import options
        fbxImportOption.import_mesh=True #sets the import option to import the mesh
        fbxImportOption.import_as_skeletal=False #This sets the import option to not import the mesh as skeletal
        fbxImportOption.import_materials=False #This sets the import option to not import materials
        fbxImportOption.static_mesh_import_data.combine_meshes = True #This combines the meshes in the import options
        importTask.options = fbxImportOption  #This sets the import options for the import task.

        self.GetAssetTools().import_asset_tasks([importTask]) #calls the asset tools to perform the import task
        return importTask.get_objects()[0] #returns the imported mesh object

    def FindOrBuildBaseMaterial(self): #this method will find or create a base material
        if EditorAssetLibrary.does_asset_exist(self.substanceBaseMatPath): #Checks if the base mat asset exist
            return EditorAssetLibrary.load_asset(self.substanceBaseMatPath) #if it does exist, loads and returns the base material
        
        baseMat = self.GetAssetTools().create_asset(self.substanceBaseMatName, self.substanceRooDir, Material, MaterialFactoryNew()) #if doesnt exist, creates new material
        baseColor = MaterialEditingLibrary.create_material_expression(baseMat, TexSample2d, -800, 0 ) #creates a material expression for base color
        baseColor.set_editor_property("parameter_name", self.baseColorName) #sets the parameter name for the base color 
        MaterialEditingLibrary.connect_material_property(baseColor, "RGB", MaterialProperty.MP_BASE_COLOR) #connects the base color to the materials base color property

        normal = MaterialEditingLibrary.create_material_expression(baseMat, TexSample2d, -800, 400) #Creates a material expression for normal mapping
        normal.set_editor_property("parameter_name", self.normalName) #sets the parameter name for the normal map
        normal.set_editor_property("texture", EditorAssetLibrary.load_asset("/Engine/EngineMaterials/DefaultNormal")) #This sets the default normal texture
        MaterialEditingLibrary.connect_material_property(normal, "RGB", MaterialProperty.MP_NORMAL) #this connects the normal map to the materials normal property

        occRoughnessMetalic = MaterialEditingLibrary.create_material_expression(baseMat, TexSample2d, -800, 800) #This creates a material expression for occlusion, roughness, and metallic properties
        occRoughnessMetalic.set_editor_property("parameter_name", self.occroughnessMetalic) #sets the parameter name for occlusion, roughness and metallic properties
        MaterialEditingLibrary.connect_material_property(occRoughnessMetalic, "R", MaterialProperty.MP_AMBIENT_OCCLUSION) #This connects occlusion to the material's ambient occlusion property.
        MaterialEditingLibrary.connect_material_property(occRoughnessMetalic, "G", MaterialProperty.MP_ROUGHNESS)#Connects the roughness to the mats roughtness property
        MaterialEditingLibrary.connect_material_property(occRoughnessMetalic, "B", MaterialProperty.MP_METALLIC)#connects metallic to the materials metallic proprty

        EditorAssetLibrary.save_asset(baseMat.get_path_name()) #saves the new base material
        return baseMat #returns the base material