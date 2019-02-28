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
        self.images = {}
        # Load all images already in the queue
        image = self.queue.get_next_image()
        while image is not None:
            img = ShimmerImage(image, self.queue.flight)
            self.images[img.id] = img
            self.image_ids.append(img.id)
            image = self.queue.get_next_image()

    def img(self, idx):
        """
        Get image data at index idx

        Arguments:
            idx: the index to get data at
        """
        # Update the image
        image = self.images[idx]
        image.update()
        return image

    def get_image(self, id):
        return self.img(id)

    def tgt(self, id):
        """
        Get the target with id

        Arguments:
            id: the target id to get
        """
        return self.queue.flight.target(id)

    def get_target(self, id):
        return self.tgt(id)

    def get_next_image(self):
        """
        Retrieves the next image out of the queue
        """
        next_img = self.queue.get_next_image()
        if next_img is None:
            # No more images in the queue.
            return self.get_replay_image()

        img = ShimmerImage(next_img, self.queue.flight)
        self.images[img.id] = img
        return img

    def get_replay_image(self):
        """
        Replays images in a loop
        """
        if self.replay_pos >= len(self.image_ids):
            self.replay_pos = 0
        img = self.images[self.image_ids[self.replay_pos]]
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
                    image=image.image, target_type=target['target_type'],
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