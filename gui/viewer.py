import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
gi.require_version("Gdk", "3.0")
from gi.repository import Gdk
from gui.frame import Frame
from gui.painter import Painter


display = Gdk.Display.get_default()
if not display:
    exit("GUI code not find the display.")

MONITOR_GEOMETRY = display.get_monitor(0).get_geometry()
MONITOR_WIDTH = MONITOR_GEOMETRY.width
MONITOR_HEIGHT = MONITOR_GEOMETRY.height

DEFAULT_VIEW_PIX_W = round(MONITOR_WIDTH * 0.5)  # pixels
DEFAULT_VIEW_PIX_H = round(MONITOR_HEIGHT * 0.7)  # pixels
DEFAULT_ZOOM = 100  # pixels per meter

# user response codes for file chooser dialog buttons
LS_DIALOG_RESPONSE_CANCEL = 1
LS_DIALOG_RESPONSE_ACCEPT = 2


class Viewer:
    def __init__(self, simulator):
        # bind the simulator
        self.simulator = simulator

        # initialize frame
        self.current_frame = Frame()

        # initialize camera parameters
        self.view_width_pixels = DEFAULT_VIEW_PIX_W
        self.view_height_pixels = DEFAULT_VIEW_PIX_H
        self.pixels_per_meter = DEFAULT_ZOOM

        # initialize the window
        self.window = Gtk.Window()
        self.window.set_title("Sobot Rimulator")
        self.window.set_resizable(False)
        self.window.connect("delete_event", self.on_delete)

        # initialize the drawing_area
        self.drawing_area = Gtk.DrawingArea()
        self.drawing_area.set_size_request(
            self.view_width_pixels, self.view_height_pixels
        )
        self.drawing_area.connect("draw", self.on_expose)

        # initialize the painter
        self.painter = Painter(self.pixels_per_meter)

        # == initialize the buttons

        # build the play button
        self.button_play = Gtk.Button("Play")
        play_image = Gtk.Image()
        play_image.set_from_stock(Gtk.STOCK_MEDIA_PLAY, Gtk.IconSize.BUTTON)
        self.button_play.set_image(play_image)
        self.button_play.set_image_position(Gtk.PositionType.LEFT)
        self.button_play.connect("clicked", self.on_play)

        # build the stop button
        self.button_stop = Gtk.Button("Stop")
        stop_image = Gtk.Image()
        stop_image.set_from_stock(Gtk.STOCK_MEDIA_STOP, Gtk.IconSize.BUTTON)
        self.button_stop.set_image(stop_image)
        self.button_stop.set_image_position(Gtk.PositionType.LEFT)
        self.button_stop.connect("clicked", self.on_stop)

        # build the step button
        self.button_step = Gtk.Button("Step")
        step_image = Gtk.Image()
        step_image.set_from_stock(Gtk.STOCK_MEDIA_NEXT, Gtk.IconSize.BUTTON)
        self.button_step.set_image(step_image)
        self.button_step.set_image_position(Gtk.PositionType.LEFT)
        self.button_step.connect("clicked", self.on_step)

        # build the reset button
        self.button_reset = Gtk.Button("Reset")
        reset_image = Gtk.Image()
        reset_image.set_from_stock(Gtk.STOCK_MEDIA_REWIND, Gtk.IconSize.BUTTON)
        self.button_reset.set_image(reset_image)
        self.button_reset.set_image_position(Gtk.PositionType.LEFT)
        self.button_reset.connect("clicked", self.on_reset)

        # build the save map button
        self.button_save_map = Gtk.Button("Save Map")
        save_map_image = Gtk.Image()
        save_map_image.set_from_stock(Gtk.STOCK_SAVE, Gtk.IconSize.BUTTON)
        self.button_save_map.set_image(save_map_image)
        self.button_save_map.set_image_position(Gtk.PositionType.LEFT)
        self.button_save_map.connect("clicked", self.on_save_map)

        # build the load map button
        self.button_load_map = Gtk.Button("Load Map")
        load_map_image = Gtk.Image()
        load_map_image.set_from_stock(Gtk.STOCK_OPEN, Gtk.IconSize.BUTTON)
        self.button_load_map.set_image(load_map_image)
        self.button_load_map.set_image_position(Gtk.PositionType.LEFT)
        self.button_load_map.connect("clicked", self.on_load_map)

        # build the random map buttons
        self.button_random_map = Gtk.Button("Random Map")
        random_map_image = Gtk.Image()
        random_map_image.set_from_stock(Gtk.STOCK_REFRESH, Gtk.IconSize.BUTTON)
        self.button_random_map.set_image(random_map_image)
        self.button_random_map.set_image_position(Gtk.PositionType.LEFT)
        self.button_random_map.connect("clicked", self.on_random_map)

        # build the show-invisibles toggle button
        self.show_invisibles = (
            False  # controls whether invisible world elements are displayed
        )
        self.button_show_invisibles = Gtk.Button()
        self._decorate_show_invisibles_button_inactive()
        self.button_show_invisibles.set_image_position(Gtk.PositionType.LEFT)
        self.button_show_invisibles.connect("clicked", self.on_show_invisibles)

        # == lay out the window

        # pack the simulation control buttons
        sim_controls_box = Gtk.HBox(spacing=5)
        sim_controls_box.pack_start(self.button_play, False, False, 0)
        sim_controls_box.pack_start(self.button_stop, False, False, 0)
        sim_controls_box.pack_start(self.button_step, False, False, 0)
        sim_controls_box.pack_start(self.button_reset, False, False, 0)

        # pack the map control buttons
        map_controls_box = Gtk.HBox(spacing=5)
        map_controls_box.pack_start(self.button_save_map, False, False, 0)
        map_controls_box.pack_start(self.button_load_map, False, False, 0)
        map_controls_box.pack_start(self.button_random_map, False, False, 0)

        # pack the invisibles button
        invisibles_button_box = Gtk.HBox()
        invisibles_button_box.pack_start(self.button_show_invisibles, False, False, 0)

        # align the controls
        sim_controls_alignment = Gtk.Alignment(
            xalign=0.5, yalign=0.5, xscale=0, yscale=0
        )
        map_controls_alignment = Gtk.Alignment(
            xalign=0.5, yalign=0.5, xscale=0, yscale=0
        )
        invisibles_button_alignment = Gtk.Alignment(
            xalign=0.5, yalign=0.5, xscale=0, yscale=0
        )
        sim_controls_alignment.add(sim_controls_box)
        map_controls_alignment.add(map_controls_box)
        invisibles_button_alignment.add(invisibles_button_box)

        # create the alert box
        self.alert_box = Gtk.Label()

        # lay out the simulation view and all of the controls
        layout_box = Gtk.VBox()
        layout_box.pack_start(self.drawing_area, False, False, 0)
        layout_box.pack_start(self.alert_box, False, False, 5)
        layout_box.pack_start(sim_controls_alignment, False, False, 5)
        layout_box.pack_start(map_controls_alignment, False, False, 5)
        layout_box.pack_start(invisibles_button_alignment, False, False, 5)

        # apply the layout
        self.window.add(layout_box)

        # show the simulator window
        self.window.show_all()

    def new_frame(self):
        self.current_frame = Frame()

    def draw_frame(self):
        self.drawing_area.queue_draw_area(
            0, 0, self.view_width_pixels, self.view_height_pixels
        )

    def control_panel_state_init(self):
        self.alert_box.set_text("")
        self.button_play.set_sensitive(True)
        self.button_stop.set_sensitive(False)
        self.button_step.set_sensitive(True)
        self.button_reset.set_sensitive(False)

    def control_panel_state_playing(self):
        self.button_play.set_sensitive(False)
        self.button_stop.set_sensitive(True)
        self.button_reset.set_sensitive(True)

    def control_panel_state_paused(self):
        self.button_play.set_sensitive(True)
        self.button_stop.set_sensitive(False)
        self.button_reset.set_sensitive(True)

    def control_panel_state_finished(self, alert_text):
        self.alert_box.set_text(alert_text)
        self.button_play.set_sensitive(False)
        self.button_stop.set_sensitive(False)
        self.button_step.set_sensitive(False)

    # EVENT HANDLERS:
    def on_play(self, widget):
        self.simulator.play_sim()

    def on_stop(self, widget):
        self.simulator.pause_sim()

    def on_step(self, widget):
        self.simulator.step_sim_once()

    def on_reset(self, widget):
        self.simulator.reset_sim()

    def on_save_map(self, widget):
        # create the file chooser
        file_chooser = Gtk.FileChooserDialog(
            title="Save Map",
            parent=self.window,
            action=Gtk.FileChooserAction.SAVE,
            buttons=(
                Gtk.STOCK_CANCEL,
                LS_DIALOG_RESPONSE_CANCEL,
                Gtk.STOCK_SAVE,
                LS_DIALOG_RESPONSE_ACCEPT,
            ),
        )
        file_chooser.set_do_overwrite_confirmation(True)
        file_chooser.set_current_folder("maps")

        # run the file chooser dialog
        response_id = file_chooser.run()

        # handle the user's response
        if response_id == LS_DIALOG_RESPONSE_CANCEL:
            file_chooser.destroy()
        elif response_id == LS_DIALOG_RESPONSE_ACCEPT:
            self.simulator.save_map(file_chooser.get_filename())
            file_chooser.destroy()

    def on_load_map(self, widget):
        # create the file chooser
        file_chooser = Gtk.FileChooserDialog(
            title="Load Map",
            parent=self.window,
            action=Gtk.FileChooserAction.OPEN,
            buttons=(
                Gtk.STOCK_CANCEL,
                LS_DIALOG_RESPONSE_CANCEL,
                Gtk.STOCK_OPEN,
                LS_DIALOG_RESPONSE_ACCEPT,
            ),
        )
        file_chooser.set_current_folder("maps")

        # run the file chooser dialog
        response_id = file_chooser.run()

        # handle the user's response
        if response_id == LS_DIALOG_RESPONSE_CANCEL:
            file_chooser.destroy()
        elif response_id == LS_DIALOG_RESPONSE_ACCEPT:
            self.simulator.load_map(file_chooser.get_filename())
            file_chooser.destroy()

    def on_random_map(self, widget):
        self.simulator.random_map()

    def on_show_invisibles(self, widget):
        # toggle the show_invisibles state
        self.show_invisibles = not self.show_invisibles
        if self.show_invisibles:
            self._decorate_show_invisibles_button_active()
        else:
            self._decorate_show_invisibles_button_inactive()
        self.simulator.draw_world()

    def on_expose(self, widget, context):
        self.painter.draw_frame(self.current_frame, widget, context)

    def on_delete(self, widget, event):
        Gtk.main_quit()
        return False

    def _decorate_show_invisibles_button_active(self):
        show_invisibles_image = Gtk.Image()
        show_invisibles_image.set_from_stock(Gtk.STOCK_REMOVE, Gtk.IconSize.BUTTON)
        self.button_show_invisibles.set_image(show_invisibles_image)
        self.button_show_invisibles.set_label("Hide Invisibles")

    def _decorate_show_invisibles_button_inactive(self):
        show_invisibles_image = Gtk.Image()
        show_invisibles_image.set_from_stock(Gtk.STOCK_ADD, Gtk.IconSize.BUTTON)
        self.button_show_invisibles.set_image(show_invisibles_image)
        self.button_show_invisibles.set_label("Show Invisibles")
