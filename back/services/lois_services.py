from database.models import LoiTravail

def get_all_lois():
    return LoiTravail.query.all()
