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

def solve_part_1(blocks: list[Block]):
    compact_blocks = move_file_blocks_into_compact_position(blocks)
    return sum(
        i * block.file_id
        for i, block in enumerate(compact_blocks)
        if not block.empty
    )

if __name__ == '__main__':
    blocks = read_disk_map()

    print(f"Answer for part 1: {solve_part_1(blocks)}")
    # print(f"Answer for part 2: {solve_part_2(blocks)}")
