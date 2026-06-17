import functools
import traceback

def standardize_output(func):
    @functools.wraps(func)
    async def wrapper(target: str, context: dict, *args, **kwargs):
        try:
            # Check for external dependencies heuristically if defined in context or module
            result = await func(target, context, *args, **kwargs)
            
            # Standardization
            if isinstance(result, dict) and "success" in result:
                return result
                
            return {
                "success": True,
                "plugin": getattr(func, "__module__", "unknown"),
                "target": target,
                "data": result,
                "errors": []
            }
        except Exception as e:
            return {
                "success": False,
                "plugin": getattr(func, "__module__", "unknown"),
                "target": target,
                "category": "Utility",
                "data": {},
                "errors": [str(e), traceback.format_exc()]
            }
    return wrapper
