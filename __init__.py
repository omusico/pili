
def model2dict(model):
    data=[]
    from types import ListType
    if type(model) is ListType:
        has_key_name = False
        if len(model) > 0 and model[0].key().name() is not None:
            has_key_name = True
        for i in model:
            data.append( dict( (prop, getattr(i, prop)) for prop in i.properties()))
            if has_key_name is True:
                data[-1]['key_name'] = i.key().name()
    else:
        data = dict( (prop, getattr(model, prop)) for prop in model.properties())
        if model.key().name() is not None:
            data['key_name'] = model.key().name()
    return data

def sortlist(items, key):
    from operator import itemgetter
    return sorted(items, key=itemgetter(key))

def filllist(items, default_value = None):
    fields = set()
    for i in items:
        fields |= set(i.keys())
    for i in items:
        diff = fields - set(i.keys())
        if len(diff) == 0:
            continue
        for k in diff:
            i[k] = default_value

    return items


def joinlist(d1, d2, k1, k2, jointype='inner'):
    if jointype == 'right':
        d1, d2 = d2, d1

    data = []
    for i in d1:
        key_value = i[k1]
        # find pos in d2
        find_row = False
        for j in d2:
            if j[k2] == key_value:
                find_row = True
                d = dict()
                d.update(i)
                d.update(j)
                data.append(d)
        if jointype != 'inner' and find_row is False:
            data.append(i)
    return data


def model2json(model):
    from django.utils import simplejson as json
    return json.dumps(model2dict(model))


