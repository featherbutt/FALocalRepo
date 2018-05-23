print('Readying program ... ', end='', flush=True)
import sqlite3
import sys, os
import PythonRead as readkeys
import FA_db as fadb
import FA_dl as fadl
import FA_tools as fatl
import FA_up as faup
import FA_var as favar

def menu(db):
    menu = (
        ('Download & Update', fadl.download_main),
        ('Search', fadb.db_search),
        ('Repair database', fadb.repair),
        ('Exit', (lambda *x: sys.exit(0)))
    )
    menu = {str(k): mk for k, mk in enumerate(menu, 1)}

    menu_l = [f'{i}) {menu[i][0]}' for i in menu]

    Session = None

    while True:
        fatl.sigint_clear()

        fatl.header('Menu')

        print('\n'.join(menu_l))
        print('\nChoose option: ', end='', flush=True)
        k = '0'
        while k not in menu:
            k = readkeys.getkey()
            k = k.replace('\x03', str(len(menu)))
            k = k.replace('\x04', str(len(menu)))
            k = k.replace('\x1b', str(len(menu)))
        print(k+'\n')

        try:
            fatl.log('MAIN MENU -> '+menu[k][0])
            Session = menu[k][1](Session, db)
        except SystemExit:
            fatl.log('PROGRAM END')
            sys.exit(0)
        except KeyboardInterrupt:
            fatl.log('PROGRAM END')
            sys.exit(130)
        except:
            err = sys.exc_info()
            fatl.log('ERROR EXIT -> '+repr(err))
            fatl.log('PROGRAM END')
            if '--debug' in sys.argv[1:]:
                raise
            else:
                print('\nAn uknown error occurred:')
                for e in err:
                    print('  '+repr(e))
                    sys.exit(1)

        print('-'*30+'\n')

fatl.log_start()
fatl.log('PROGRAM START')

fatl.sigint_block()

print('\b \b'*21, end='', flush=True)

if os.path.isfile(favar.log_file):
    print('Trimming log file ... ', end='', flush=True)
    fatl.log_trim()
    print('\b \b'*22, end='', flush=True)

if os.path.isfile(favar.db_file):
    faup.db_upgrade()

if os.path.isfile(favar.db_file):
    db = sqlite3.connect(favar.db_file)
    fatl.log('DB -> connected')
else:
    db = sqlite3.connect(favar.db_file)
    print('Creating database & tables ... ', end='', flush=True)
    fadb.mktable(db, 'submissions')
    fadb.mktable(db, 'users')
    fadb.mktable(db, 'infos')
    print('\b \b'*31, end='', flush=True)
    fatl.log('DB -> created')

menu(db)
