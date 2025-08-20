# backend/accounts/models.py
from mongoengine import Document, StringField, EmailField
from django.contrib.auth.hashers import make_password, check_password

class User(Document):
    username = StringField(required=True)
    email = EmailField(required=True, unique=True)
    password = StringField(required=True)
    mobile_no = StringField(required=True)
    city = StringField()
    role = StringField(choices=('management','staff','guest'), default='guest')

    def set_password(self, raw_password):
        
        self.password = make_password(raw_password)
        self.save()

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def to_dict(self):
        return {
            "id": str(self.id),
            "username": self.username,
            "email": self.email,
            "mobile_no": self.mobile_no,
            "city": self.city,
            "role": self.role
        }
