__base_table__ = 'base'
__workqueue_table__ = 'workqueue'
__completed_table__ = 'completed'
__trash_table__ = 'trash'


from tinydb import TinyDB, Query, table, where
import app.utils as u
import threading
from tinydb.operations import increment
import random

from types import FunctionType
from typing import (
    Callable,
    Dict,
    Iterable,
    Iterator,
    List,
    Mapping,
    Optional,
    Union,
    cast
)


def sync(lock):
    # 用于数据编辑的锁。本项目几乎全异步函数，以防万一加个锁，
    # 反正暂时运算密集的部分都会分布出去，本项目没有耗时计算。
    def sync_lock(fn):
        def new_fn(*args, **kwargs):
            lock.acquire()
            print("db_lock:",fn.__name__)
            try:
                return fn(*args, **kwargs)
            finally:
                lock.release()
                print("db_unlock")
        new_fn.__name__ = fn.__name__
        new_fn.__doc__ = fn.__doc__
        return new_fn
    return sync_lock


class DB(object):
    db_ = TinyDB('./db.json')
    query = Query()
    query2 = Query()

    @staticmethod
    def get_last_item_id() -> int:
        return DB.db_.table(__base_table__).get(where('item_id_auto').exists())['item_id_auto']

    class auto_time_table(table.Table):
        # 相当于重载tinyDB的方法，实现在原功能基础上附带插入id，创建时间，更新时间等功能。
        mutex = threading.Lock()

        @staticmethod
        def auto_increate_item_id() -> int:
            # 生成自增编号
            # base初始化时，会插入一条带有item_id_auto字段的doc，用作自增编号
            # 主要用于视频工作项的全局生成序号
            DB.db_.table(__base_table__).update_auto_id(increment('item_id_auto'), where('item_id_auto').exists())
            return DB.get_last_item_id()

        @sync(mutex)
        def insert(self, document: Mapping) -> List[int]:
            # 如果插入对象是 视频处理工作对象时，新增item_id字段，作为工作任务的id
            if super().name == __workqueue_table__:
                if document.get('item_id') is None:
                    document['item_id'] = self.auto_increate_item_id()

            if document.get('doc') is None:
                document['doc'] = u.generate_doc_id()

            if document.get('created') is None:
                document['created'] = u.get_standard_time()
                document['updated'] = ''
            else:
                document['updated'] = u.get_standard_time()

            return super().insert(document)

        def upsert(self, document: Mapping, cond: Optional[Query] = None):
            # 因为doc在插入过程中会被改变，会同时出现插入与更新操作。
            # 懒得处理，直接禁用
            raise Exception("此版本禁止使用upsert")

        @sync(mutex)
        def insert_multiple(self, documents: Iterable[Mapping]) -> List[int]:
            for document in documents:
                return self.insert(document)

        @sync(mutex)
        def update(
                self,
                fields: Union[Mapping, Callable[[Mapping], None]],
                cond: Optional[Query] = None,
                doc_ids: Optional[Iterable[int]] = None,
        ) -> List[int]:
            t = u.get_standard_time()
            if type(fields) is not FunctionType:
                fields['updated'] = t
                return super().update(fields, cond, doc_ids)
            else:
                tmp = super().update(fields, cond, doc_ids)
                super().update({'updated': t}, cond, doc_ids)
                return tmp

        def update_auto_id(
                self,
                fields: Union[Mapping, Callable[[Mapping], None]],
                cond: Optional[Query] = None,
                doc_ids: Optional[Iterable[int]] = None,
        ) -> List[int]:
            t = u.get_standard_time()
            if type(fields) is not FunctionType:
                fields['updated'] = t
                return super().update(fields, cond, doc_ids)
            else:
                tmp = super().update(fields, cond, doc_ids)
                super().update({'updated': t}, cond, doc_ids)
                return tmp

        @sync(mutex)
        def remove(
                self,
                cond: Optional[Query] = None,
                doc_ids: Optional[Iterable[int]] = None,
        ) -> List[int]:
            return super().remove(cond, doc_ids)

    db_.table_class = auto_time_table
    base = db_.table(__base_table__)

    workqueue = db_.table(__workqueue_table__)
    completed = db_.table(__completed_table__)
    trash = db_.table(__trash_table__)
    print('TinyDB initial completed')

    def __init__(self):
        if len(DB.base) == 0:
            DB.base.insert({"item_id_auto": 0})
        print('TinyDB __init__ completed')

    @staticmethod
    def work_finish(doc_id: str, work_status: Union['pic', 'video', 'error'] = 'video'):
        items = DB.workqueue.search(DB.query.doc == doc_id)
        for item in items:
            item['status'] = work_status
            DB.completed.insert(item)
            DB.workqueue.remove(doc_ids=[item.doc_id])
            print("move:", item.doc_id)

    @staticmethod
    def work_drop(doc_ids: list):
        docs = []
        for doc_id in doc_ids:
            for item in DB.workqueue.search(DB.query.doc == doc_id):
                docs.append(item.doc_id)

        if len(docs) > 0:
            DB.workqueue.remove(doc_ids=list(set(docs)))

        print("work_drop:", docs)

    @staticmethod
    def get_random(count: int):
        last_id = DB.get_last_item_id()
        db_size = len(DB.completed)
        count_ = db_size if count > db_size else count

        doc_ids = list(range(1, last_id+1))
        random.shuffle(doc_ids)
        items = []
        for doc_id in doc_ids:
            item = DB.completed.get(doc_id=doc_id)
            if item is not None:
                # TODO:正式的时候要换成video
                if item['status'] != 'error':
                    items.append(item)
            if len(items) >= count_:
                return items
        return items



db = DB()



# db.insert_multiple([{'id': 1, 'type': 'a','name':'carry'},{'id': 2, 'type': 'b','name':'tomas'}])
# db.insert({'id': 9, 'type': 'c','name':'cfff'})
# db.upsert({'id': 9, 'type': 'e','name':'cfff'},Q.id ==9)

# Q = Query()
# P = Query()
# db.search(Q.id == 9)
# db.search(Q['type'] == 'a')
# db.search(Q.name.matches('^J'))
# db.search(Q.id.test(lambda val, m, n: m <= val <= n, 2, 3))
# db.search(Q.grounp.any(['a', 'b']))
# db.search(Q.grounp.any(P.type == 'read')) # 内部也是一个集合时可以这么写
#
# el = db.get(Q.id == 9)
# el.doc_id
# db.get(doc_id=1)
# db.contains(Q.type == 'a')
# db.count(Q.type == 'a')
# db.update({'grounp':['苹果x', 'b']}, Q.type =='b')
# db.remove(Q.名字 == '苹果')
# db.remove(Q.new.exists())
# db.remove(Q.id == 9)

# db.insert({'new':{'id': 1, 'type': 'a','name':'ttt'}})
# db.update(delete('key1'), User.name == 'John')
# db.upsert({'id': increment('id'), 'name': 'CC', 'type': 'c'}, Q.type == 'c')

# db.table('_default').all()
#
# len(db)
# len(completed_tb)
# db.count(Q.id.exists())
# db.completed.remove(Query().index.exists())
# base_tb.name