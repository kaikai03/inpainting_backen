__base_table__ = 'base'
__workqueue_table__ = 'workqueue'
__completed_table__ = 'completed'
__trash_table__ = 'trash'



from tinydb import TinyDB, Query, table, where
import app.utils as u
import threading
from tinydb.operations import increment
import random
from enum import Enum
import math


class stat(str, Enum):
    cpl = 'completed'
    stop = 'stopped'
    que = 'queuing'
    err = 'error'


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

    @staticmethod
    def get_all_id(table_name: str) -> List[str]:
        return list(DB.db_.storage.read()[table_name].keys())

    @staticmethod
    def get_table_size(work_status: Union[stat.cpl, stat.que, stat.stop, stat.err] = stat.cpl) -> int:
        table_ = DB.completed if work_status == stat.cpl else DB.workqueue
        return len(table_)

    @staticmethod
    def get_trash_size() -> int:
        return len(DB.trash)

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

            if document.get('doc_code') is None:
                document['doc_code'] = u.generate_doc_id()

            if document.get('created') is None:
                document['created'] = u.get_standard_time()
                document['updated'] = ''
            else:
                document['updated'] = u.get_standard_time()

            return super().insert(document)

        def upsert(self, document: Mapping, cond: Optional[Query] = None):
            # 因为doc_code在插入过程中会被改变，会同时出现插入与更新操作。
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
    def work_create(tasks: List[dict], work_status: Union[stat.stop, stat.que] = stat.que):
        status = []
        for item in tasks:
            item['status'] = work_status
            status.append(DB.workqueue.insert(item))
            print("create:", item)
        return status

    @staticmethod
    def work_change(doc_code: str, work_status: Union[stat.cpl, stat.que, stat.stop, stat.err] = stat.cpl):
        items = DB.workqueue.search(DB.query.doc_code == doc_code)
        for item in items:
            item['status'] = work_status
            if work_status == stat.cpl:
                DB.completed.insert(item)
                DB.workqueue.remove(doc_ids=[item.doc_id])
                print("completed move:", item.doc_id)
            else:
                DB.workqueue.update({'status': work_status}, doc_ids=[item.doc_id])

    @staticmethod
    def work_drop(doc_codes: List[str] = [], doc_ids: Optional[Iterable[int]] = None):
        # 已完成的任务将不会被直接删除，而是进入回收站
        docs = []
        for doc_code in doc_codes:
            for item in DB.workqueue.search(DB.query.doc_code == doc_code):
                if item['status'] == stat.cpl:
                    DB.trash.insert(item)

                docs.append(item.doc_id)

        if doc_ids is not None:
            docs.extend(doc_ids)

        if len(docs) > 0:
            DB.workqueue.remove(doc_ids=list(set(docs)))

        print("work_drop:", docs)
        return docs

    @staticmethod
    def get_random(count: int):
        doc_ids = DB.get_all_id(__completed_table__)
        db_size = len(DB.completed)
        count_ = db_size if count > db_size else count

        random.shuffle(doc_ids)
        items = []
        for doc_id in doc_ids:
            item = DB.completed.get(doc_id=int(doc_id))
            if item is not None:
                # 这个状态判断现在多余了，因为分表
                if item['status'] != stat.cpl:
                    items.append(item)
            if len(items) >= count_:
                return items
        return items

    @staticmethod
    def get_task(start: int, end, work_status: Union[stat.cpl, stat.que, stat.stop, stat.err]
                 ) -> List[str]:
        table_ = DB.completed if work_status == stat.cpl else DB.workqueue

        if isinstance(end, int):
            if (start + end) > len(table_):
                return []

        return table_.all()[start:end]

    @staticmethod
    def get_imgs_name(doc_codes: List[str] = [],
                      work_status: Union[stat.cpl, stat.que, stat.stop, stat.err] = stat.cpl) -> List[str]:
        results = []
        for doc_code in doc_codes:
            # 虽然code是唯一的，但没用get的原因是,search返回数组，空数组就能跳过了，减少错误判断
            if work_status == stat.cpl:
                result = DB.completed.search(DB.query.doc_code == doc_code)
            else:
                result = DB.workqueue.search(DB.query.doc_code == doc_code)
            results.extend(result)

        return [item['img'] for item in results]

    @staticmethod
    def get_videos_name(doc_codes: List[str] = []) -> List[str]:
        results = []
        for doc_code in doc_codes:
            # 虽然code是唯一的，但没用get的原因是,search返回数组，空数组就能跳过了，减少错误判断
            result = DB.completed.search(DB.query.doc_code == doc_code)
            for item in result:
                results.extend([doc_code + '_' + postfix +'.mp4' for postfix in item['postfix']])
        return results



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