import asyncio, asyncssh, sys

async def run_client() -> None:
    async with asyncssh.connect('10.48.205.118', username='guest', port=8022, known_hosts=None) as conn:
        async with conn.create_process('bc') as process:
            while True:
                buff = input()
                process.stdin.write(buff + '\n')
                print("Message sent!")

try:
    asyncio.get_event_loop().run_until_complete(run_client())
except (OSError, asyncssh.Error) as exc:
    sys.exit('SSH connection failed: ' + str(exc))
