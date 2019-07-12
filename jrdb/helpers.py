import os
import re
from typing import Union

import pandas as pd
from django.utils.module_loading import import_string

from .templates.template import Template


def startswith(
    f: Union[pd.Series, pd.DataFrame], prefix: str, rename: bool = False
) -> Union[pd.Series, pd.DataFrame]:
    f = f.copy()
    axis = "columns" if isinstance(f, pd.DataFrame) else "index"
    names = [name for name in getattr(f, axis) if name.startswith(prefix)]
    f = f[names]
    if rename:
        f = f.rename(
            **{
                axis: lambda name: name[len(prefix) :]
                if name.startswith(prefix)
                else name
            }
        )
    f.prefix = prefix
    return f


def template_factory(path: str) -> Template:
    name = extract_template_name(path)
    module_path = ".".join(["jrdb", "templates", name])
    return import_string(module_path)(path)


def extract_template_name(path):
    basename = os.path.basename(path)
    filename, _ = os.path.splitext(basename)
    name = re.search("[A-Z]+", filename).group()
    return name
