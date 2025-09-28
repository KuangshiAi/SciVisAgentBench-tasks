import napari

viewer = napari.Viewer()

# 1) open your plugin's dock widget at startup
#    (use plugin package name and the widget name from its manifest)
dock, widget = viewer.window.add_plugin_dock_widget(
    plugin_name="napari-socket",
    widget_name="Socket Server",
)

# 2) automatically start the socket server
if hasattr(widget, "_start"):
    widget._start()

napari.run()    