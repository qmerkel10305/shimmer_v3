   def arc_load_flight(self, flight_id):
        self.flight = ARC.Flight(flight_id)
        # Connect this flight to all images
        self.currimg.flight = self.flight
        self.nextimg.flight = self.flight
        self.previmg.flight = self.flight
        images = self.flight.all_images(filenames=True)
        # XXX: Race Condition!  Images arriving here will be missed
        self.flight.start_listener()
        if images:
            self.expand_filelist_and_load_image(images)
        else:
            self.put_error_image_to_window()
        self.update_title()
        self.update_statusbar()

    def arc_update_flight(self):
        if self.stop_now:
            return

        images = []
        while True:
            img = self.flight.next_image(timeout=0.01, filename=True)
            if not img:
                break
            else:
                images.append(img)

        if images:
            if not self.image_list:
                self.expand_filelist_and_load_image(images)
                self.update_title()
                self.update_statusbar()
            else:
                for i in images:
                    self.image_list.append(i)
                self.thumbpane_update_images(True)

    def arc_manual_add_target(self, button, image, thumb, coord,
            target_type, letter, shape, orientation,
            letter_color, background_color, notes):
        target_type = target_type.get_active()
        try:
            ARC.TargetType(target_type)
        except ValueError:
            target_type = None

        letter = letter.get_text()
        if not letter:
            letter = None
        shape = shape.get_active()
        try:
            shape = ARC.Shape(shape).name
        except ValueError:
            shape = None
        orientation = orientation.get_text()
        if not orientation:
            orientation = None
        letter_color = letter_color.get_active()
        try:
            letter_color = ARC.Color(letter_color).name
        except ValueError:
            letter_color = None
        background_color = background_color.get_active()
        try:
            background_color = ARC.Color(background_color).name
        except ValueError:
            background_color = None
        notes = notes.get_text()
        if not notes:
            notes = None

        # Insert target
        target = self.flight.insert_target(coord, image=image, manual=True,
            target_type=target_type, letter=letter, shape=shape,
            orientation=orientation, letter_color=letter_color,
            background_color=background_color, notes=notes)

        thumb_path = os.path.join(self.flight.target_folder, "target_%d.jpg" % target.target_id)
        thumb.save(thumb_path, "jpeg", {"quality": "100"})
        target.set_thumbnail(thumb_path)

