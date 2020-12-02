from .imported.treelib import Tree
from .imported.treelib.exceptions import NodeIDAbsentError
from typing import Optional
import shlex


class Commander:
    def __init__(self, caller="", auto_node:bool=False):
        self.caller = caller
        self.tree = Tree()
        self.events = {"on_error": None}
        self.auto_node = auto_node


        self.tree.create_node(self.caller, self.caller)

    def run(self, cmd:str):
        if cmd.find(self.caller) == 0:
            cmd = "\"" + self.caller + "\" " + cmd[len(self.caller):]
            phrases = shlex.split(cmd)

            p, a = self._split(phrases)
            return self._run(p, *a)
        return None

    # Decorator to add commands
    def __call__(self, name="", parent=""):
        def decorator(func):
            self._add_func(func, name, parent)
        return decorator

    # Drcorator to add event handlers
    def event(self):
        def decorator(func):
            if func.__name__ == "on_error":
                self.events["on_error"] = func
            else:
                raise Exception("Invalid event")
        return decorator


    def _split(self, phrases:list):
        tests = [phrases.pop(0)]
        for p in phrases:
            tests.append(tests[-1] + ":" + p)

        func_path = None
        for t in tests:
            if self.tree.get_node(t) is None:
                func_path = tests[tests.index(t)-1]
                break

        func_path = func_path or tests[-1]
        args = (tests[-1].split(func_path)[1]).split(":")[1:]

        return func_path, args

    def _run(self, func_path, *args):
        node = self.tree.get_node(func_path)
        if node is None:
            self._raise(FunctionNotFound(f"Function ({func_path}) not found, and error handler not registered"))
        else:
            func = node.data
            if func is None:
                self._raise(FunctionNotFound(f"Function ({node.identifier}) not found, and error handler not registered"))
            else:
                return func(*args)

    def _add_func(self, func, name="", parent=""):
        name = name or func.__name__
        parent = self.caller + ("" if parent == "" else ":" + parent)
        nid = parent + ":" + name
        try:
            self.tree.create_node(name, nid, parent, func)
        except Exception as e:
            if self.auto_node:
                p, n = ":".join(parent.split(":")[len(self.caller):-1]), parent.split(":")[-1]
                self._add_func(lambda *args: None, n, p)
                self.tree.create_node(name, nid, parent, func)
            else:
                raise e

    def _raise(self, error):
        if self.events["on_error"] is not None:
            self.events["on_error"](error)
        else:
            raise error


class FunctionNotFound(Exception):
    def __init__(self, msg):
        self.msg = msg


class DatabaseNotFound(Exception):
    def __init__(self, msg):
        self.msg = msg