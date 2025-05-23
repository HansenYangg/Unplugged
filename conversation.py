import os
from pathlib import Path

class ConversationHandler:
    _instance = None
    _initialized = False

    # make sure only one instance of this class 

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self, max_window_size = 6, auto_save = True, save_path = None):
        if not self._initialized:
            self.max_window_size = max_window_size
            self.history = [] # could use deque instead, but since conversation history length is capped at 14, would be a negligible difference. can change if we want longer histories though
            self.total_messages = 0
            self.curr_window_size = 0
            self.auto_save = auto_save
            if save_path is None:
                self.save_path = str(Path(__file__).parent / "s_p" / "save_path.txt")
            else:
                self.save_path = save_path

            os.makedirs(os.path.dirname(self.save_path), exist_ok=True)
            self.load_history()
            self._initialized = True
            
    

    def add_message(self, msg, role): # could maybe optimize by storing conversation in reverse order (then traversing in reverse order to maintain correct order), so can pop in O(1) vs O(N), but conversation history is only 6 messages so very short
        msg = msg.replace('\n', ' ').strip()
        
        if self.curr_window_size < self.max_window_size:
            self.history.append(f"{role}: {msg}")
        else:
            self.history = self.history[1:]
            self.history.append(f"{role}: {msg}")

        self.total_messages += 1
        self.curr_window_size += 1

        if self.auto_save:
            self.save_history()


    def clear_history(self) -> None:
        self.history = []
        self.total_messages = 0
        self.curr_window_size = 0
        
        try:
            if os.path.exists(self.save_path):
                os.remove(self.save_path)
            
            backup_path = f"{self.save_path}.backup"
            if os.path.exists(backup_path):
                os.remove(backup_path)
                
        except Exception as e:
            self.logger.error(f"Failed to remove save files: {str(e)}")
    


    def get_conversation_history(self):
        if not self.history:
            return None
        
        return '\n'.join(self.history)
    
    
    def save_history(self):
        try:
            if os.path.exists(self.save_path):
                backup_path = f"{self.save_path}.backup"
                try:
                    os.replace(self.save_path, backup_path)
                except Exception as e:
                    print(f"Failed to create backup: {str(e)}")
            
            with open(self.save_path, 'w', encoding='utf-8') as f:
                for message in self.history:
                    f.write(f"{message}\n")
                    
            return True
            
        except Exception as e:
            print(f"Failed to save conversation history: {str(e)}")
            return False
        


    def load_history(self):
        try:
            if os.path.exists(self.save_path):
                with open(self.save_path, 'r', encoding='utf-8') as f:
                    self.history = [line.strip() for line in f if line.strip()]
                    self.total_messages = len(self.history)
                    self.curr_window_size = len(self.history)
                return True
            
            return False
            
        except Exception as e:
            print(f"Failed to load conversation history: {str(e)}")
            return False
        
    def change_autosave(self, changed):
        self.auto_save = changed

    # for quality of life / debugging 

    def get_curr_window_size(self):
        return self.curr_window_size

    def get_messages(self):
        return self.history
    
    def history_exists(self):
        return len(self.history) > 0

    

