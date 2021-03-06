from .views import app
from .models import graph
from .email_template import *
#from .nltk_model import *
from .utils import *


def create_uniqueness_constraint(label, property):
    query = "CREATE CONSTRAINT ON (n:{label}) ASSERT n.{property} IS UNIQUE"
    graph.run(query.format(label=label, property=property))

create_uniqueness_constraint("User", "username")
create_uniqueness_constraint("Tag", "name")
create_uniqueness_constraint("Post", "id")