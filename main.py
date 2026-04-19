import argparse
import time
from typing import List, Tuple

def static_chunking(data: List[int], chunk_size: int) -> List[List[int]]:
    """
    Divide the data into chunks of fixed size.

    Args:
    data (List[int]): The input data to be chunked.
    chunk_size (int): The size of each chunk.

    Returns:
    List[List[int]]: A list of chunks.
    """
    return [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]

def dynamic_chunking(data: List[int], max_chunk_size: int) -> List[List[int]]:
    """
    Divide the data into chunks of varying size based on a maximum chunk size.

    Args:
    data (List[int]): The input data to be chunked.
    max_chunk_size (int): The maximum size of each chunk.

    Returns:
    List[List[int]]: A list of chunks.
    """
    chunks = []
    current_chunk = []
    for item in data:
        if len(current_chunk) < max_chunk_size:
            current_chunk.append(item)
        else:
            chunks.append(current_chunk)
            current_chunk = [item]
    if current_chunk:
        chunks.append(current_chunk)
    return chunks

def hybrid_chunking(data: List[int], chunk_size: int, max_chunk_size: int) -> List[List[int]]:
    """
    Combine static and dynamic chunking strategies.

    Args:
    data (List[int]): The input data to be chunked.
    chunk_size (int): The size of each chunk for static chunking.
    max_chunk_size (int): The maximum size of each chunk for dynamic chunking.

    Returns:
    List[List[int]]: A list of chunks.
    """
    static_chunks = static_chunking(data, chunk_size)
    hybrid_chunks = []
    for chunk in static_chunks:
        dynamic_chunks = dynamic_chunking(chunk, max_chunk_size)
        hybrid_chunks.extend(dynamic_chunks)
    return hybrid_chunks

def process_chunk(chunk: List[int]) -> int:
    """
    Simulate processing a chunk.

    Args:
    chunk (List[int]): The chunk to be processed.

    Returns:
    int: The result of processing the chunk.
    """
    time.sleep(0.1)  # Simulate processing time
    return sum(chunk)

def evaluate_chunking_strategy(data: List[int], chunking_strategy: str, chunk_size: int = 10, max_chunk_size: int = 20) -> Tuple[float, float]:
    """
    Evaluate the performance of a chunking strategy.

    Args:
    data (List[int]): The input data to be chunked.
    chunking_strategy (str): The chunking strategy to use (static, dynamic, or hybrid).
    chunk_size (int): The size of each chunk for static chunking. Defaults to 10.
    max_chunk_size (int): The maximum size of each chunk for dynamic chunking. Defaults to 20.

    Returns:
    Tuple[float, float]: The total processing time and the sum of the processed chunks.
    """
    start_time = time.time()
    if chunking_strategy == 'static':
        chunks = static_chunking(data, chunk_size)
    elif chunking_strategy == 'dynamic':
        chunks = dynamic_chunking(data, max_chunk_size)
    elif chunking_strategy == 'hybrid':
        chunks = hybrid_chunking(data, chunk_size, max_chunk_size)
    else:
        raise ValueError("Invalid chunking strategy")
    
    total_sum = 0
    for chunk in chunks:
        total_sum += process_chunk(chunk)
    
    end_time = time.time()
    total_time = end_time - start_time
    return total_time, total_sum

def main():
    parser = argparse.ArgumentParser(description='Evaluate chunking strategies for RAG pipelines')
    parser.add_argument('--chunking_strategy', type=str, choices=['static', 'dynamic', 'hybrid'], required=True)
    parser.add_argument('--chunk_size', type=int, default=10)
    parser.add_argument('--max_chunk_size', type=int, default=20)
    parser.add_argument('--data_size', type=int, default=1000)
    args = parser.parse_args()

    data = list(range(args.data_size))
    total_time, total_sum = evaluate_chunking_strategy(data, args.chunking_strategy, args.chunk_size, args.max_chunk_size)
    print(f"Chunking strategy: {args.chunking_strategy}")
    print(f"Total processing time: {total_time:.2f} seconds")
    print(f"Sum of processed chunks: {total_sum}")

if __name__ == "__main__":
    main()