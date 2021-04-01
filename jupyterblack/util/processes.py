from multiprocessing import Pool
from typing import Callable, Iterable, List, TypeVar, cast

T = TypeVar("T")
S = TypeVar("S")


def keyboard_interruptable_processing_map(n_workers: int, func: Callable[[T], S], items: Iterable[T]) -> List[S]:
    process_pool = Pool(processes=n_workers)
    exited_early = False
    try:
        return process_pool.map_async(func, items).get(1)
    except KeyboardInterrupt:
        print("Caught keyboard interrupt from user")
        process_pool.terminate()
        exited_early = True
        return cast(List[S], [])
    finally:
        if not exited_early:
            process_pool.close()
        process_pool.join()
