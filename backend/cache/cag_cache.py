from typing import Dict, Any, List, Optional
import threading
import time


class CAGCache:
    def __init__(self, ttl: int = 3600):
        self.ttl = ttl
        self._cache: Dict[str, Dict[str, Any]] = {}
        self._lock = threading.Lock()
        self._hits = 0
        self._misses = 0

    def _is_valid(self, entry: Dict[str, Any]) -> bool:
        return time.time() - entry["timestamp"] < self.ttl

    def get(self, key: str) -> Optional[Any]:
        with self._lock:
            entry = self._cache.get(key)
            if entry and self._is_valid(entry):
                self._hits += 1
                return entry["value"]
            self._misses += 1
            return None

    def set(self, key: str, value: Any) -> None:
        with self._lock:
            self._cache[key] = {
                "value": value,
                "timestamp": time.time()
            }

    def get_retrieval(self, key: str) -> Optional[List]:
        return self.get(f"retrieval:{key}")

    def set_retrieval(self, key: str, value: List) -> None:
        self.set(f"retrieval:{key}", value)

    def get_answer(self, key: str) -> Optional[str]:
        return self.get(f"answer:{key}")

    def set_answer(self, key: str, value: str) -> None:
        self.set(f"answer:{key}", value)

    def invalidate_document(self, document_id: int) -> int:
        with self._lock:
            keys_to_remove = []
            for key in self._cache.keys():
                if str(document_id) in key:
                    keys_to_remove.append(key)
            for key in keys_to_remove:
                del self._cache[key]
            return len(keys_to_remove)

    def flush(self) -> int:
        with self._lock:
            count = len(self._cache)
            self._cache.clear()
            return count

    def get_stats(self) -> Dict[str, Any]:
        total = self._hits + self._misses
        hit_rate = self._hits / total if total > 0 else 0.0
        return {
            "total_entries": len(self._cache),
            "hit_rate": hit_rate,
            "total_hits": self._hits,
            "total_misses": self._misses,
            "memory_usage_mb": 0.0
        }


cag_cache = CAGCache()
