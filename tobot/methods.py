# This file is placed in the Public Domain.


"methods"


from tob.objects import Object, items


class Default(Object):

    def __getattr__(self, key):
        return self.__dict__.get(key, "")



def edit(obj, setter, skip=True):
    for key, val in items(setter):
        if skip and val == "":
            continue
        try:
            setattr(obj, key, int(val))
            continue
        except ValueError:
            pass
        try:
            setattr(obj, key, float(val))
            continue
        except ValueError:
            pass
        if val in ["True", "true"]:
            setattr(obj, key, True)
        elif val in ["False", "false"]:
            setattr(obj, key, False)
        else:
            setattr(obj, key, val)


def fmt(obj, args=[], skip=[], plain=False, empty=False):
    if not args:
        args = obj.__dict__.keys()
    txt = ""
    for key in args:
        if key.startswith("__"):
            continue
        if key in skip:
            continue
        value = getattr(obj, key, None)
        if value is None:
            continue
        if not empty and not value:
            continue
        if plain:
            txt += f"{value} "
        elif isinstance(value, str):
            txt += f'{key}="{value}" '
        elif isinstance(value, (int, float, dict, bool, list)):
            txt += f"{key}={value} "
        else:
            txt += f"{key}={name(value, True)} "
    return txt.strip()


def parse(obj, txt):
    data = {
        "args": [],
        "cmd": "",
        "gets": Default(),
        "index": None,
        "init": "",
        "opts": "",
        "otxt": txt,
        "rest": "",
        "silent": Default(),
        "sets": Default(),
        "txt": ""
    }
    for k, v in data.items():
        setattr(obj, k, getattr(obj, k, v))
    args = []
    nr = -1
    for spli in txt.split():
        if spli.startswith("-"):
            try:
                obj.index = int(spli[1:])
            except ValueError:
                obj.opts += spli[1:]
            continue
        if "-=" in spli:
            key, value = spli.split("-=", maxsplit=1)
            setattr(obj.silent, key, value)
            setattr(obj.gets, key, value)
            continue
        if "==" in spli:
            key, value = spli.split("==", maxsplit=1)
            setattr(obj.gets, key, value)
            continue
        if "=" in spli:
            key, value = spli.split("=", maxsplit=1)
            setattr(obj.sets, key, value)
            continue
        nr += 1
        if nr == 0:
            obj.cmd = spli
            continue
        args.append(spli)
    if args:
        obj.args = args
        obj.txt  = obj.cmd or ""
        obj.rest = " ".join(obj.args)
        obj.txt  = obj.cmd + " " + obj.rest
    else:
        obj.txt = obj.cmd or ""


def __dir__():
    return (
        'edit',
        'fmt',
        'name',
        'parse'
   )
