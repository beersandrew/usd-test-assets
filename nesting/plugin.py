from pxr import Plug
registry = Plug.Registry()
for plugin in registry.GetAllPlugins():
    print(plugin.name, plugin.path, plugin.isLoaded)


from pxr import Plug, Tf, Usd
registry = Plug.Registry()
print(">>>>>", "Typed Schemas")
for type_name in registry.GetAllDerivedTypes(Usd.Typed):
    print(type_name)
print(">>>>>", "API Schemas")
for type_name in registry.GetAllDerivedTypes(Usd.APISchemaBase):
    print(type_name)

# For example to lookup where the "Cube" type is registered from,
# we can run:
print(">>>>>", "Cube Schema Plugin Source")
plugin = registry.GetPluginForType(Tf.Type.FindByName("UsdGeomCube"))
print(plugin.name)
print(plugin.path)
print(plugin.resourcePath)
print(plugin.metadata)