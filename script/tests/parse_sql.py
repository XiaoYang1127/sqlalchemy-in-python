from pymysql.converters import escape_bytes_prefixed, escape_item
from pymysql.connections import DEFAULT_CHARSET


def _escape_args(args):
    if isinstance(args, (tuple, list)):
        return tuple(escape(arg) for arg in args)
    elif isinstance(args, dict):
        return dict((key, escape(val)) for (key, val) in args.items())
    else:
        # If it's not a dictionary let's try escaping it anyways.
        # Worst case it will throw a Value error
        return escape(args)


def escape(obj):
    if isinstance(obj, str):
        return "'" + escape_string(obj) + "'"

    if isinstance(obj, bytes):
        return escape_bytes_prefixed(obj)

    return escape_item(obj, DEFAULT_CHARSET)


def escape_string(s):
    return s.replace("'", "''")


print(_escape_args("yxx"))
print(_escape_args("yxx or 1#"))
