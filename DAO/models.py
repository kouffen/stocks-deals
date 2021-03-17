from sqlalchemy import table, Column, String, INTEGER, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from DAO import database_access as db


class Enterprise(db.Base):
    """ The Enterprise table / class for company infos """
    __tablename__ = 'enterprises'

    FORMAT_DATE = '%d/%m/%Y'

    def __init__(self, name_enterprise, reg_number, niu, creation_date, fiscal_year,
                 phone_contact, email_address, location_address):
        self.name_enterprise = name_enterprise
        self.reg_number = reg_number
        self.niu = niu
        self.creation_date = datetime.strptime(creation_date, self.FORMAT_DATE)
        self.fiscal_year = fiscal_year
        self.phone_contact = phone_contact
        self.email_address = email_address
        self.location_address = location_address

    id_enterprise = Column(INTEGER, nullable=False, primary_key=True)
    name_enterprise = Column(String, nullable=False)
    reg_number = Column(String)
    niu = Column(String)
    creation_date = Column(DateTime)
    fiscal_year = Column(INTEGER)
    phone_contact = Column(String)
    email_address = Column(String)
    location_address = Column(String)
    sessiono_id = Column(INTEGER, ForeignKey="sessiono.id_sessiono")
    creation_date = Column(datetime.timestamp())
    # get a list activities of our company
    activities = relationship("Activity", order_by="Activity.id_activity", back_populates="enterprise")


class Activity(db.Base):
    """ Acivities of our company"""
    __tablename__ = 'activities'

    id_activity = Column(INTEGER, nullable=False, primary_key=True)
    activity_name = Column(String)
    # set our foreign key column
    enterprise_id = Column(INTEGER, ForeignKey("enterprises.id_enterprise"))
    sessiono_id = Column(INTEGER, ForeignKey="sessiono.id_sessiono")
    creation_date = Column(datetime.timestamp())

    enterprise = relationship("Enterprise", back_populates="activities")


class Operator(db.Base):
    """ A person who manage the stock"""
    __tablename__ = 'operators'

    id_operator = Column(INTEGER, nullable=False, primary_key=True)
    login = Column(String)
    password = Column(String)
    name = Column(String)
    surname = Column(String)
    birthday_operator = Column(datetime)
    birthplace_operator = Column(String)
    address_operator = Column(String)
    creation_date = Column(datetime.timestamp())


class ProductCategory(db.Base):
    """define group of products"""
    __tablename__ = 'productscategories'

    id_category = Column(INTEGER, nullable=False, primary_key=True)
    name_category = Column(String)
    comments_category = Column(String)
    sessiono_id = Column(INTEGER, ForeignKey="sessiono.id_sessiono")
    creation_date = Column(datetime.timestamp())
    # get All the products assigned to a specific category (inverse relationship OnetoMany)
    products = relationship("Product", order_by="Product.id_product", back_populates="category")


class Product(db.Base):
    """ The items in our store"""
    __tablename__ = 'products'

    id_product = Column(INTEGER, nullable=False, primary_key=True)
    reference_product = Column(String)
    name_product = Column(String)
    quantity_product = Column(INTEGER)
    bar_code_product = Column(String)
    category_id = Column(INTEGER, ForeignKey='productscategories.id_category')
    sessiono_id = Column(INTEGER, ForeignKey="sessiono.id_sessiono")
    creation_date = Column(datetime.timestamp())

    category = relationship("ProductCategory", back_populates="products")

    inputstocks = relationship("InputStock", order_by="InputStock.id_input", back_populates="product")

    outputstocks = relationship("OutputStock", order_by="OutputStock.id_input", back_populates="product")


class InputStock(db.Base):
    """ Record new input in our store"""
    __tablename__ = "inputstocks"
    id_input = Column(INTEGER, nullable=False, primary_key=True)
    date_input = Column(datetime.timestamp())
    # link the input with the product
    product_id = Column(INTEGER, ForeignKey="products.id_product")
    sessiono_id = Column(INTEGER, ForeignKey="sessiono.id_sessiono")
    quantity_input = Column(float)
    creation_date = Column(datetime.timestamp())

    product = relationship("Product", back_populates="inputstocks")


class OutputStock(db.Base):
    """ Record all the ouput of the store"""
    __tablename__ = "outpustocks"
    id_input = Column(INTEGER, nullable=False, primary_key=True)
    date_input = Column(datetime.timestamp())
    # link the input with the product
    product_id = Column(INTEGER, ForeignKey="products.id_product")
    sessiono_id = Column(INTEGER, ForeignKey="sessiono.id_sessiono")
    quantity_input = Column(float)

    product = relationship("Product", back_populates="outputstocks")


class SessionOperator(db.Base):
    """ All the actions of an operator shloud by known by its sessions(interval)"""
    __tablename__ = "sessionoperator"
    id_sessiono = Column(INTEGER, nullable=False, primary_key=True)
    operator_id = Column(INTEGER, ForeignKey='Operator.id_operator')
    debut_sessiono = Column(datetime.timestamp())
    fin_session0 = Column(datetime.timestamp())
    creation_date = Column(datetime.timestamp())




def main():

    jean_et_frere = Enterprise('Jean Et Frere Sarl', 'RC/DLA/2018/A/25', 'P01523456975465',
                               '15/12/2018', '2021', '+237699188584', 'talajeanmarie@gmail.com',
                               'Brazzaville, derriere le Lycee')

    print('la premiere entreprise creer est : %s' % jean_et_frere.name_enterprise)
    print(' elle a ete creer le : %s' % jean_et_frere.creation_date)
    print(' sa cle est : %s' % jean_et_frere.id)

    db.Base.metadata.create_all(db.engine)
    session = db.Session()
    session.add(jean_et_frere)
    for instance in session.query(Enterprise).order_by(Enterprise.id):
        print(instance.fiscal_year)

    print(str(jean_et_frere.id))
    session.commit()
    session.close()


if __name__ == '__main__':
    main()




