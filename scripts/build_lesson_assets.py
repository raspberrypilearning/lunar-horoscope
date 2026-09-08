#!/usr/bin/env python3
"""Derive the variable-free starter and QA checkpoints from the supplied SB3.

The complete archive is read-only. Checkpoints share its assets and retain its
block IDs so their additions can be audited against the actual project target.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMPLETE = ROOT / 'en/code/lunar-horoscope-complete/lunar-horoscope-complete.sb3'
SOURCE_SHA256 = '68fac17f7e74bcf72e315c4aff6a779ff3e8da341ae7461dd6c5327c7ae95fff'
VARIABLE_STEPS = {
    'var_birth_year': 5, 'var_cycle': 7,
    'var_animal_index': 8, 'var_animal_name': 8,
    'var_element_index': 9, 'var_element_name': 9,
    'var_costume_number': 10, 'var_your_sign': 11,
}
STAGE_STEPS = {
    4: 4, 6: 11, 7: 4, 8: 4, 9: 5, 10: 5, 13: 6, 27: 7,
    33: 8, 36: 9, 41: 8, 45: 9, 49: 10, 55: 11, 63: 12, 64: 12,
    65: 15, 66: 15, 70: 15, 74: 15, 78: 15,
    82: 16, 86: 16, 90: 16, 94: 17, 96: 17, 97: 17, 98: 17,
}


def read_complete():
    with zipfile.ZipFile(COMPLETE) as archive:
        return json.loads(archive.read('project.json'))


def subtree(blocks, block_id, include_next=False):
    found = {block_id}
    block = blocks[block_id]
    for name, value in block.get('inputs', {}).items():
        for child in value[1:]:
            if isinstance(child, str) and child in blocks:
                found |= subtree(blocks, child, name.startswith('SUBSTACK'))
    if include_next and block.get('next'):
        found |= subtree(blocks, block['next'], True)
    return found


def remove_stack(blocks, hat):
    for key in subtree(blocks, hat, True):
        del blocks[key]


def checkpoint(step):
    project = copy.deepcopy(read_complete())
    stage = project['targets'][0]
    blocks = stage['blocks']
    selected = (['stage_block_0003'] if step >= 4 else []) + [
        f'stage_block_{number:04d}' for number, introduced in STAGE_STEPS.items()
        if introduced <= step
    ]
    keep = subtree(blocks, 'stage_block_0001', True) if step >= 2 else set()
    for key in selected:
        keep |= subtree(blocks, key)
    stage['blocks'] = {key: value for key, value in blocks.items() if key in keep}
    for index, key in enumerate(selected):
        stage['blocks'][key]['next'] = selected[index + 1] if index + 1 < len(selected) else None
        stage['blocks'][key]['parent'] = selected[index - 1] if index else None
    stage['variables'] = {
        key: [value[0], 0] for key, value in stage['variables'].items()
        if VARIABLE_STEPS[key] <= step
    }
    stage['currentCostume'] = 0
    for target in project['targets'][1:]:
        blocks = target['blocks']
        name = target['name']
        if name in {'Zodiac Wheel', 'Element Wheel'}:
            prefix = 'zodiac' if name == 'Zodiac Wheel' else 'element'
            introduced = 12 if prefix == 'zodiac' else 13
            if step < (2 if prefix == 'zodiac' else 3):
                remove_stack(blocks, f'{prefix}_block_0001')
            if step < 17:
                remove_stack(blocks, f'{prefix}_block_0022')
            if step < introduced:
                remove_stack(blocks, f'{prefix}_block_0007')
            elif step < 14:
                repeat = blocks[f'{prefix}_block_0008']
                old_reporter = repeat['inputs']['TIMES'][1]
                for key in subtree(blocks, old_reporter):
                    del blocks[key]
                repeat['inputs']['TIMES'] = [1, [6, '60']]
            target.update(visible=True, direction=90)
            target.update(x=-112 if prefix == 'zodiac' else 112,
                          y=45 if prefix == 'zodiac' else 75,
                          size=35 if prefix == 'zodiac' else 25)
        elif name == 'Animal':
            if step < 4:
                remove_stack(blocks, 'animal_block_0001')
            if step < 10:
                remove_stack(blocks, 'animal_block_0005')
            elif step < 18:
                for key in subtree(blocks, 'animal_block_0014'):
                    del blocks[key]
                del blocks['animal_block_0011']
                del blocks['animal_block_0017']
                blocks['animal_block_0010']['next'] = 'animal_block_0012'
                blocks['animal_block_0012']['parent'] = 'animal_block_0010'
                blocks['animal_block_0013']['next'] = None
            target.update(visible=False, currentCostume=0)
        elif name == 'Try Another Year':
            if step < 4:
                remove_stack(blocks, 'button_block_0001')
            if step < 19:
                remove_stack(blocks, 'button_block_0003')
                remove_stack(blocks, 'button_block_0007')
            target['visible'] = False
        elif name == 'Pointers':
            if step < 3:
                remove_stack(blocks, 'pointers_block_0001')
            if step < 17:
                remove_stack(blocks, 'pointers_block_0006')
            target.update(visible=True, x=0, y=0, size=100)
    project['monitors'] = [
        monitor for monitor in project['monitors']
        if monitor['opcode'] != 'data_variable' or monitor['id'] in stage['variables']
    ]
    for monitor in project['monitors']:
        monitor['visible'] = False
        if monitor['opcode'] == 'data_listcontents':
            monitor['value'] = copy.deepcopy(stage['lists'][monitor['id']][1])
        else:
            monitor['value'] = 0
    return project


def write_archive(path, project):
    path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(COMPLETE) as source, zipfile.ZipFile(path, 'w', zipfile.ZIP_DEFLATED) as output:
        for item in source.infolist():
            if item.filename != 'project.json':
                output.writestr(item, source.read(item.filename))
        output.writestr('project.json', json.dumps(project, separators=(',', ':')))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--checkpoint', type=int, choices=range(1, 23), help='Also package a QA checkpoint under render_targets.')
    args = parser.parse_args()
    digest = hashlib.sha256(COMPLETE.read_bytes()).hexdigest()
    if digest != SOURCE_SHA256:
        raise SystemExit('The complete SB3 changed; review the lesson mappings before rebuilding.')
    write_archive(ROOT / 'en/code/lunar-horoscope-starter/lunar-horoscope-starter.sb3', checkpoint(1))
    targets = ROOT / 'render_targets'
    targets.mkdir(exist_ok=True)
    for step in range(1, 23):
        (targets / f'step_{step}.json').write_text(json.dumps(checkpoint(step), indent=2) + '\n')
    if args.checkpoint:
        write_archive(targets / f'step_{args.checkpoint}.sb3', checkpoint(args.checkpoint))
    print('Built starter with all original lists and costumes, zero variables, zero scripts, and 22 JSON checkpoints.')


if __name__ == '__main__':
    main()
