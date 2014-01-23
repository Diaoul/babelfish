from pkg_resources import resource_stream, EntryPoint  # @UnresolvedImport
from stevedore import ExtensionManager
from stevedore.extension import Extension


class ConvertersManager(ExtensionManager):
    def __init__(self, namespace):
        super(ConvertersManager, self).__init__(namespace, invoke_on_load=True,
                                         invoke_args=(), invoke_kwds={},
                                         propagate_map_exceptions=True)

    def _internal_entry_points(self):
        return []

    def _find_entry_points(self, namespace):
        entry_points = {}
        # Internal entry points
        if namespace == 'babelfish.language_converters':
            internal_entry_points_str = self._internal_entry_points()
            for internal_entry_point_str in internal_entry_points_str:
                internal_entry_point = EntryPoint.parse(internal_entry_point_str)
                entry_points[internal_entry_point.name] = internal_entry_point

        # Package entry points
        setuptools_entrypoints = super(ConvertersManager, self)._find_entry_points(namespace)
        for setuptools_entrypoint in setuptools_entrypoints:
            entry_points[setuptools_entrypoint.name] = setuptools_entrypoint

        return list(entry_points.values())

    def load_from_entry_points(self):
        for ep in self._find_entry_points('babelfish.language_converters'):
            loaded = self._load_one_plugin(ep, invoke_on_load=True, invoke_args=(), invoke_kwds={})
            if loaded:
                self.extensions.append(loaded)
        self._extensions_by_name = None

    def clear(self):
        del self.extensions[:]
        self._extensions_by_name = None

    def __setitem__(self, name, converter):
        if name in self:
            del self[name]
        self.extensions.append(Extension(name, None, None, converter))
        self._extensions_by_name = None

    def __contains__(self, name):
        try:
            self[name]
            return True
        except KeyError:
            return False

    def __delitem__(self, name):
        for e in self.extensions:
            if e.name == name:
                self.extensions.remove(e)
                break
        self._extensions_by_name = None
