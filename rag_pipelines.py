import argparse
import time
from typing import List, Tuple

def static_chunking(data: List[str], chunk_size: int) -> List[List[str]]:
    """
    Static chunking strategy that splits data into fixed-size chunks.

    Args:
    - data (List[str]): Input data to be chunked.
    - chunk_size (int): Size of each chunk.

    Returns:
    - List[List[str]]: Chunked data.
    """
    return [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]


def dynamic_chunking(data: List[str], max_chunk_size: int) -> List[List[str]]:
    """
    Dynamic chunking strategy that splits data into variable-size chunks based on max_chunk_size.

    Args:
    - data (List[str]): Input data to be chunked.
    - max_chunk_size (int): Maximum size of each chunk.

    Returns:
    - List[List[str]]: Chunked data.
    """
    chunks = []
    current_chunk = []
    current_size = 0
    for item in data:
        if current_size + len(item) > max_chunk_size:
            chunks.append(current_chunk)
            current_chunk = [item]
            current_size = len(item)
        else:
            current_chunk.append(item)
            current_size += len(item)
    if current_chunk:
        chunks.append(current_chunk)
    return chunks


def hybrid_chunking(data: List[str], chunk_size: int, max_chunk_size: int) -> List[List[str]]:
    """
    Hybrid chunking strategy that combines static and dynamic chunking.

    Args:
    - data (List[str]): Input data to be chunked.
    - chunk_size (int): Size of each chunk.
    - max_chunk_size (int): Maximum size of each chunk.

    Returns:
    - List[List[str]]: Chunked data.
    """
    chunks = []
    current_chunk = []
    current_size = 0
    for item in data:
        if current_size + len(item) > max_chunk_size:
            chunks.append(current_chunk)
            current_chunk = [item]
            current_size = len(item)
        elif len(current_chunk) >= chunk_size:
            chunks.append(current_chunk)
            current_chunk = [item]
            current_size = len(item)
        else:
            current_chunk.append(item)
            current_size += len(item)
    if current_chunk:
        chunks.append(current_chunk)
    return chunks


def process_chunk(chunk: List[str]) -> Tuple[int, float]:
    """
    Simulate processing a chunk by sleeping for a duration proportional to the chunk size.

    Args:
    - chunk (List[str]): Chunk to be processed.

    Returns:
    - Tuple[int, float]: Chunk size and processing time.
    """
    chunk_size = len(''.join(chunk))
    processing_time = chunk_size / 1000  # Simulate processing time
    time.sleep(processing_time)
    return chunk_size, processing_time


def main():
    parser = argparse.ArgumentParser(description='RAG Pipeline Chunking Strategies')
    parser.add_argument('--chunking_strategy', choices=['static', 'dynamic', 'hybrid'], required=True)
    parser.add_argument('--chunk_size', type=int, required=True)
    parser.add_argument('--max_chunk_size', type=int, required=True)
    parser.add_argument('--data_size', type=int, required=True)
    args = parser.parse_args()

    data = [f'Data {i}' for i in range(args.data_size)]

    if args.chunking_strategy == 'static':
        chunks = static_chunking(data, args.chunk_size)
    elif args.chunking_strategy == 'dynamic':
        chunks = dynamic_chunking(data, args.max_chunk_size)
    else:
        chunks = hybrid_chunking(data, args.chunk_size, args.max_chunk_size)

    total_chunk_size = 0
    total_processing_time = 0
    for chunk in chunks:
        chunk_size, processing_time = process_chunk(chunk)
        total_chunk_size += chunk_size
        total_processing_time += processing_time

    print(f'Chunking Strategy: {args.chunking_strategy}')
    print(f'Total Chunk Size: {total_chunk_size}')
    print(f'Total Processing Time: {total_processing_time}')


if __name__ == '__main__':
    main()