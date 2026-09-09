import unittest
import json
import os
import app as flask_app
from database.db_init import init_db
from services.db_service import DB_PATH

class BloodBankSystemTestCase(unittest.TestCase):
    def setUp(self):
        init_db()
        flask_app.app.config['TESTING'] = True
        self.client = flask_app.app.test_client()

    def test_01_login_admin(self):
        res = self.client.post('/api/auth/login', json={
            'username': 'admin',
            'password': 'Admin@123'
        })
        data = res.get_json()
        self.assertTrue(data['success'])
        self.assertEqual(data['user']['role'], 'ADMIN')

    def test_02_login_doctor(self):
        res = self.client.post('/api/auth/login', json={
            'username': 'doctor',
            'password': 'Doctor@123'
        })
        data = res.get_json()
        self.assertTrue(data['success'])
        self.assertEqual(data['user']['role'], 'MEDICAL_OFFICER')

    def test_03_create_and_sign_record_workflow(self):
        # 1. Login as Staff
        self.client.post('/api/auth/login', json={'username': 'staff', 'password': 'Staff@123'})

        # 2. Create Donor Record Draft
        payload = {
          'save_as_draft': True,
          'donor': {
            'full_name': 'Ramesh Kumar Patil',
            'gender': 'Male',
            'date_of_birth': '1995-05-15',
            'age': 31,
            'mobile_number': '9876543210',
            'residential_address': 'Kothrud, Pune',
            'city_district': 'Pune',
            'blood_group_known': 'B+',
            'donation_type': 'Voluntary'
          },
          'medical_exam': {
            'weight_kg': 68,
            'pulse_rate': 74,
            'bp_systolic': 120,
            'bp_diastolic': 80,
            'hemoglobin_g_dl': 14.2,
            'body_temperature': 98.4,
            'skin_site_inspection': 'Satisfactory',
            'screening_outcome': 'ELIGIBLE'
          },
          'donation_details': {
            'blood_bag_number': 'BAG-2026-TEST01',
            'bag_type': 'Single',
            'volume_ml': 350
          }
        }
        res = self.client.post('/api/records', json=payload)
        data = res.get_json()
        self.assertTrue(data['success'])
        record_id = data['record_id']

        # 3. Submit for Medical Verification
        res_sub = self.client.post(f'/api/records/{record_id}/submit')
        self.assertTrue(res_sub.get_json()['success'])

        # 4. Login as Medical Officer
        self.client.post('/api/auth/login', json={'username': 'doctor', 'password': 'Doctor@123'})

        # 5. Sign Record
        dummy_sig = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="
        res_sign = self.client.post(f'/api/records/{record_id}/sign', json={
            'signature_data': dummy_sig,
            'medical_notes': 'Verified and eligible.'
        })
        self.assertTrue(res_sign.get_json()['success'])

        # 6. Verify record is locked
        res_rec = self.client.get(f'/api/records/{record_id}')
        rec_data = res_rec.get_json()
        self.assertEqual(rec_data['record']['status'], 'SIGNED')
        self.assertIsNotNone(rec_data['signature']['signature_data'])

    def test_04_excel_export(self):
        self.client.post('/api/auth/login', json={'username': 'admin', 'password': 'Admin@123'})
        res = self.client.get('/api/export/excel')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.mimetype, 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

    def test_05_print_record(self):
        self.client.post('/api/auth/login', json={'username': 'staff', 'password': 'Staff@123'})
        res = self.client.get('/print/1')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'JANKALYAN BLOOD CENTRE', res.data)

if __name__ == '__main__':
    unittest.main()
