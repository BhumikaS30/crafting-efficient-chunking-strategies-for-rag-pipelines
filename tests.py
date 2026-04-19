import argparse
import time
from typing import List, Dict

def static_chunking(data: List[str], chunk_size: int) -> List[List[str]]:
    """
    Static chunking strategy that divides the input data into fixed-size chunks.

    Args:
    - data (List[str]): The input data to be chunked.
    - chunk_size (int): The size of each chunk.

    Returns:
    - List[List[str]]: A list of chunks, where each chunk is a list of strings.
    """
    return [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]


def dynamic_chunking(data: List[str], max_chunk_size: int) -> List[List[str]]:
    """
    Dynamic chunking strategy that divides the input data into variable-size chunks
    based on the maximum chunk size.

    Args:
    - data (List[str]): The input data to be chunked.
    - max_chunk_size (int): The maximum size of each chunk.

    Returns:
    - List[List[str]]: A list of chunks, where each chunk is a list of strings.
    """
    chunks = []
    current_chunk = []
    current_size = 0
    for item in data:
        item_size = len(item.encode('utf-8'))
        if current_size + item_size > max_chunk_size:
            chunks.append(current_chunk)
            current_chunk = [item]
            current_size = item_size
        else:
            current_chunk.append(item)
            current_size += item_size
    if current_chunk:
        chunks.append(current_chunk)
    return chunks


def hybrid_chunking(data: List[str], chunk_size: int, max_chunk_size: int) -> List[List[str]]:
    """
    Hybrid chunking strategy that combines static and dynamic chunking.

    Args:
    - data (List[str]): The input data to be chunked.
    - chunk_size (int): The size of each chunk for static chunking.
    - max_chunk_size (int): The maximum size of each chunk for dynamic chunking.

    Returns:
    - List[List[str]]: A list of chunks, where each chunk is a list of strings.
    """
    static_chunks = static_chunking(data, chunk_size)
    hybrid_chunks = []
    for chunk in static_chunks:
        dynamic_chunks = dynamic_chunking(chunk, max_chunk_size)
        hybrid_chunks.extend(dynamic_chunks)
    return hybrid_chunks


def rag_pipeline(data: List[str], chunking_strategy: str, chunk_size: int, max_chunk_size: int) -> Dict[str, float]:
    """
    Simulates a RAG pipeline with the given chunking strategy.

    Args:
    - data (List[str]): The input data to be processed.
    - chunking_strategy (str): The chunking strategy to use (static, dynamic, or hybrid).
    - chunk_size (int): The size of each chunk for static chunking.
    - max_chunk_size (int): The maximum size of each chunk for dynamic chunking.

    Returns:
    - Dict[str, float]: A dictionary containing the processing time and latency.
    """
    start_time = time.time()
    if chunking_strategy == 'static':
        chunks = static_chunking(data, chunk_size)
    elif chunking_strategy == 'dynamic':
        chunks = dynamic_chunking(data, max_chunk_size)
    elif chunking_strategy == 'hybrid':
        chunks = hybrid_chunking(data, chunk_size, max_chunk_size)
    else:
        raise ValueError('Invalid chunking strategy')
    end_time = time.time()
    processing_time = end_time - start_time
    latency = processing_time / len(chunks)
    return {'processing_time': processing_time, 'latency': latency}


def main():
    parser = argparse.ArgumentParser(description='RAG Pipeline Chunking Strategies')
    parser.add_argument('--chunking_strategy', type=str, choices=['static', 'dynamic', 'hybrid'], required=True)
    parser.add_argument('--chunk_size', type=int, required=True)
    parser.add_argument('--max_chunk_size', type=int, required=True)
    parser.add_argument('--data_size', type=int, required=True)
    args = parser.parse_args()
    data = [f'Data point {i}' for i in range(args.data_size)]
    result = rag_pipeline(data, args.chunking_strategy, args.chunk_size, args.max_chunk_size)
    print(f'Chunking Strategy: {args.chunking_strategy}')
    print(f'Processing Time: {result["processing_time"]:.2f} seconds')
    print(f'Latency: {result["latency"]:.2f} seconds')


if __name__ == '__main__':
    main()