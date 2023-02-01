import requests
import redis


class TestMain:
    # API_URL = "http://127.0.0.1:8000"
    API_URL = "http://web:8000"

    # decoded_connection = redis.Redis(decode_responses=True)
    pool = redis.ConnectionPool(host='cashe', port=6379, db=0)
    decoded_connection = redis.Redis(
        connection_pool=pool, decode_responses=True,
    )

    def get_id_menu(self):
        r = requests.get(f"{self.API_URL}/api/v1/menus")
        first_id = r.json()[0]['id']
        return first_id

    def get_id_submenu(self):
        api_test_menu_id = self.get_id_menu()
        r = requests.get(
            f"{self.API_URL}/api/v1/menus/{api_test_menu_id}/submenus/?skip = 0 & limit = 100",
        )
        id_submenu = r.json()[0]['id']
        return id_submenu

    def get_id_dish(self):
        api_test_menu_id = self.get_id_menu()
        id_submenu = self.get_id_submenu()
        r = requests.get(
            f"{self.API_URL}/api/v1/menus/{api_test_menu_id}/submenus/{id_submenu}/dishes",
        )
        id_dish = r.json()[0]['id']
        return id_dish

    def test_get_menus(self):
        r = requests.get(f"{self.API_URL}/api/v1/menus?skip=0&limit=100")
        assert r.status_code == 200

    def test_create_menu(self):
        payload = {"title": "menu1", "description": "menu1 description"}
        r = requests.post(f"{self.API_URL}/api/v1/menus", json=payload)
        assert r.status_code == 201

    def test_get_menu(self):
        id = self.get_id_menu()
        r = requests.get(f"{self.API_URL}/api/v1/menus/{id}")
        myjson = r.json()
        assert myjson['title'] == "menu1"
        assert myjson['description'] == "menu1 description"
        assert myjson['submenus_count'] == 0
        assert myjson['dishes_count'] == 0
        assert r.status_code == 200

    def test_update_menu(self):
        id = self.get_id_menu()
        payload = {
            "title": "menu1 updated",
            "description": "menu1 description updated",
        }
        r = requests.patch(f"{self.API_URL}/api/v1/menus/{id}", json=payload)
        r = requests.get(f"{self.API_URL}/api/v1/menus/{id}")
        myjson = r.json()
        assert myjson['title'] == "menu1 updated"
        assert myjson['description'] == "menu1 description updated"
        assert myjson['submenus_count'] == 0
        assert myjson['dishes_count'] == 0
        assert r.status_code == 200

    def test_delete_menu(self):
        id = self.get_id_menu()
        r = requests.delete(f"{self.API_URL}/api/v1/menus/{id}")
        myjson = r.json()
        assert myjson['status'] == True
        assert myjson['message'] == "The menu has been deleted"
        assert r.status_code == 200

    def test_get_submenus(self):
        self.test_create_menu()
        api_test_menu_id = self.get_id_menu()
        r = requests.get(
            f"{self.API_URL}/api/v1/menus/{api_test_menu_id}/submenus/?skip = 0 & limit = 100",
        )
        assert r.status_code == 200

    def test_create_submenu(self):
        api_test_menu_id = self.get_id_menu()
        payload = {
            "title": "submenu1", "description": "submenu1 description",
            "main_menu_id": api_test_menu_id,
        }
        r = requests.post(
            f"{self.API_URL}/api/v1/menus/{api_test_menu_id}/submenus", json=payload,
        )
        assert r.status_code == 201

    def test_get_submenu(self):
        api_test_menu_id = self.get_id_menu()
        id_submenu = self.get_id_submenu()
        r = requests.get(
            f"{self.API_URL}/api/v1/menus/{api_test_menu_id}/submenus/{id_submenu}",
        )
        myjson = r.json()
        assert myjson['title'] == "submenu1"
        assert myjson['description'] == "submenu1 description"
        assert myjson['main_menu_id'] == api_test_menu_id
        assert myjson['dishes_count'] == 0
        assert r.status_code == 200

    def test_update_submenu(self):
        api_test_menu_id = self.get_id_menu()
        id_submenu = self.get_id_submenu()
        payload = {
            "title": "submenu1 updated",
            "description": "submenu1 description updated",
        }
        r = requests.patch(
            f"{self.API_URL}/api/v1/menus/{api_test_menu_id}/submenus/{id_submenu}", json=payload,
        )
        r = requests.get(
            f"{self.API_URL}/api/v1/menus/{api_test_menu_id}/submenus/{id_submenu}",
        )
        myjson = r.json()
        assert myjson['title'] == "submenu1 updated"
        assert myjson['description'] == "submenu1 description updated"
        assert myjson['main_menu_id'] == api_test_menu_id
        assert myjson['dishes_count'] == 0
        assert r.status_code == 200

    def test_delete_submenu(self):
        api_test_menu_id = self.get_id_menu()
        id_submenu = self.get_id_submenu()
        r = requests.delete(
            f"{self.API_URL}/api/v1/menus/{api_test_menu_id}/submenus/{id_submenu}",
        )
        myjson = r.json()
        assert myjson['status'] == True
        assert myjson['message'] == "The submenu has been deleted"
        assert r.status_code == 200

    def test_get_dishes(self):
        self.test_create_submenu()
        api_test_menu_id = self.get_id_menu()
        id_submenu = self.get_id_submenu()
        r = requests.get(
            f"{self.API_URL}/api/v1/menus/{api_test_menu_id}/submenus/{id_submenu}/dishes",
        )
        assert r.status_code == 200

    def test_create_dish(self):
        api_test_menu_id = self.get_id_menu()
        id_submenu = self.get_id_submenu()
        payload = {
            "title": "dish1",
            "description": "dish1 description",
            "submenu_id": id_submenu,
            "price": "10.20",
        }
        r = requests.post(
            f"{self.API_URL}/api/v1/menus/{api_test_menu_id}/submenus/{id_submenu}/dishes", json=payload,
        )
        myjson = r.json()
        assert myjson['title'] == "dish1"
        assert myjson['description'] == "dish1 description"
        assert myjson['submenu_id'] == id_submenu
        assert myjson['price'] == "10.20"
        assert r.status_code == 201

    def test_get_dish(self):
        api_test_menu_id = self.get_id_menu()
        id_submenu = self.get_id_submenu()
        id_dish = self.get_id_dish()
        r = requests.get(
            f"{self.API_URL}/api/v1/menus/{api_test_menu_id}/submenus/{id_submenu}/dishes/{id_dish}",
        )
        myjson = r.json()
        assert myjson['title'] == "dish1"
        assert myjson['description'] == "dish1 description"
        assert myjson['submenu_id'] == id_submenu
        assert myjson['price'] == "10.20"
        assert r.status_code == 200

    def test_update_dish(self):
        api_test_menu_id = self.get_id_menu()
        id_submenu = self.get_id_submenu()
        id_dish = self.get_id_dish()
        payload = {
            "title": "dish1 updated",
            "description": "dish1 description updated",
            "price": "20.30",
        }
        r = requests.patch(
            f"{self.API_URL}/api/v1/menus/{api_test_menu_id}/submenus/{id_submenu}/dishes/{id_dish}", json=payload,
        )
        r = requests.get(
            f"{self.API_URL}/api/v1/menus/{api_test_menu_id}/submenus/{id_submenu}/dishes/{id_dish}",
        )
        myjson = r.json()
        assert myjson['title'] == "dish1 updated"
        assert myjson['description'] == "dish1 description updated"
        assert myjson['price'] == "20.30"
        assert r.status_code == 200

    def test_delete_dish(self):
        api_test_menu_id = self.get_id_menu()
        id_submenu = self.get_id_submenu()
        id_dish = self.get_id_dish()
        r = requests.delete(
            f"{self.API_URL}/api/v1/menus/{api_test_menu_id}/submenus/{id_submenu}/dishes/{id_dish}",
        )
        myjson = r.json()
        assert myjson['status'] == True
        assert myjson['message'] == "The dish has been deleted"
        self.test_delete_menu()
        assert r.status_code == 200
