import dearpygui.dearpygui as dpg

class GUI:
    def __init__(self):
        dpg.create_context()
        dpg.create_viewport()
        dpg.setup_dearpygui()
        dpg.maximize_viewport()
        dpg.set_viewport_title("Imagere")
        dpg.set_global_font_scale(3)

        with dpg.window(label="##root") as self.root:
            dpg.add_text("Hello world")
            dpg.add_input_text(label="string")
            dpg.add_slider_float(label="float")

    def start(self):
        dpg.set_primary_window(self.root, True)
        dpg.set_viewport_vsync(True)
        dpg.show_viewport()
        dpg.start_dearpygui()
        dpg.destroy_context()