from typing import NamedTuple

Block = NamedTuple('Block', [
    ('empty', bool),
    ('file_id', int),
])

def read_disk_map() -> list[Block]:
    with open('./inputs/day_9.txt') as f:
        blocks = []
        file_id = 0
        block_definitions = f.readline().rstrip()
        for definition_index, block_definition in enumerate(block_definitions):
            is_empty = definition_index % 2 == 1
            for _ in range(int(block_definition)):
                blocks.append(
                    Block(empty=is_empty, file_id=file_id if not is_empty else None)
                )
            if not is_empty:
                file_id += 1
    return blocks

def is_compact(blocks: list[Block]) -> bool:
    "Return whether `blocks` is compact, and if not the first empty block index"
    first_empty_index = next(i for i, block in enumerate(blocks) if block.empty)
    is_compact = all(block.empty for block in blocks[first_empty_index:])
    return is_compact, first_empty_index if not is_compact else None

def move_file_blocks_into_compact_position(blocks: list[Block]) -> list[Block]:
    new_blocks = [*blocks]

    def get_file_block_from_end():
        return next((block, -i-1) for i, block in enumerate(new_blocks[::-1]) if not block.empty)

    while True:
        is_blocks_compact, first_empty_index = is_compact(new_blocks)
        if is_blocks_compact:
            break
        file_block, file_block_index = get_file_block_from_end()
        new_blocks[file_block_index] = new_blocks[first_empty_index]
        new_blocks[first_empty_index] = file_block

    return new_blocks

def checksum(blocks: list[Block]) -> int:
    return sum(
        i * block.file_id
        for i, block in enumerate(blocks)
        if not block.empty
    )

def solve_part_1(blocks: list[Block]) -> int:
    compact_blocks = move_file_blocks_into_compact_position(blocks)
    return checksum(compact_blocks)

def move_files_into_compact_position(blocks: list[Block]) -> list[Block]:
    def get_next_empty_block_series(block_list: list[Block]):
        it = enumerate(block_list)
        i, block = next(it)
        try:
            while True:
                current_series = []
                current_series_indices = []
                while not block.empty:
                    i, block = next(it)
                while block.empty:
                    current_series.append(block)
                    current_series_indices.append(i)
                    i, block = next(it)
                yield current_series, current_series_indices
        except StopIteration:
            return

    def get_next_file_block_series_from_end(block_list: list[Block]):
        get_index = lambda i: len(block_list) - i - 1
        it = enumerate(block_list[::-1])
        i, block = next(it)
        try:
            while True:
                current_file_id = None
                current_series = []
                current_series_indices = []
                while block.empty:
                    i, block = next(it)
                while not block.empty:
                    if current_file_id != None and block.file_id != current_file_id:
                        break
                    current_file_id = block.file_id
                    current_series.append(block)
                    current_series_indices.append(get_index(i))
                    i, block = next(it)
                yield current_series, list(reversed(current_series_indices))
        except StopIteration:
            return

    new_blocks = [*blocks]
    for file_blocks, file_blocks_indices in get_next_file_block_series_from_end(blocks):
        for empty_blocks, empty_blocks_indices in get_next_empty_block_series(new_blocks):
            if len(empty_blocks) >= len(file_blocks) and file_blocks_indices[0] > empty_blocks_indices[0]:
                (
                    new_blocks[empty_blocks_indices[0]:empty_blocks_indices[0]+len(file_blocks)],
                    new_blocks[file_blocks_indices[0]:file_blocks_indices[-1]+1],
                ) = (
                    new_blocks[file_blocks_indices[0]:file_blocks_indices[-1]+1],
                    new_blocks[empty_blocks_indices[0]:empty_blocks_indices[0]+len(file_blocks)],
                )
                break
    return new_blocks

def print_blocks(blocks: list[Block]):
    for block in blocks:
        print(block.file_id if not block.empty else '.', end='')
    print()

def solve_part_2(blocks: list[Block]) -> int:
    compact_blocks = move_files_into_compact_position(blocks)
    return checksum(compact_blocks)

if __name__ == '__main__':
    blocks = read_disk_map()

    print(f"Answer for part 1: {solve_part_1(blocks)}")
    print(f"Answer for part 2: {solve_part_2(blocks)}")
