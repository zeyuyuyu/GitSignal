import asyncio
from typing import Dict, List, Callable, Any
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Signal:
    name: str
    timestamp: datetime
    data: Any

class GitSignal:
    def __init__(self):
        self._subscribers: Dict[str, List[Callable]] = {}
        self._event_loop = asyncio.get_event_loop()
        self._signal_queue = asyncio.Queue()

    async def emit(self, signal_name: str, data: Any) -> None:
        """Emit a signal to all subscribers"""
        signal = Signal(
            name=signal_name,
            timestamp=datetime.utcnow(),
            data=data
        )
        await self._signal_queue.put(signal)

    def subscribe(self, signal_name: str, callback: Callable) -> None:
        """Subscribe to a signal"""
        if signal_name not in self._subscribers:
            self._subscribers[signal_name] = []
        self._subscribers[signal_name].append(callback)

    def unsubscribe(self, signal_name: str, callback: Callable) -> None:
        """Unsubscribe from a signal"""
        if signal_name in self._subscribers:
            self._subscribers[signal_name].remove(callback)

    async def _process_signals(self) -> None:
        """Process signals from the queue"""
        while True:
            signal = await self._signal_queue.get()
            if signal.name in self._subscribers:
                for callback in self._subscribers[signal.name]:
                    try:
                        await asyncio.create_task(callback(signal))
                    except Exception as e:
                        print(f"Error processing signal {signal.name}: {e}")
            self._signal_queue.task_done()

    def start(self) -> None:
        """Start the signal processing loop"""
        self._event_loop.create_task(self._process_signals())

    def stop(self) -> None:
        """Stop the signal processing loop"""
        self._event_loop.stop()

# Example usage
async def main():
    git_signal = GitSignal()
    git_signal.start()

    async def handle_commit(signal: Signal):
        print(f"Received commit: {signal.data}")

    git_signal.subscribe('new_commit', handle_commit)
    await git_signal.emit('new_commit', {'hash': 'abc123', 'message': 'test commit'})

if __name__ == '__main__':
    asyncio.run(main())