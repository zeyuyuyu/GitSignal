import asyncio
import websockets
import json
import git
from pathlib import Path
from typing import Set, Dict

class GitEventServer:
    def __init__(self):
        self.clients: Set[websockets.WebSocketServerProtocol] = set()
        self.watched_repos: Dict[str, float] = {}
    
    async def register(self, websocket: websockets.WebSocketServerProtocol):
        self.clients.add(websocket)
        try:
            async for message in websocket:
                data = json.loads(message)
                if data['action'] == 'watch':
                    self.watched_repos[data['repo_path']] = 0
        except websockets.exceptions.ConnectionClosed:
            pass
        finally:
            self.clients.remove(websocket)
    
    async def broadcast_changes(self, repo_path: str, changes: dict):
        if not self.clients:
            return
        message = json.dumps({
            'repo_path': repo_path,
            'changes': changes
        })
        await asyncio.gather(
            *[client.send(message) for client in self.clients]
        )
    
    async def monitor_repos(self):
        while True:
            for repo_path in self.watched_repos:
                try:
                    repo = git.Repo(repo_path)
                    last_commit_time = repo.head.commit.committed_date
                    
                    if last_commit_time > self.watched_repos[repo_path]:
                        changes = {
                            'hash': repo.head.commit.hexsha,
                            'message': repo.head.commit.message,
                            'author': repo.head.commit.author.name,
                            'files': [item.a_path for item in repo.head.commit.diff('HEAD~1')]
                        }
                        await self.broadcast_changes(repo_path, changes)
                        self.watched_repos[repo_path] = last_commit_time
                except Exception as e:
                    print(f'Error monitoring {repo_path}: {str(e)}')
            
            await asyncio.sleep(1)

async def main():
    server = GitEventServer()
    async with websockets.serve(server.register, 'localhost', 8765):
        await server.monitor_repos()

if __name__ == '__main__':
    asyncio.run(main())
