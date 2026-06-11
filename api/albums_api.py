from api.base_client import BaseClient

class AlbumsAPI(BaseClient):
    def get_album(self, album_id):
        return self.get(f"/albums/{album_id}")

    def get_all_albums(self):
        return self.get("/albums")

    def get_album_photos(self, album_id):
        return self.get(f"/albums/{album_id}/photos")
