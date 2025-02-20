import io

import msgpack
import numpy as np


def serialize_numpy(numpy_arr: np.ndarray) -> bytes:
    """
    Сериализация одного numpy массива в bytes. Используется .npy формат функции np.save
    """

    assert isinstance(numpy_arr, np.ndarray)
    with io.BytesIO() as in_memory_fd:
        np.save(in_memory_fd, numpy_arr, allow_pickle=False)
        in_memory_fd.seek(0)
        return in_memory_fd.read()


def deserialize_numpy(data: bytes) -> np.ndarray:
    """
    Десериализация bytes в numpy.  Используется .npy формат для функции np.load
    """

    assert isinstance(data, bytes)
    in_memory_fd = io.BytesIO(data)
    return np.load(in_memory_fd, allow_pickle=False)


def default(obj):
    """ Функция сериализации расширенного типа для msgpack"""

    if isinstance(obj, np.ndarray):
        serialized_numpy = serialize_numpy(obj)
        # 42 – произвольный идентификатор расширенного типа (значение от -128 до 127)
        return msgpack.ExtType(0, serialized_numpy)
    raise TypeError("Неизвестный тип: %r" % (obj,))


def ext_hook(code: int, data):
    """Функция для десериализации расширенного типа для msgpack"""

    if code == 0:
        return deserialize_numpy(data)
    return msgpack.ExtType(code, data)


if __name__ == '__main__':
    # Пример использования:
    my_obj = np.arange(9).reshape((3, 3))
    # Упаковываем с передачей функции default
    packed = msgpack.packb(my_obj, default=default)
    # Распаковываем с передачей ext_hook
    unpacked = msgpack.unpackb(packed, ext_hook=ext_hook)

    print("Упакованные данные:", packed)
    print("Распакованный объект:", unpacked)
    print("Данные объекта:", unpacked.data)
