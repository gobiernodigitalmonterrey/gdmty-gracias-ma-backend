from fastapi import Form, File, UploadFile
from pydantic import BaseModel
from typing import Type, get_type_hints, Optional, Any
import inspect

def as_form(cls: Type[BaseModel]):
    """
    Convierte un modelo de Pydantic en compatible con FastAPI para recibir datos desde un formulario HTML (multipart/form-data).
    Soporta campos de tipo str, int, y UploadFile (para archivos).
    """
    new_params = []

    type_hints = get_type_hints(cls)

    for field_name, model_field in cls.__fields__.items():
        annotation = type_hints[field_name]
        default = model_field.default if model_field.default is not None else ...

        # Usar File() si es un archivo
        if annotation is UploadFile or annotation is Optional[UploadFile]:
            form_field = File(default=default)
        else:
            form_field = Form(default=default)

        param = inspect.Parameter(
            field_name,
            inspect.Parameter.POSITIONAL_ONLY,
            default=form_field,
            annotation=annotation
        )
        new_params.append(param)

    def make_signature(params):
        return inspect.Signature(params)

    cls.__signature__ = make_signature(new_params)
    return cls
