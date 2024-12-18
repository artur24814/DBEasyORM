import ast
import os
import importlib.util
from typing import List, Tuple


class SubclassFinder(ast.NodeVisitor):
    def __init__(self, base_class_name):
        self.base_class_name = base_class_name
        self.subclasses = []

    def visit_ClassDef(self, node):
        if self._is_subclass_of_model(node):
            self.subclasses.append(node.name)
        self.generic_visit(node)

    def _is_subclass_of_model(self, node):
        for base in node.bases:
            if isinstance(base, ast.Name) and base.id == self.base_class_name:
                return True
        return False


class ModelClassesLoader:
    MODEL_BASE_CLASS_NAME = 'Model'

    def load_models(self, loockup_folder: str) -> List[object]:
        classInstances = list()
        detected_subclasses = self._get_detected_subclasses(loockup_folder, self.MODEL_BASE_CLASS_NAME)

        for file_path, class_name in detected_subclasses:
            class_module = self._import_file_as_module(file_path, class_name)
            classInstance = getattr(class_module, class_name, None)()
            classInstances.append(classInstance)
        return classInstances

    def _get_detected_subclasses(self, folder_path: str, base_class_name: str) -> List[Tuple[str, str]]:
        subclasses = []
        for root, _, files in os.walk(folder_path):
            for file in files:
                if file.endswith(".py"):
                    file_path = os.path.join(root, file)
                    subclasses_in_file = self._find_model_subclasses_in_file(file_path, base_class_name)
                    subclasses.extend((file_path, cls) for cls in subclasses_in_file)
        return subclasses

    def _find_model_subclasses_in_file(self, file_path: str, base_class_name: str) -> List[str]:
        with open(file_path, "r", encoding="utf-8") as file:
            tree = ast.parse(file.read(), filename=file_path)
        finder = SubclassFinder(base_class_name)
        finder.visit(tree)
        return finder.subclasses

    def _import_file_as_module(self, file_path: str, module_name: str) -> object:
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
