from application import db,create_app
from application.model import Role

app = create_app()
def create_role():
    admin_role = Role(name='Admin')
    sponsor = Role(name="Sponsor")
    influencer = Role(name='Influencer')
    db.session.add(admin_role)
    db.session.add(sponsor)
    db.session.add(influencer)
    db.session.commit()



if __name__ == '__main__':
    with app.app_context():
       create_role()