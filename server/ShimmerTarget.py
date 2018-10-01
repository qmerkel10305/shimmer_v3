import ARC
import cv2

class ShimmerTarget(object):
    def __init__(self, target_region):
        self.target_region = target_region
        self.valid = True

    def __iter__(self):
        if not self.valid:
            raise StopIteration()
        yield ('target_id', self.target_region.target_region_id)
        yield ('target_type', self.target_region.target.target_type if self.target_region.target.target_type is not None else 0)
        yield ('letter', self.target_region.target.letter)
        yield ('shape', self.target_region.target.shape)
        yield ('letter_color', self.target_region.target.letter_color)
        yield ('shape_color', self.target_region.target.background_color)
        yield ('orientation', self.target_region.target.orientation)
        yield ('notes', self.target_region.target.notes)
        yield ('a', {'x':self.target_region.coord1[0], 'y':self.target_region.coord1[1]})
        yield ('b', {'x':self.target_region.coord2[0], 'y':self.target_region.coord2[1]})
        yield ('width', self.target_region.coord2[0] - self.target_region.coord1[0])
        yield ('height', self.target_region.coord2[1] - self.target_region.coord1[1])

    @property
    def id(self):
        return self.target_region.target_region_id

    def create_thumbnail(self):
        tgtimage = self.target_region.image.jpg()
        tgtimage = cv2.imread(tgtimage)
        # Set coordinates for cropped image
        crop_img = tgtimage[int(self.target_region.coord1[1]):int(self.target_region.coord2[1]),
                            int(self.target_region.coord1[0]):int(self.target_region.coord2[0])]
        # Save the cropped image
        thumbnail_path = self.target_region.flight.folder + "/targets/target_" + str(self.target_region.target_region_id) + ".jpg"
        cv2.imwrite(thumbnail_path, crop_img)
        self.target_region.target.update_thumbnail(thumbnail_path)