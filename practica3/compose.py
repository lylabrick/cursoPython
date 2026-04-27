from __future__ import annotations

from typing import Callable, TypeVar, Any

T = TypeVar("T")

def compose(*fns: Callable[..., Any]) -> Callable[..., Any]:
    """
    compose(f, g, h)(x) == f(g(h(x))).
    Si no se pasan funciones, retorna identidad.
    """
    if not fns:
        return lambda x: x
    
    def composed(*args: Any, **kwargs: Any) -> Any:
        # la última función puede aceptar *args/**kwargs
        result = fns[-1](*args, **kwargs)
        # las demás se aplican sobre un solo valor
        for fn in reversed(fns[:-1]):
            result = fn(result)
        return result
    return composed