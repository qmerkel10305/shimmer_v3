from ShimmerTarget import ShimmerTarget

class ShimmerImage(object):
    next_id = 0
    """
    ShimmerImage wraps data for an image.

    Arguments:
        image: the ARC.Image this ShimmerImage wraps
        flight: the ARC.Flight this image belongs to
    """
    def __init__(self, image, flight):
        self.image = image
        self.flight = flight

        self.id = ShimmerImage.next_id
        self.image_url = "image/" + str(ShimmerImage.next_id)
        self.targets = [ ShimmerTarget(tgt) for tgt in image.get_target_regions(flight=flight) ]

        ShimmerImage.next_id += 1

    def __iter__(self):
        yield ('id', self.id)
        yield ('image', self.image_url)
        yield ('targets', self.targets)
        yield ('flight', self.flight.flight_id)

    @property
    def path(self):
        return self.image.jpg()

    def update_targets(self, new_targets):
        """
        Synchronizes target data in this image with data from the frontend.

        Arguments:
            new_targets: Target data from the frontend. This may contain
                         targets already in the list of known targets
        """
        # check the initial length of the targets array
        # this is used to check if targets were deleted later
        initial_length = len(self.targets)

        # Sort both lists of targets so that the order of keys match
        self.targets = sorted(self.targets, key=lambda x: x.id)
        new_targets = sorted(new_targets, key=target_comparator)

        # Insert new targets
        i = 0
        for target in new_targets:
            if not 'target_id' in target:
                _, target_region = self.add_target(**target)
                self.targets.append(ShimmerTarget(target_region))
                i += 1
            else:
                break

        # Delete any targets that were deleted on the frontend
        incoming_targets = new_targets[i:]
        i = 0
        for target in incoming_targets:
            while self.targets[i].id != target['target_id']:
                self.targets[i].delete_region()
                del self.targets[i]
            i += 1
        for _ in range(i, initial_length):
            self.targets[i].delete_region()
            del self.targets[i]

    def add_target(self, target_type=None, alphanumeric=None,
                   alphanumeric_color=None, shape_color=None, shape=None,
                   alphanumeric_orientation=None, notes=None,
                   a=None, b=None,
                   width=None, height=None):
        coord1 = (a['x'], a['y'])
        coord2 = (b['x'], b['y'])
        return self.flight.insert_target(
            coord1, coord2, image=self.image, manual=True,
            target_type=target_type, letter=alphanumeric, shape=shape,
            orientation=alphanumeric_orientation, letter_color=alphanumeric_color,
            background_color=shape_color, notes=notes
        )

def target_comparator(target):
    if not 'target_id' in target:
        return 0
    else:
        return target['target_id']