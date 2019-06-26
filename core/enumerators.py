class AppEnum:

    ROOT_PERMISSION = 1000
    MANAGER_PERMISSION = 100
    USER_PERMISSION = 1

    @classmethod
    def available(self):
        return [a for a in dir(self) if not a.startswith('__') and not callable(getattr(self, a))]

    @classmethod
    def available_values(self):
        return [getattr(self, i) for i in self.available()]
