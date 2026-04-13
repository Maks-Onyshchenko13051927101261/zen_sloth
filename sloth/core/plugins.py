import importlib;
import sys;
import os;
import time;
from .security import Security;


class PluginManager:
    def __init__(self, folder):
        self.folder = os.path.abspath(folder);
        self.cache = {};  # {name: (module, last_mtime)}
        os.makedirs(self.folder, exist_ok=True);

    def _get_mtime(self, name):
        path = os.path.join(self.folder, f"{name}.py")
        return os.path.getmtime(path);

    def load_plugin(self, name):
        module_name = f"plugins.{name}"

        # якщо вже завантажений
        if module_name in sys.modules:
            module = sys.modules[module_name]
            importlib.reload(module)
            return module

        return importlib.import_module(module_name)

    def run(self, name):
        try:
            # 1. Безпечний шлях до файлу
            plugin_path = Security.get_safe_path(self.folder, f"{name}.py")
            
            if not os.path.exists(plugin_path):
                return {"error": f"Plugin '{name}' not found at {plugin_path}"};

            mtime = self._get_mtime(plugin_path)
            cached = self.cache.get(name)

            # 2. Hot Reload логіка
            if not cached or cached[1] < mtime:
                module_name = f"plugins.{name}"
                
                if module_name in sys.modules:
                    module = importlib.reload(sys.modules[module_name])
                else:
                    module = importlib.import_module(module_name)
                
                self.cache[name] = (module, mtime)
            else:
                module = self.cache[name][0]

            # 3. Перевірка наявності функції run
            if hasattr(module, "run"):
                return module.run()
            else:
                return {"error": f"Plugin '{name}' has no run() function"};

        except Exception as e:
            return {"status": "error", "plugin": name, "error": str(e)}