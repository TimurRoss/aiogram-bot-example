class Sdict:
    def __init__(self, d: dict):
        super().__init__()
        self.d = d

    def __getattr__(self, item: str):
        value = self.d.get(item)
        if isinstance(value, dict):
            return self.__class__(value)

        return value
    def __getitem__(self, item):
        return self.d[item]
    def __repr__(self):
        return repr(self.d)
    def get(self,item):
        return self.d.get(item)
    def keys(self):
        return self.d.keys()
    def values(self):
        return self.d.values()
    def items(self):
        return self.d.items()
    def get_dict(self):
        return self.d
    def clear(self):
        self.d.clear()
    def copy(self):
        return self.__class__(self.d.copy())
    def update(self,dict2):
        self.d.update(dict2)
    def update(self,**keys):
        self.d.update(keys)


# Example
# genMessage = {
#     'from_user': {
#         'id': 123,
#         'username': "username",
#         'full_name': "fullName"
#     }
# }
# x = Sdict(genMessage)
# print(x.from_user, type(x.from_user))
# # {'id': 123, 'username': 'username', 'full_name': 'fullName'} <class 'core.tools.Supdict.Sdict'>
# print(x.from_user.id, type(x.from_user.id))
# # 123 <class 'int'>
# print(x.from_user.username, type(x.from_user.username))
# # username <class 'str'>
# print(x)
# # {'from_user': {'id': 123, 'username': 'username', 'full_name': 'fullName'}}