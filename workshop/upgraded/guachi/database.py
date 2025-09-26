import sqlite3

BASE = """CREATE TABLE IF NOT EXISTS _guachi_data (key TEXT PRIMARY KEY, value TEXT)"""
OPT_MAP = """CREATE TABLE IF NOT EXISTS _guachi_options (key TEXT PRIMARY KEY, value TEXT)"""
DEF_MAP = """CREATE TABLE IF NOT EXISTS _guachi_defaults (key TEXT PRIMARY KEY, value TEXT)"""

class dbdict(dict):
    def __init__(self, path, table='_guachi_data'):
        super().__init__()
        self.table = table
        self.db_filename = path
        self.con = sqlite3.connect(self.db_filename)
        self.con.execute(BASE)
        self.con.execute(OPT_MAP)
        self.con.execute(DEF_MAP)
        self.select_value = f"SELECT value FROM {self.table} WHERE key=?"
        self.select_key = f"SELECT key FROM {self.table} WHERE key=?"
        self.update_value = f"UPDATE {self.table} SET value=? WHERE key=?"
        self.insert_key_value = f"INSERT INTO {self.table} (key,value) VALUES (?,?)"
        self.delete_key = f"DELETE FROM {self.table} WHERE key=?"
        self.select_keys = f"SELECT key from {self.table}"
        self.select_all = f"SELECT * from {self.table}"

    def __getitem__(self, key):
        row = self.con.execute(self.select_value, (key,)).fetchone()
        if not row:
            raise KeyError(f"key '{key}' not found in persistent dictionary")
        return self._restore_type(row[0])

    def __setitem__(self, key, item):
        if isinstance(item, dict):
            raise sqlite3.InterfaceError("Cannot store dict type in dbdict value.")
        item_str = str(item)
        try:
            if self.con.execute(self.select_key, (key,)).fetchone():
                self.con.execute(self.update_value, (item_str, key))
            else:
                self.con.execute(self.insert_key_value, (key, item_str))
        except sqlite3.InterfaceError as e:
            raise sqlite3.InterfaceError(e)
        self.con.commit()
        return super().__setitem__(key, item)

    def __delitem__(self, key):
        if self.con.execute(self.select_key, (key,)).fetchone():
            self.con.execute(self.delete_key, (key,))
            self.con.commit()
        else:
            raise KeyError(f"key '{key}' not found in persistent dictionary")

    def get(self, key, default=None):
        row = self.con.execute(self.select_value, (key,)).fetchone()
        if not row:
            return default
        return self._restore_type(row[0])

    def keys(self):
        return [row[0] for row in self.con.execute(self.select_keys).fetchall()]

    def items(self):
        return [(k, self._restore_type(v)) for k, v in self.con.execute(self.select_all).fetchall()]

    def get_all(self):
        dict_all = {}
        for key, value in self.con.execute(self.select_all):
            dict_all[key] = self._restore_type(value)
        return dict_all

    def _integrity_check(self):
        try:
            integrity = self.con.execute("pragma integrity_check").fetchone()
            if integrity == ('ok',):
                return True
        except Exception as error:
            return error

    def _close(self):
        self.con.close()

    def _restore_type(self, value):
        # int, float, bool 등으로 복원
        if value is None:
            return value
        if value.isdigit():
            return int(value)
        try:
            return float(value)
        except ValueError:
            pass
        if value.lower() in ('true', 'false'):
            return value.lower() == 'true'
        return value
