from ZODB.FileStorage import FileStorage
from ZODB.DB import DB
import transaction

class EventCollection(object) :
    def __init__(self, filename) :
        self.storage = FileStorage(filename)
        self.db = DB(self.storage)
        self.connection = self.db.open()
        self.store = self.connection.root()
        self.events_since_save = 0

    def new_key(self) :
        return max(self.store.keys())+1 if self.store.keys() else 0

    def save(self):
        transaction.commit()

    def events(self) :
        for key in self.store.keys() :
            yield self.store[key]

    def add_event(self, event) :
        self.store[self.new_key()] = event
        self.events_since_save += 1
        if self.events_since_save > 10000 :
            print "Saving..."
            self.events_since_save = 0
            self.save()
