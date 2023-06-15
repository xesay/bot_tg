anonymous_filter = lambda x: True if x.lower().count('я') >= 23 else False



print(anonymous_filter('ЯЯЯЯЯяяяяяяяяяяяяяяяяяяяяяя'))