from bson.objectid import ObjectId

def objectid_to_str(obj):
        obj['_id'] = obj['_id'].__str__()
        
        return obj