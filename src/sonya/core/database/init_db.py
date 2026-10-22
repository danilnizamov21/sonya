from sonya.database.models import Base
from sonya.database.session import engine

Base.metadata.create_all(engine)
