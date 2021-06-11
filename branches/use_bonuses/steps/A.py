from phase_pattern import *
from copy       import deepcopy

first = Phase()


def on_return(menu=None, user=None, message=None):
    key = message.content
    keys = [k['key'] for k in user.basket]
    if key in keys:
        i = keys.index(key)
        user.basket = user.basket[:i] + user.basket[i+1:] + user.basket[i]
    else:
        user.basket.append(deepcopy(menu.products[key]))
        # user.basket[-1]['amount']
        # user.basket[-1]['price']
    return user, 'NEXT', None

def on_call(menu=None, user=None, message=None):
    menu.database.to_log(user, message,'use_bonus')
    user_id = user.id
    total_price = [i['price'] for i in user.basket]*user.discount
    keys = products.keys()
    values = [products[key]['title'] for key in keys]

    callbacks = [key for key in keys]

    markup = first.get_buttons(values, callbacks, cols=2, bb=False, refb=True)
    MSG = 'Привет, я - чат-бот, ведущий прямой репортаж с морского дна!\nС помощью меня можно заказать морепродукты на дом прямиком с Дальнего Востока!\n(оформляя заказ через чат-бота, вы соглашаетесь на получение новостей о свежих поступлениях морепродуктов)\n\nСмотри что у нас есть:'
    menu.bot.send_message(user_id, MSG, reply_markup=markup)


def check_access(menu, user,message):
    if (message.type == 'callback') and (message.content in menu.products):
        return True
    else:
        return False

def on_undo(menu=None,user=None,message=None):
    user.basket = user.basket[:-1]
    return user


setattr(first, 'on_call', on_call)
setattr(first, 'check_access', check_access)
setattr(first, 'on_return',on_return)
setattr(first, 'on_undo', on_undo)
# del on_call, on_return, check_access
