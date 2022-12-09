from __future__ import annotations
from dataclasses import dataclass, field
from typing import Protocol, Optional


@dataclass
class FileType(Protocol):
    name: str
    size: int


@dataclass
class File:
    name: str
    size: int


@dataclass
class Directory:
    name: str
    size: int = 0
    contained_in: Optional[Directory] = None
    contents: dict[str, FileType] = field(default_factory=dict)
    path: str = field(init=False)

    def __post_init__(self):
        if self.contained_in is None:
            self.path = ''
            return
        self.path = f'{self.contained_in.path}/{self.name}'

    def get_subdir(self, subdir_name: str) -> Directory:
        if subdir_name not in self.contents:
            self.add_contents(subdir_name, 0)
        return self.contents[subdir_name]

    def add_contents(self, file_name: str, file_size: int) -> None:
        if file_name in self.contents:
            print(f'Conflict: {file_name} already in directory {self.name}')
        self.contents[file_name] = File(name=file_name, size=file_size)
        self.add_usage(file_size)

    def add_subdir(self, subdir_name: str) -> None:
        self.contents[subdir_name] = Directory(name=subdir_name, contained_in=self)

    def add_usage(self, usage: int) -> None:
        self.size += usage
        if self.contained_in is not None:
            self.contained_in.add_usage(usage)


ROOT = Directory(name='')
cur_dir = ROOT


def change_dir(cd: Directory, _to: str) -> Directory:
    if _to == '..':
        return cd.contained_in
    elif _to == '/':
        return ROOT
    else:
        return cd.get_subdir(_to)


def get_dir_storages(root: Directory) -> dict[str, int]:
    info = {root.path: root.size}
    for c in root.contents.values():
        if isinstance(c, Directory):
            info.update(get_dir_storages(c))
    return info


for line in open('input.txt', 'r+').readlines():
    if line.startswith('$ cd'):
        cur_dir = change_dir(cur_dir, line[5:].strip())
        continue
    elif line.startswith('$ ls'):
        continue
    size_type, info = line.split()
    if size_type.isdigit():
        cur_dir.add_contents(file_name=info.strip(), file_size=int(sizetype))
    elif size_type == 'dir':
        cur_dir.add_subdir(subdir_name=info.strip())

dir_sizes = get_dir_storages(ROOT).values()
print(f'Pt1: {sum(j for j in dir_sizes if j <= 100_000)}')
print(f'Pt2: {min(j for j in dir_sizes if j >= ROOT.size - 40_000_000)}')