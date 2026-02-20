#!/usr/bin/env python3
import sys
import os
import gi
import logging

# Setup logging to /tmp/adorlipi_debug.log
logging.basicConfig(filename='/tmp/adorlipi_debug.log', level=logging.DEBUG, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

gi.require_version('IBus', '1.0')
from gi.repository import IBus, GLib

# Add project root to path
# In dev mode: platforms/linux/ -> root (2 levels up)
# In installed mode: /usr/share/adorlipi/ -> same dir (core/ is a sibling)
script_dir = os.path.dirname(os.path.abspath(__file__))
dev_root = os.path.dirname(os.path.dirname(script_dir))  # platforms/linux -> root
installed_root = script_dir  # /usr/share/adorlipi/

# Check which root has core/
if os.path.isdir(os.path.join(dev_root, 'core')):
    project_root = dev_root
elif os.path.isdir(os.path.join(installed_root, 'core')):
    project_root = installed_root
else:
    project_root = dev_root  # fallback

if project_root not in sys.path:
    sys.path.insert(0, project_root)

from core.engine.transliterator import Transliterator
logging.info(f"Successfully imported Transliterator from {project_root}")

class AdorLipiEngine(IBus.Engine):
    def __init__(self):
        super().__init__()
        self.transliterator = Transliterator()
        self.buffer = ""
        self.lookup_table = IBus.LookupTable.new(10, 0, True, True)
        logging.info("AdorLipiEngine initialized")

    def do_process_key_event(self, keyval, keycode, state):
        logging.debug(f"KeyEvent: val={keyval}, code={keycode}, state={state}")
        
        # Ignore key release events
        if state & IBus.ModifierType.RELEASE_MASK:
            return False

        # Handle Backspace
        if keyval == IBus.BackSpace:
            if self.buffer:
                self.buffer = self.buffer[:-1]
                self._update()
                return True
            return False
            
        # Handle Candidate Selection (1, 2)
        if self.buffer and self.lookup_table.get_number_of_candidates() > 0:
            if keyval == IBus.KEY_1:
                # Select Bangla (Candidate 0)
                bangla = self.transliterator.transliterate(self.buffer)
                self._commit(bangla)
                return True
            elif keyval == IBus.KEY_2:
                # Select English (Candidate 1)
                english = self.buffer
                self._commit(english)
                return True
            elif keyval == IBus.Down:
                self.lookup_table.cursor_down()
                self.update_lookup_table(self.lookup_table, True)
                return True
            elif keyval == IBus.Up:
                self.lookup_table.cursor_up()
                self.update_lookup_table(self.lookup_table, True)
                return True
        
        # Handle Enter/Return -> Commit buffer (Default Bangla)
        if keyval == IBus.Return or keyval == IBus.KP_Enter:
            if self.buffer:
                # If lookup table has cursor, commit selected
                cursor = self.lookup_table.get_cursor_pos()
                if cursor == 1:
                    self._commit(self.buffer) # English
                else:
                    self._commit() # Default Bangla
                return True
            return False
            
        # Handle Space -> Commit buffer (Default Bangla) + space
        if keyval == IBus.space:
            if self.buffer:
                bangla = self.transliterator.transliterate(self.buffer)
                self._commit(bangla + " ")
                return True
            return False

        # Handle regular characters. 
        # We check for standard modifiers (Ctrl/Alt) to ignore shortcuts.
        if state & (IBus.ModifierType.CONTROL_MASK | IBus.ModifierType.MOD1_MASK):
            return False

        # Check if printable ASCII
        if keyval < 128:
            char = chr(keyval)
            if char.isprintable():
                self.buffer += char
                self._update()
                return True
            
        return False

    def _update_lookup_table(self, candidates):
        self.lookup_table.clear()
        for i, candidate in enumerate(candidates):
            text = IBus.Text.new_from_string(candidate)
            self.lookup_table.append_candidate(text)
        self.update_lookup_table(self.lookup_table, True)

    def _update(self):
        if self.buffer:
            bangla = self.transliterator.transliterate(self.buffer)
            english = self.buffer
            
            # Dual Suggestion: 1. Bangla, 2. English
            candidates = [bangla, english]
            
            # Update Preedit (Show Bangla as default inline)
            text = IBus.Text.new_from_string(bangla)
            attrs = IBus.AttrList()
            attrs.append(IBus.Attribute.new(IBus.AttrType.UNDERLINE, IBus.AttrUnderline.SINGLE, 0, len(bangla)))
            text.set_attributes(attrs)
            self.update_preedit_text(text, len(bangla), True)
            
            # Update Lookup Table for selection
            self._update_lookup_table(candidates)
            
        else:
            self.hide_preedit_text()
            self.hide_lookup_table()

    def _commit(self, text=None):
        if text:
            # Commit specific text (from selection or space)
            logging.info(f"Committing specific: {text}")
            self.commit_text(IBus.Text.new_from_string(text))
        elif self.buffer:
            # Default commit (Bangla)
            bangla = self.transliterator.transliterate(self.buffer)
            logging.info(f"Committing default: {bangla}")
            self.commit_text(IBus.Text.new_from_string(bangla))
            
        self.buffer = ""
        self.lookup_table.clear()
        self._update()

class AdorLipiService(IBus.Service):
    def __init__(self, connection):
        try:
            super().__init__() 
            self.factory = IBus.Factory.new(connection.get_connection())
            self.factory.add_engine("adorlipi", AdorLipiEngine)
            logging.info("AdorLipiService registered (Factory created)")
        except Exception as e:
            logging.critical(f"Failed to initialize service: {e}")
            raise e

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--ibus":
        try:
            IBus.init()
            bus = IBus.Bus()
            bus.request_name("org.freedesktop.IBus.AdorLipi", 0)
            AdorLipiService(bus)
            loop = GLib.MainLoop()
            loop.run()
        except Exception as e:
            logging.critical(f"Error in main loop: {e}")
    else:
        print("Usage: ibus_engine.py --ibus")

if __name__ == "__main__":
    main()
