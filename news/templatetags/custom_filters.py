from django import template

register = template.Library()

stop_list_symb = ['ч', 'а', 'п']
stop_list_str = str(stop_list_symb)


@register.filter()
def censor(value):
    # проверка на цензурирование только строк
    if not isinstance(value, str):
        raise ValueError('Нельзя применять цензора не к строке!')

    words = str.split(value)

    if words in stop_list_symb:
        value = value.replace(words, '*')

    return value
    # return value.replace('a', '*')   -- если прописывать только эту строку без тела функции,
                                            # то замена символа происходит, но это не то.

