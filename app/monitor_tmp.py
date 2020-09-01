# coding: utf-8

import psutil


def get_cpu_count():
    return psutil.cpu_count()


class monitor:
    def __init__(self):
        cpu_count = get_cpu_count()
        interval = 1

    def get_cpu_used(self):
        used = psutil.cpu_percent(self.interval, True)
        return {'average': sum(used) / self.cpu_count, 'per': used}

    @staticmethod
    def get_memory_used():
        vm = psutil.virtual_memory()
        sm = psutil.swap_memory()
        return {'virtual': {'used': vm.used, 'free': vm.free, 'pct': vm.percent},
                'swap':  {'used': sm.used, 'free': sm.free, 'pct': sm.percent}}

    @staticmethod
    def get_disk_used(all=False):
        if all:
            return [{i.device:psutil.disk_usage(i.device)} for i in psutil.disk_partitions(True)]
        else:
            return psutil.disk_usage("/")._asdict()

        list(psutil.disk_usage("/")._asdict())
        list(psutil.disk_usage("/"))
        psutil.disk_usage("/")._asdict()["total"]

        {tuple_[0]: tuple_[1] for tuple_ in psutil.disk_usage("/")._asdict()}

    @staticmethod
    def usage_to_dic(usage):
        ordered_dict = usage._asdict()
        return {key: ordered_dict[key] for key in list(ordered_dict)}

    usage_to_dic(psutil.disk_usage("/"))