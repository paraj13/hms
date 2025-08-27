from mongoengine import Document, StringField, FloatField, IntField, ListField, DateTimeField, BooleanField, ReferenceField
import datetime

class Room(Document):
    number = IntField(required=True, unique=True)
    type = StringField(required=True, choices=['single', 'double', 'suite'])
    status = StringField(required=True, choices=['available', 'booked', 'maintenance'], default='available')
    price = FloatField(required=True)

    cover_image = StringField(required=False)          
    other_images = ListField(StringField(), default=[])

    def to_dict(self):
        return {
            'id': str(self.id),
            'number': self.number,
            'type': self.type,
            'status': self.status,
            'price': self.price,
            "cover_image": self.cover_image,
            "other_images": self.other_images,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }


class Service(Document):
    name = StringField(required=True, unique=True)
    category = StringField(required=True)
    description = StringField()
    price = FloatField(required=True)
    is_active = BooleanField(default=True)

    created_at = DateTimeField(default=datetime.datetime.utcnow)
    updated_at = DateTimeField(default=datetime.datetime.utcnow)

    def save(self, *args, **kwargs):
        self.updated_at = datetime.datetime.utcnow()
        return super(Service, self).save(*args, **kwargs)

    def to_dict(self):
        return {
            "id": str(self.id),
            "name": self.name,
            "category": self.category,
            "description": self.description,
            "price": self.price,
            "is_active": self.is_active,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
        
class ServiceBooking(Document):
    meta = {'collection': 'service_bookings'}
    user = ReferenceField('User', required=True)  # direct reference to User
    service = ReferenceField(Service, required=True)
    booking_date = DateTimeField(default=datetime.datetime.utcnow)
    date = StringField()
    time = StringField()
    notes = StringField()  # optional
    status = StringField(default="pending")

    def __str__(self):
        return f"Booking {self.id} - User: {self.user.id} Service: {self.service.name}"