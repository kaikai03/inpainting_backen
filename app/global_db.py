from tinydb import TinyDB, where, Query
from tinydb.operations import increment
db1 = 'origin'


db = TinyDB('./db.json')
# db.insert_multiple([{'id': 1, 'type': 'a','name':'carry'},{'id': 2, 'type': 'b','name':'tomas'}])
Q = Query()
P = Query()
db.search(Q.type == 'a')
db.search(Q['type'] == 'a')
db.search(where('type') == 'a')
db.search(Q.name.matches('^J'))
db.search(Q.id.test(lambda val, m, n: m <= val <= n, 2, 3))
db.search(Q.grounp.any(['a', 'b']))
db.search(Q.grounp.any(P.type == 'read')) # 内部也是一个集合时可以这么写

el = db.get(Q.type == 'a')
el.doc_id
db.get(doc_id=1)
db.contains(Q.type == 'a')
db.count(Q.type == 'a')
db.update({'grounp':['苹果x', 'b']}, Q.type =='b')
# db.remove(Q.名字 == '苹果')
# db.remove(Q.new.exists())
# db.remove(Q.type == 'c')

# db.insert({'new':{'id': 1, 'type': 'a','name':'ttt'}})
# db.update(delete('key1'), User.name == 'John')
db.upsert({'id': increment('id'), 'name': 'CC', 'type': 'c'}, Q.type == 'c')

db.table('_default').all()

len(db)
db.count(Q.id.exists())