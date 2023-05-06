from bdbaza import sqlite
from user.zapis_handlers import register_user_handlers
from user.my_spisok_handlers import register_spisok_handlers
from user.otherBTN import register_othter_handler
from adminss.admin_excel import *
from adminss.admin import *
from adminss.admin_editor import *



async def on_startup(_):
    await sqlite.db_start()
    await register_hnd()


async def register_hnd():
    register_spisok_handlers(dp)
    register_user_handlers(dp)
    register_admin_handler(dp)
    register_admin_noexcel_handler(dp)
    register_othter_handler(dp)
    register_admin_editor_handler(dp)





if __name__ == '__main__':
    executor.start_polling(dp,
                           skip_updates=True,
                           on_startup=on_startup)