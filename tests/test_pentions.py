import unittest
from fastapi.testclient import TestClient
from main import app
from app.backend.db.database import create_db, get_db
from sqlalchemy.orm import Session
from app.backend.db.models import PentionModel
from app.backend.schemas import Pention, UpdatePention
from app.backend.classes.pention_class import PentionClass

class TestPentions(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        self.db = next(get_db())
        create_db(self.db)

    def test_index(self):
        pention1 = PentionModel(name="Pension 1", amount=1000)
        pention2 = PentionModel(name="Pension 2", amount=2000)
        self.db.add_all([pention1, pention2])
        self.db.commit()

        response = self.client.get("/pentions/")

        self.assertEqual(response.status_code, 200)

        expected_data = [
            {"id": pention1.id, "name": "Pension 1", "amount": 1000},
            {"id": pention2.id, "name": "Pension 2", "amount": 2000},
        ]
        self.assertEqual(response.json(), {"message": expected_data})

if __name__ == "__main__":
    unittest.main()