from simple_term_menu import TerminalMenu
import pickle
import os
from helper import get_latest_run_folder


def main(proj):

    title = proj['title']

    choices = pickle.load(
        open(os.path.join(get_latest_run_folder(title), "choices.p"), "rb"))

    # Load sids
    try:
        sids = pickle.load(
            open(os.path.join(get_latest_run_folder(title), "sids.p"), "rb"))
    except (OSError, IOError) as e:
        sids = []
        pickle.dump(sids, open(os.path.join(
            get_latest_run_folder(title), "sids.p"), "wb"))

    # Load already chosen ksfs
    try:
        ksfs_done = pickle.load(
            open(os.path.join(get_latest_run_folder(title), "ksfs_done.p"), "rb"))
    except (OSError, IOError) as e:
        ksfs_done = []
        pickle.dump(ksfs_done, open(os.path.join(
            get_latest_run_folder(title), "ksfs_done.p"), "wb"))

    for i, choice in enumerate(choices):

        ksf = choice['ksf']
        res = choice['res']

        # Skip if ksf already done
        if ksf in ksfs_done:
            continue

        # Terminal
        terminal_menu = TerminalMenu(
            ['       ' + x['show'] for x in res],
            title=(str(i) + '/' + str(len(choices)) + '  ' + ksf)
        )
        menu_entry_index = terminal_menu.show()

        # Add to done
        ksfs_done.append(ksf)
        pickle.dump(ksfs_done, open(os.path.join(
            get_latest_run_folder(title), "ksfs_done.p"), "wb"))

        if menu_entry_index is not None:
            sids.append(res[menu_entry_index]['id'])
            pickle.dump(sids, open(os.path.join(
                get_latest_run_folder(title), "sids.p"), "wb"))

    return True
