from sonya.core.database.models import Base
from sonya.core.database.session import engine

Base.metadata.create_all(engine)
