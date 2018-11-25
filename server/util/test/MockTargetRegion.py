class MockTargetRegion(object):
    def __init__(self, target_region_id, target=None, image=None, flight=None, coord1=None, coord2=None):
        self.target_region_id = target_region_id
        self.target = target
        self.image = image
        self.flight = flight
        self.coord1 = coord1
        self.coord2 = coord2

    def delete_region(self):
        pass

    def update_thumbnail(self, thumbnail_path):
        pass
