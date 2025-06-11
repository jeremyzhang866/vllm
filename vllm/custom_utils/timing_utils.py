# coding: utf-8
import time
import functools
import inspect
from custom_logging import init_logger

logger = init_logger(__name__)

def format_time(elapsed_us):
    """辅助函数：将微秒转换为毫秒+微秒格式"""
    ms = int(elapsed_us // 1000)
    us = int(elapsed_us % 1000)
    return f"{ms}ms, {us:03d}us"

def log_execution_time(theme=""):
    """
    通用装饰器：在函数执行前后分别打印日志并计算耗时。
    支持同步和异步函数。
    """
    def decorator(func):
        is_coroutine = inspect.iscoroutinefunction(func)

        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs):
            cls = getattr(args[0], "__class__", None)
            name = f"{cls.__name__}.{func.__name__}" if cls else func.__name__
            logger.info("[%s] %s 开始执行", theme, name)
            start = time.perf_counter()
            result = await func(*args, **kwargs)
            elapsed = (time.perf_counter() - start) * 1_000_000  # us
            logger.info(
                "[%s] %s 执行结束，耗时: %s",
                theme, name, format_time(elapsed)
            )
            return result

        @functools.wraps(func)
        def sync_wrapper(*args, **kwargs):
            cls = getattr(args[0], "__class__", None)
            name = f"{cls.__name__}.{func.__name__}" if cls else func.__name__
            logger.info("[%s] %s 开始执行", theme, name)
            start = time.perf_counter()
            result = func(*args, **kwargs)
            elapsed = (time.perf_counter() - start) * 1_000_000  # us
            logger.info(
                "[%s] %s 执行结束，耗时: %s",
                theme, name, format_time(elapsed)
            )
            return result

        return async_wrapper if is_coroutine else sync_wrapper

    return decorator

class Timer:
    """
    支持 with Timer(...) 作为上下文管理器使用，
    在 __enter__ 和 __exit__ 中打印开始/结束日志及耗时。
    """
    def __init__(self, label="代码块", theme=""):
        self.label = label
        self.theme = theme
        self._start = None

    def __enter__(self):
        logger.info("[%s] %s 开始执行", self.theme or "Timer", self.label)
        self._start = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        elapsed = (time.perf_counter() - self._start) * 1_000_000  # us
        logger.info(
            "[%s] %s 执行结束，耗时: %s",
            self.theme or "Timer", self.label, format_time(elapsed)
        )
        return False  # 不屏蔽异常

class AsyncTimer:
    """
    支持 async with AsyncTimer(...) 作为异步上下文管理器使用，
    在 __aenter__ 和 __aexit__ 中打印开始/结束日志及耗时。
    """
    def __init__(self, label="代码块", theme=""):
        self.label = label
        self.theme = theme
        self._start = None

    async def __aenter__(self):
        logger.info("[%s] %s 开始执行", self.theme or "AsyncTimer", self.label)
        self._start = time.perf_counter()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        elapsed = (time.perf_counter() - self._start) * 1_000_000  # us
        logger.info(
            "[%s] %s 执行结束，耗时: %s",
            self.theme or "AsyncTimer", self.label, format_time(elapsed)
        )
        return False  # 不屏蔽异常


# class MyService:
#     @log_execution_time(theme="MyService")
#     def compute(self, n):
#         # 模拟耗时操作
#         total = 0
#         for i in range(n):
#             total += i * i
#         return total
#
# svc = MyService()
# result = svc.compute(1000000)
#
#
#
# def process_data(data):
#     with Timer(label="数据处理", theme="BatchJob"):
#         # 模拟数据处理
#         processed = [d**2 for d in data]
#     return processed
#
# process_data(range(100000))
#
#
# import asyncio
#
# async def async_task():
#     async with AsyncTimer(label="异步任务", theme="AsyncJob"):
#         await asyncio.sleep(0.8)
#     print("任务完成")
#
# asyncio.run(async_task())
#
#
#
# class AsyncWorker:
#     @log_execution_time(theme="AsyncWorker")
#     async def fetch_data(self, url):
#         # 模拟异步 IO
#         await asyncio.sleep(1.2)
#         return {"data": "ok"}
#
# async def main():
#     worker = AsyncWorker()
#     res = await worker.fetch_data("http://example.com")
#     print(res)
#
# asyncio.run(main())