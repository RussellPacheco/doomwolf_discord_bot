import os, json
from config import config

class PseudoDB:
  def __init__(self): 
    if not os.path.exists(config.db_file_path):
      self._create_db_file()
    with open(config.db_file_path, 'r') as db_file:
      self._db = json.load(db_file)

  def _create_db_file(self):
    with open(config.db_file_path, 'w') as db_file:
      json.dump({
        'challenges': {
          'current': {},
          'past': []
        },
        'admins': [
          {
            'id': 636913307605008407,
            'name': 'BobSanders',
          }
        ],
        'channels': {
          'main': config.main_channel,
        }
      }, db_file, indent=2)
  
  def _save_db(self):
    json.dump(self._db, open(config.db_file_path, 'w'), indent=2)
  
  def add_admin(self, admin_id, admin_name):
    self._db['admins'].append({
      'id': admin_id,
      'name': admin_name,
    })
    self._save_db()
  
  def get_admins(self):
    return self._db['admins']
  
  def add_challenge(self, challenge):
    if self._db['challenges']['current'] != {}:
      self._db['challenges']['past'].append(self._db['challenges']['current'])
    self._db['challenges']['current'] = challenge
    self._save_db()

  def end_challenge(self):
    self._db['challenges']['past'].append(self._db['challenges']['current'])
    self._db['challenges']['current'] = {}
    self._save_db()

  def get_current_challenge(self):
    return self._db['challenges']['current']
  
  def get_past_challenges(self):
    return self._db['challenges']['past']
  

db = PseudoDB()


    
