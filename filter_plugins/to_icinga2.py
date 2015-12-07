def to_icinga2_expression(a):
    return "\n".join([var2string(k, v) for (k, v) in a.items()])


def var2string(key, value):
    """
    generate vars.*http_vhosts*[*Default Page*] = { ... } entries if value is a dict
    vars.*os* = ... entries if value is a string
    :param key:
    :param value:
    :return:
    """
    # simple string values like var.os = "Linux"
    if type(value) is str:
        return 'vars.%s = "%s"' % (key, value)
    elif type(value) is dict:
        return "\n".join(
            ['vars.%s["%s"] = {\n%s\n}' % (key, entry, var_keys2string(values)) for entry, values in value.items()]
        )
    else:
        raise TypeError("unknown type %s, expecting type dict or str" % type(value))


def var_keys2string(values):
    """
    generates the values part of vars.xyz["myKey"] = *{ values }*
    :param values:
    :return:
    """
    return "\n".join(["    " + value2string(k, v) for k, v in values.items()])


def value2string(key, value):
    if type(value) is str:
        return '%s = "%s"' % (key, value)
    elif type(value) is int:
        return '%s = %s' % (key, value)
    elif type(value) is list:
        print(['"%s"' % str(i) for i in value])
        return "%s = [ %s ]" % (key, ", ".join(['"%s"' % str(i) for i in value]))
    else:
        raise TypeError("unknown type %s, expecting type list or str" % type(value))


class FilterModule(object):
    @staticmethod
    def filters():
        return {
            'to_icinga2': to_icinga2_expression
        }


