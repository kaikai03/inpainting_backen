# coding: utf-8

import psutil
import time
import pynvml

class Monitor:
    """ 速度单位为 bytes/s"""
    def __init__(self, interval=1):
        self.cpu_count = Monitor.get_cpu_count()
        self.interval = interval

    @staticmethod
    def get_cpu_count():
        return psutil.cpu_count()

    def get_cpu_used(self):
        used = psutil.cpu_percent(self.interval, True)
        return {'average': sum(used) / self.cpu_count, 'per': used}

    @staticmethod
    def get_memory_used():
        vm = psutil.virtual_memory()
        sm = psutil.swap_memory()
        return {'virtual': Monitor.usage_to_dic(vm),
                'swap':  Monitor.usage_to_dic(sm)}

    @staticmethod
    def usage_to_dic(usage):
        ordered_dict = usage._asdict()
        return {key: ordered_dict[key] for key in list(ordered_dict)}

    @staticmethod
    def get_disk_used(device_all=False):
        # false 只监控项目盘
        if device_all:
            return [{i.device: Monitor.usage_to_dic(psutil.disk_usage(i.device))} for i in psutil.disk_partitions(True)]
        else:
            return Monitor.usage_to_dic(psutil.disk_usage("/"))

    def get_disk_io(self, device_all=False):
        # device_all 为 false 时，返回最大的读写速度
        def get_io():
            infos = psutil.disk_io_counters(1).items()
            return [(item[0], item[1].read_bytes, item[1].write_bytes) for item in infos]
        start = get_io()
        time.sleep(self.interval)
        end = get_io()
        results = [{'device_name': item[0], 'read_speed': (item[1]-start[index][1])/self.interval,
                  'write_speed': (item[2]-start[index][2])/self.interval} for index, item in enumerate(end)]
        if device_all:
            return results
        else:
            speed_max, index_max = 0,0
            for index,item in enumerate(results):
                speed = item['read_speed']+item['write_speed']
                if speed > speed_max:
                    index_max = index
            results_filted = results[index_max]
            del results_filted['device_name']
            return results_filted

    def get_net_io(self):
        def get_io():
            infos = psutil.net_io_counters()
            return infos.bytes_sent, infos.bytes_recv
        start = get_io()
        time.sleep(self.interval)
        end = get_io()
        return {'sent_speed': (end[0]-start[0])/self.interval,
                'recv_speed': (end[1]-start[1])/self.interval}

    @staticmethod
    def get_gpu_info():
        try:
            pynvml.nvmlInit()
            handle = pynvml.nvmlDeviceGetHandleByIndex(0)  # 这里的0是GPU id
            meminfo = pynvml.nvmlDeviceGetMemoryInfo(handle)
            print(meminfo.total)  # 第二块显卡总的显存大小
            print(meminfo.used)  # 这里是字节bytes，所以要想得到以兆M为单位就需要除以1024**2
            print(meminfo.free)  # 第二块显卡剩余显存大小
            print(pynvml.nvmlDeviceGetCount())  # 显示有几块GPU
        except Exception as e:
            print(e)

    def get_report(self):
        return {'cpu': self.get_cpu_used(),
                'memory': self.get_memory_used(),
                'disk_used': self.get_disk_used(device_all=False),
                'disk_io': self.get_disk_io(device_all=False),
                'net_io': self.get_net_io(),
                }


Monitor().get_report()