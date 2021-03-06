import os, time
import asyncio, asyncssh, crypt, sys
from typing import Optional

passwords = {'guest': '',                 # guest account with no password
             'user123': 'qV2iEadIGV2rw'   # password of 'secretpw'
            }

async def handle_client(process: asyncssh.SSHServerProcess) -> None:
    process.stdout.write('Enter numbers one per line, or EOF when done:\n')

    total = 0

    async for line in process.stdin:
        line = line.rstrip('\n')
        print(line)
        os.system('curl --request POST https://api.pushcut.io/QWz5_f5mzkfk6pHuIfO4y/notifications/Seizure')
        time.sleep(10)
class MySSHServer(asyncssh.SSHServer):
    def connection_made(self, conn: asyncssh.SSHServerConnection) -> None:
        print('SSH connection received from %s.' %
                  conn.get_extra_info('peername')[0])

    def connection_lost(self, exc: Optional[Exception]) -> None:
        if exc:
            print('SSH connection error: ' + str(exc), file=sys.stderr)
        else:
            print('SSH connection closed.')

    def begin_auth(self, username: str) -> bool:
        # If the user's password is the empty string, no auth is required
        return passwords.get(username) != ''

    def password_auth_supported(self) -> bool:
        return True

    def validate_password(self, username: str, password: str) -> bool:
        pw = passwords.get(username, '*')
        return crypt.crypt(password, pw) == pw

async def start_server() -> None:
    await asyncssh.create_server(MySSHServer, '', 8022,
                                 server_host_keys=['~/.ssh/id_rsa'],
                                 process_factory=handle_client)

loop = asyncio.get_event_loop()

try:
    loop.run_until_complete(start_server())
except (OSError, asyncssh.Error) as exc:
    sys.exit('Error starting server: ' + str(exc))

loop.run_forever()
