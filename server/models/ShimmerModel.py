from server.models.ShimmerImage import ShimmerImage
from server.models.ShimmerTarget import ShimmerTarget
from server.models.ShimmerTargetRegion import ShimmerTargetRegion

class ShimmerModel():
    """
    Queues of images for Shimmer

    Arguments:
        queue: The underlying ImageQueue
    """

    def __init__(self, queue):
        self.queue = queue
        self.replay_pos = 0
        self.image_ids = []
        # Load all images already in the queue
        image = self.queue.get_next_image()
        while image is not None:
            self.image_ids.append(image.image_id)
            image = self.queue.get_next_image()

    def img(self, idx):
        """
        Get image data at index idx

        Arguments:
            idx: the index to get data at
        """
        arc_image = self.queue.flight.image(self.image_ids[idx])
        image = ShimmerImage(idx, arc_image, self.queue.flight)
        return image

    def get_image(self, image_id):
        return self.img(image_id)

    def tgt(self, target_id):
        """
        Get the target with id

        Arguments:
            target_id: the target id to get
        """
        # Pending target(id) method in ARC.Flight
        # return self.queue.flight.target(id)
        # XXX Hack: Iterate over all targets
        for target in self.get_all_targets():
            if target.id == target_id:
                return target
        raise KeyError("Target not found")

    def get_target(self, target_id):
        return self.tgt(target_id)

    def get_next_image(self):
        """
        Retrieves the next image out of the queue
        """
        next_img = self.queue.get_next_image()
        if next_img is None:
            # No more images in the queue.
            return self.get_replay_image()

        self.image_ids.append(next_img.image_id)
        img = ShimmerImage(len(self.image_ids) - 1, next_img, self.queue.flight)
        return img

    def get_replay_image(self):
        """
        Replays images in a loop
        """
        if self.replay_pos >= len(self.image_ids):
            self.replay_pos = 0
        img = ShimmerImage(
            self.replay_pos,
            self.queue.flight.image(self.image_ids[self.replay_pos]),
            self.queue.flight
        )
        self.replay_pos += 1
        return img

    def get_all_targets(self):
        """
        Get all targets from a flight
        """
        return [ ShimmerTarget(target) for target in self.queue.flight.all_targets() ]

    def insert_target(self, idx, target, target_region):
        """
        Creates a new target

        Arguments:
            idx: Shimmer flight image index
            target: Dictionary containing parameters for a new target
            target_region: Dictionary containing parameters for a new target_region
        """
        image = self.img(idx)
        coord = (target_region['a']['x'], target_region['a']['y'])
        coord2 = (target_region['b']['x'], target_region['b']['y'])

        result = self.queue.flight.insert_target(coord, coord2=coord2,
                    image=image.image, target_type=int(target['target_type']),
                    letter=target['letter'], shape=target['shape'],
                    background_color=target['shape_color'],
                    letter_color=target['letter_color'],
                    orientation=target['orientation'],
                    notes=target['notes'], thumb=None, manual=True)

        new_region = ShimmerTargetRegion(result[1])
        new_region.create_thumbnail()

        return {
            "target" : ShimmerTarget(result[0]),
            "target_region": new_region
        }

    def update_target(self, target_id, new_target):
        """
        Updates an existing target

        Arguments:
            target_id: ID of the Target
            new_target: Dictionary containing new target data
        """
        target = self.tgt(target_id)
        target.deserialize(new_target)
        return target

    def delete_target(self, target_id):
        """
        Deletes a target and associated target regions
        """
        target = self.tgt(target_id)
        target.delete()

    def merge_targets(self, target_id, target_ids):
        """
        Updates an existing target

        Arguments:
            target_id: ID of the Target
            target_ids: List of target ids
        """
        arc_target = self.tgt(target_id).target

        for old_id in target_ids:
            old_target = self.tgt(old_id)
            arc_target.absorb_target(old_target.target)

    def get_flight_id(self):
        """
        Gets the current flight id
        """
        return self.queue.get_flight_id()
        
    def get_target_regions(self, target_id):
        """
        Gets the target regions for a target

        Arguments:
            target_id: the target to get the regions of
        """
        target = self.tgt(target_id)
        return [ ShimmerTargetRegion(region) for region in target.target.get_target_regions() ]

    def get_shimmer_image_id(self, data_id):
        """
        Searches through the image_ids numbers to see if one exists with that number
        Otherwise returns -1

        Arguments:
            data_id: the database id for an image
        """
        for i, id in enumerate(self.image_ids):
            if(id == data_id):
                return i
        return -1