import os
from datetime import datetime


# Nome do arquivo de backup com timestamp
backup_filename = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.sql"

# Comando de backup
backup_command = f"mysqldump -u yakiro.service.com -h server --set-gtid-purged=OFF --no-tablespaces 'database$name'  > /home/yakiro/backupSQL/{backup_filename}"

# Executar o comando de backup
os.system(backup_command)