from linkstore.linkstore import Linkstore
from linkstore.link_storage import SqliteLinkStorage

def before_scenario(context, scenario):
    context.link_storage = SqliteLinkStorage(in_memory=True)
    context.linkstore = Linkstore(context.link_storage)
