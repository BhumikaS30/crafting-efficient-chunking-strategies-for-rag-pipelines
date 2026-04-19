import argparse
from dataclasses import dataclass
from typing import List
import time
import random

@dataclass
class Chunk:
    """Class to represent a chunk of data."""
    id: int
    size: int

class ChunkingStrategy:
    """Base class for chunking strategies."""
    def __init__(self, chunk_size: int):
        """
        Initialize the chunking strategy.

        Args:
        chunk_size (int): The size of each chunk.
        """
        self.chunk_size = chunk_size

    def chunk(self, data: List[int]) -> List[Chunk]:
        """
        Chunk the data.

        Args:
        data (List[int]): The data to be chunked.

        Returns:
        List[Chunk]: A list of chunks.
        """
        raise NotImplementedError

class StaticChunkingStrategy(ChunkingStrategy):
    """Class to represent a static chunking strategy."""
    def chunk(self, data: List[int]) -> List[Chunk]:
        """
        Chunk the data using a static chunking strategy.

        Args:
        data (List[int]): The data to be chunked.

        Returns:
        List[Chunk]: A list of chunks.
        """
        chunks = []
        for i in range(0, len(data), self.chunk_size):
            chunk = Chunk(i // self.chunk_size, min(self.chunk_size, len(data) - i))
            chunks.append(chunk)
        return chunks

class DynamicChunkingStrategy(ChunkingStrategy):
    """Class to represent a dynamic chunking strategy."""
    def __init__(self, chunk_size: int, max_chunk_size: int):
        """
        Initialize the dynamic chunking strategy.

        Args:
        chunk_size (int): The initial size of each chunk.
        max_chunk_size (int): The maximum size of each chunk.
        """
        super().__init__(chunk_size)
        self.max_chunk_size = max_chunk_size

    def chunk(self, data: List[int]) -> List[Chunk]:
        """
        Chunk the data using a dynamic chunking strategy.

        Args:
        data (List[int]): The data to be chunked.

        Returns:
        List[Chunk]: A list of chunks.
        """
        chunks = []
        current_chunk = []
        current_size = 0
        for item in data:
            if current_size + 1 > self.max_chunk_size:
                chunk = Chunk(len(chunks), self.max_chunk_size)
                chunks.append(chunk)
                current_chunk = []
                current_size = 0
            current_chunk.append(item)
            current_size += 1
        if current_chunk:
            chunk = Chunk(len(chunks), current_size)
            chunks.append(chunk)
        return chunks

class HybridChunkingStrategy(ChunkingStrategy):
    """Class to represent a hybrid chunking strategy."""
    def __init__(self, chunk_size: int, max_chunk_size: int, threshold: int):
        """
        Initialize the hybrid chunking strategy.

        Args:
        chunk_size (int): The initial size of each chunk.
        max_chunk_size (int): The maximum size of each chunk.
        threshold (int): The threshold to switch to dynamic chunking.
        """
        super().__init__(chunk_size)
        self.max_chunk_size = max_chunk_size
        self.threshold = threshold

    def chunk(self, data: List[int]) -> List[Chunk]:
        """
        Chunk the data using a hybrid chunking strategy.

        Args:
        data (List[int]): The data to be chunked.

        Returns:
        List[Chunk]: A list of chunks.
        """
        if len(data) > self.threshold:
            return DynamicChunkingStrategy(self.chunk_size, self.max_chunk_size).chunk(data)
        else:
            return StaticChunkingStrategy(self.chunk_size).chunk(data)

def simulate_rag_pipeline(chunks: List[Chunk]) -> float:
    """
    Simulate the RAG pipeline.

    Args:
    chunks (List[Chunk]): A list of chunks.

    Returns:
    float: The time taken to process the chunks.
    """
    start_time = time.time()
    for chunk in chunks:
        # Simulate processing time
        time.sleep(random.uniform(0.01, 0.1))
    end_time = time.time()
    return end_time - start_time

def main():
    parser = argparse.ArgumentParser(description="Chunking Strategies for RAG Pipelines")
    parser.add_argument("--chunk_size", type=int, default=10, help="The size of each chunk")
    parser.add_argument("--max_chunk_size", type=int, default=100, help="The maximum size of each chunk")
    parser.add_argument("--threshold", type=int, default=1000, help="The threshold to switch to dynamic chunking")
    parser.add_argument("--strategy", type=str, default="static", help="The chunking strategy to use")
    parser.add_argument("--data_size", type=int, default=10000, help="The size of the data")
    args = parser.parse_args()

    data = list(range(args.data_size))

    if args.strategy == "static":
        chunking_strategy = StaticChunkingStrategy(args.chunk_size)
    elif args.strategy == "dynamic":
        chunking_strategy = DynamicChunkingStrategy(args.chunk_size, args.max_chunk_size)
    elif args.strategy == "hybrid":
        chunking_strategy = HybridChunkingStrategy(args.chunk_size, args.max_chunk_size, args.threshold)
    else:
        raise ValueError("Invalid chunking strategy")

    chunks = chunking_strategy.chunk(data)
    time_taken = simulate_rag_pipeline(chunks)
    print(f"Time taken: {time_taken:.2f} seconds")

if __name__ == "__main__":
    main()