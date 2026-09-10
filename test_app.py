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
          },
          'consent': {
            'consent_given': True,
            'abnormal_results_notify': True,
            'donor_signature_data': "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="
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
        self.assertIsNotNone(rec_data['consent']['donor_signature_data'])

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

    def test_06_admin_user_management(self):
        # 1. Login as Admin
        self.client.post('/api/auth/login', json={'username': 'admin', 'password': 'Admin@123'})
        with flask_app.app.app_context():
            flask_app.execute_db("DELETE FROM users WHERE username LIKE 'temp_user%'")

        # 2. Create User
        res_create = self.client.post('/api/users', json={
            'username': 'temp_user_test',
            'password': 'TempPassword@123',
            'full_name': 'Temp Test User',
            'role': 'STAFF',
            'medical_reg_no': 'TEMP-101'
        })
        data_create = res_create.get_json()
        self.assertTrue(data_create['success'])
        temp_user_id = data_create['user_id']

        # 3. Update User (Name & Password)
        res_update = self.client.put(f'/api/users/{temp_user_id}', json={
            'username': 'temp_user_updated',
            'full_name': 'Updated Temp Name',
            'role': 'MEDICAL_OFFICER',
            'medical_reg_no': 'MO-TEMP-999',
            'password': 'NewPassword@456'
        })
        self.assertTrue(res_update.get_json()['success'])

        # 4. Verify login with new password works
        res_login_new = self.client.post('/api/auth/login', json={
            'username': 'temp_user_updated',
            'password': 'NewPassword@456'
        })
        self.assertTrue(res_login_new.get_json()['success'])

        # 5. Switch back to Admin
        self.client.post('/api/auth/login', json={'username': 'admin', 'password': 'Admin@123'})

        # 6. Attempt to delete primary Admin account -> expect HTTP 400 error
        res_del_admin = self.client.delete('/api/users/1')
        self.assertEqual(res_del_admin.status_code, 400)
        self.assertIn('cannot be soft-deleted', res_del_admin.get_json()['message'])

        # 7. Delete temporary user -> expect success
        res_del_temp = self.client.delete(f'/api/users/{temp_user_id}')
        self.assertTrue(res_del_temp.get_json()['success'])

    def test_07_rbac_user_management(self):
        # Login as Staff
        self.client.post('/api/auth/login', json={'username': 'staff', 'password': 'Staff@123'})

        # Verify access is denied (403) for non-admin
        self.assertEqual(self.client.get('/api/users').status_code, 403)
        self.assertEqual(self.client.post('/api/users', json={'username': 'x', 'password': 'y', 'full_name': 'z'}).status_code, 403)
        self.assertEqual(self.client.put('/api/users/1', json={'username': 'admin'}).status_code, 403)
        self.assertEqual(self.client.delete('/api/users/1').status_code, 403)

if __name__ == '__main__':
    unittest.main()
