from app.mod_commodity.models import Commodity
from app import db

def get_all_data():
    return Commodity.query.all()

def select_by_id(id):
    return Commodity.query.filter_by(id=id).first()

#update or insert data
def insert_data(commodity):
    recordid = 0
    if(commodity.id==0):
        db.session.add(commodity)
        db.session.commit()
        #recordid = commodity.id
    else:
        data = {'desc':commodity.desc,'location':commodity.location,'event_name':commodity.event_name,
                'person':commodity.person,'tel':commodity.tel}
        Commodity.query.filter_by(id=commodity.id).update(data)
        db.session.commit()

    return recordid

def delete_by_id(commodity):
    db.session.delete(commodity)
    db.session.commit()

#get all blocks of the chain
def get_all_blocks():
    return Commodity.query.filter_by(status='Y').order_by(Commodity.chain_index).all()


#update block chain's data
def update_hash_data(commodity):
    data = {'current_hash':commodity.current_hash,'pre_hash':commodity.pre_hash,'random_num':commodity.random_num,
           'chain_index':commodity.chain_index,'status':commodity.status}
    Commodity.query.filter_by(id=commodity.id).update(data)
    db.session.commit()

    return commodity.id