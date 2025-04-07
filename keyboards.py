from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_brand_kb(page):
    btn_stockx = InlineKeyboardButton(text='StockX', callback_data='brand_stockx')
    btn_sephora = InlineKeyboardButton(text='Sephora', callback_data='brand_sephora')
    btn_nordstrom = InlineKeyboardButton(text='Nordstrom', callback_data='brand_nordstrom')
    btn_grailed = InlineKeyboardButton(text='Grailed', callback_data='brand_grailed')
    btn_amazon = InlineKeyboardButton(text='Amazon', callback_data='brand_amazon')
    btn_ebay = InlineKeyboardButton(text='Ebay', callback_data='brand_ebay')
    btn_lv = InlineKeyboardButton(text='LV', callback_data='brand_lv')
    btn_dior = InlineKeyboardButton(text='Dior', callback_data='brand_dior')
    btn_end = InlineKeyboardButton(text='End', callback_data='brand_end')
    btn_goat_v1 = InlineKeyboardButton(text='Goat V1', callback_data='brand_goat_v1')
    btn_goat_v2 = InlineKeyboardButton(text='Goat V2', callback_data='brand_goat_v2')
    btn_nike = InlineKeyboardButton(text='Nike', callback_data='brand_nike')
    btn_adidas = InlineKeyboardButton(text='Adidas', callback_data='brand_adidas')
    btn_gucci = InlineKeyboardButton(text='Gucci', callback_data='brand_gucci')
    btn_stussy = InlineKeyboardButton(text='Stussy', callback_data='brand_stussy')

    btn_continue = InlineKeyboardButton(text='Далее', callback_data='from_brand_continue')

    # Navigation buttons
    btn_to_1st_page = InlineKeyboardButton(text='1 страница', callback_data='page_1')
    btn_to_2nd_page = InlineKeyboardButton(text='2 страница', callback_data='page_2')
    btn_to_3rd_page = InlineKeyboardButton(text='3 страница', callback_data='page_3')

    match page:
        case 1:
            kb = InlineKeyboardMarkup(inline_keyboard=[
                [btn_stockx, btn_sephora],
                [btn_nordstrom, btn_grailed],
                [btn_amazon, btn_ebay],
                [btn_to_1st_page, btn_to_2nd_page, btn_to_3rd_page],
                [btn_continue]
            ])
        case 2:
            kb = InlineKeyboardMarkup(inline_keyboard=[
                [btn_lv, btn_dior],
                [btn_end, btn_goat_v1],
                [btn_goat_v2, btn_nike],
                [btn_to_1st_page, btn_to_2nd_page, btn_to_3rd_page],
                [btn_continue]
            ])
        case 3:
            kb = InlineKeyboardMarkup(inline_keyboard=[
                [btn_adidas],
                [btn_gucci],
                [btn_stussy],
                [btn_to_1st_page, btn_to_2nd_page, btn_to_3rd_page],
                [btn_continue]
            ])
        case _:
            kb = InlineKeyboardMarkup(inline_keyboard=[
                [btn_to_1st_page, btn_to_2nd_page, btn_to_3rd_page],
                [btn_continue]
            ])

    return kb
