from __future__ import annotations

from typing import Callable, Iterable, Iterator, TypeVar, Optional, Any

T = TypeVar("T")
U = TypeVar("U")

def my_map(func: Callable[..., U], *iterables: Iterable[Any]) -> Iterator[U]:
    """
    Implementa map(func, *iterables) desde cero.
    - Para cuando el iterable más corto se agota (igual que map).
    - Devuelve un iterador.
    """
    if func is None:
        raise TypeError("my_map() does not support")
    
    iters = [iter(it) for it in iterables]
    while True:
        args = []
        for it in iters:
            try:
                args.append(next(it))
            except StopIteration:
                return
        yield func(*args)
        

def my_filter(func: Optional[Callable[[T], bool]], iterable: Iterable[T]) -> Iterator[T]:
    """
    Implementa filter(func, iterable) desde cero.
    - Si func es None, filtra por truthiness (igual que filter).
    - Devuelve un iterador.
    """
    if func is None:
        for x in iterable:
            if x:
                yield x
    else:
        for x in iterable:
            if func(x):
                yield x
                
                
                
_sentinel = object()


def my_reduce(func: Callable[[U, T], U], iterable: Iterable[T], initial: Any = _sentinel) -> U:
    """
    Implementa reduce(func, iterable[, initial]) desde cero (sin functools).
    - Si no hay initial y el iterable está vacío => TypeError (igual que reduce).
    """
    it = iter(iterable)
    if initial is _sentinel:
        try:
            acc = next(it)  # type: ignore[assignment]
        except StopIteration:
            raise TypeError("my_reduce() of empty sequence with no initial value")
    else:
        acc = initial  # type: ignore[assignment]
    for x in it:
        acc = func(acc, x)
    return acc  # type: ignore[return-value]