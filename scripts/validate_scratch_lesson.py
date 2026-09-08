#!/usr/bin/env python3
"""Validate the Scratch adaptation, source preservation, and lesson checkpoints.

Uses the actual SB3 expression graph for calculation checks. This is a focused
static/data-flow check, not a replacement for running animations in Scratch.
"""
from __future__ import annotations

import copy
import hashlib
import json
import math
import re
import zipfile
from pathlib import Path

from build_lesson_assets import COMPLETE, ROOT, SOURCE_SHA256, VARIABLE_STEPS, checkpoint, read_complete

errors = []
warnings = []
checks = 0


def check(condition, message):
    global checks
    checks += 1
    if not condition:
        errors.append(message)


def validate_graph(project, label):
    stage = project['targets'][0]
    globals_ = stage['variables']
    lists = stage['lists']
    for target in project['targets']:
        blocks = target['blocks']
        variables = {**globals_, **target['variables']}
        for key, block in blocks.items():
            for link in ('next', 'parent'):
                check(block.get(link) is None or block[link] in blocks, f'{label}/{target["name"]}/{key}: broken {link}')
            for name, value in block.get('fields', {}).items():
                if name == 'VARIABLE':
                    check(value[1] in variables, f'{label}: variable used before creation: {value}')
                if name == 'LIST':
                    check(value[1] in lists, f'{label}: missing list {value}')
            for name, value in block.get('inputs', {}).items():
                for child in value[1:]:
                    if isinstance(child, str):
                        check(child in blocks, f'{label}: missing input block {child}')
                        if child in blocks:
                            check(blocks[child]['parent'] == key, f'{label}: wrong parent on {child}')
                    elif isinstance(child, list) and child[0] == 12:
                        check(child[2] in variables, f'{label}: undeclared variable reporter {child[1]}')
        for monitor in project['monitors']:
            if monitor['opcode'] == 'data_variable':
                check(monitor['id'] in globals_, f'{label}: undeclared variable monitor')


class Expressions:
    def __init__(self, project, answer):
        self.stage = project['targets'][0]
        self.blocks = self.stage['blocks']
        self.variables = {k: v[1] for k, v in self.stage['variables'].items()}
        self.lists = copy.deepcopy(self.stage['lists'])
        self.answer = answer

    @staticmethod
    def number(value):
        try:
            return float(value)
        except (ValueError, TypeError):
            return 0.0

    @staticmethod
    def string(value):
        return str(int(value)) if isinstance(value, float) and value.is_integer() else str(value)

    def value(self, raw):
        if isinstance(raw, str):
            return self.expr(raw)
        if raw[0] == 12:
            return self.variables[raw[2]]
        return raw[1]

    def expr(self, key):
        b = self.blocks[key]
        op = b['opcode']
        a = {k: self.value(v[1]) for k, v in b.get('inputs', {}).items() if not k.startswith('SUBSTACK')}
        if op == 'sensing_answer': return self.answer
        if op == 'data_variable': return self.variables[b['fields']['VARIABLE'][1]]
        if op == 'operator_round': return math.floor(self.number(a['NUM']) + 0.5)
        if op == 'operator_mathop':
            assert b['fields']['OPERATOR'][0] == 'floor'
            return math.floor(self.number(a['NUM']))
        if op == 'operator_join': return self.string(a['STRING1']) + self.string(a['STRING2'])
        if op == 'data_itemoflist':
            index = int(self.number(a['INDEX']))
            items = self.lists[b['fields']['LIST'][1]][1]
            assert 1 <= index <= len(items), f'out-of-range list index {index}'
            return items[index - 1]
        if op == 'operator_equals':
            try:
                if str(a['OPERAND1']).strip() and str(a['OPERAND2']).strip():
                    return float(a['OPERAND1']) == float(a['OPERAND2'])
            except (ValueError, TypeError):
                pass
            return str(a['OPERAND1']).lower() == str(a['OPERAND2']).lower()
        if op == 'operator_gt': return self.number(a['OPERAND1']) > self.number(a['OPERAND2'])
        if op == 'operator_lt': return self.number(a['OPERAND1']) < self.number(a['OPERAND2'])
        if op == 'operator_and': return bool(a['OPERAND1'] and a['OPERAND2'])
        if op == 'operator_add': return self.number(a['NUM1']) + self.number(a['NUM2'])
        if op == 'operator_subtract': return self.number(a['NUM1']) - self.number(a['NUM2'])
        if op == 'operator_multiply': return self.number(a['NUM1']) * self.number(a['NUM2'])
        if op == 'operator_divide': return self.number(a['NUM1']) / self.number(a['NUM2'])
        if op == 'operator_mod': return self.number(a['NUM1']) % self.number(a['NUM2'])
        raise ValueError(f'Unsupported expression: {op}')

    def calculate(self):
        key = 'stage_block_0003'
        while key:
            b = self.blocks[key]
            op = b['opcode']
            if op == 'data_setvariableto':
                self.variables[b['fields']['VARIABLE'][1]] = self.value(b['inputs']['VALUE'][1])
            elif op == 'control_repeat_until':
                if not self.value(b['inputs']['CONDITION'][1]): return False
            elif op == 'data_deletealloflist':
                self.lists[b['fields']['LIST'][1]][1].clear()
            elif op == 'data_addtolist':
                self.lists[b['fields']['LIST'][1]][1].append(self.value(b['inputs']['ITEM'][1]))
            key = b['next']
        return True


def main():
    content = ROOT / 'en'
    check(hashlib.sha256(COMPLETE.read_bytes()).hexdigest() == SOURCE_SHA256, 'Complete source archive was changed')
    complete = read_complete()
    starter_path = content / 'code/lunar-horoscope-starter/lunar-horoscope-starter.sb3'
    with zipfile.ZipFile(starter_path) as z, zipfile.ZipFile(COMPLETE) as source:
        starter = json.loads(z.read('project.json'))
        check(z.testzip() is None, 'Starter ZIP checksum failure')
        for filename in source.namelist():
            if filename != 'project.json':
                check(z.read(filename) == source.read(filename), f'Asset altered: {filename}')
    check(starter == checkpoint(1), 'Starter does not match lesson starting state')
    for a, b in zip(starter['targets'], complete['targets']):
        check(not a['blocks'], f'Starter scripts found in {a["name"]}')
        check(not a['variables'], f'Starter variables found in {a["name"]}')
        check(a['lists'] == b['lists'], f'Starter list data differs: {a["name"]}')
        check(a['costumes'] == b['costumes'], f'Starter costume order differs: {a["name"]}')
    for step in range(1, 23):
        project = checkpoint(step)
        validate_graph(project, f'step {step}')
        expected_vars = {key for key, n in VARIABLE_STEPS.items() if n <= step}
        check(set(project['targets'][0]['variables']) == expected_vars, f'step {step}: wrong variable set')
        if step >= 5:
            for year in (1, 1983, 1984, 2024, 2025, 2026, 2044, 9999):
                runtime = Expressions(project, str(year))
                check(runtime.calculate(), f'step {step}: valid input rejected: {year}')
        if step >= 6:
            for value in ('hello', '', '0', '-1', '10000', '2024.5'):
                check(not Expressions(project, value).calculate(), f'step {step}: invalid input accepted: {value!r}')
    for a, b in zip(checkpoint(19)['targets'], complete['targets']):
        check(a['blocks'] == b['blocks'], f'Final lesson blocks differ from target: {a["name"]}')
    expected_examples = {1984: ('Rat', 'Wood', 1), 2024: ('Dragon', 'Wood', 21),
                         2025: ('Snake', 'Wood', 26), 2026: ('Horse', 'Fire', 32),
                         1983: ('Pig', 'Water', 60), 2044: ('Rat', 'Wood', 1)}
    costumes = next(t for t in complete['targets'] if t['name'] == 'Animal')['costumes']
    for year in range(1, 10000):
        runtime = Expressions(complete, str(year))
        check(runtime.calculate(), f'Valid year rejected: {year}')
        v = runtime.variables
        number = int(v['var_costume_number'])
        check(1 <= number <= 60, f'Invalid costume number for {year}')
        check(costumes[number - 1]['name'] == f'{v["var_animal_name"].lower()}_{v["var_element_name"].lower()}', f'Costume/name mismatch for {year}')
        check(len(runtime.lists['list_your_traits'][1]) == 7, f'Wrong trait count for {year}')
        if year in expected_examples:
            check((v['var_animal_name'], v['var_element_name'], number) == expected_examples[year], f'Test-table mismatch: {year}')
        if year <= 9939:
            later = Expressions(complete, str(year + 60)); later.calculate()
            check(later.variables['var_costume_number'] == number, f'60-year periodicity failed for {year}')
    # Dino Jump is the formatting authority: intro, then quoted TASK callouts.
    paths = sorted(content.glob('step_*.md'), key=lambda p: int(p.stem.split('_')[1]))
    check([p.name for p in paths] == [f'step_{n}.md' for n in range(1, 23)], 'Step numbering is not contiguous')
    titles = []
    for n, path in enumerate(paths, 1):
        text = path.read_text()
        headings = re.findall(r'^## (.+)$', text, re.M)
        check(len(headings) == 1, f'{path.name}: expected one plain Markdown title')
        titles.append(headings[0])
        check(text.startswith(f'## {headings[0]}\n\n'), f'{path.name}: title placement')
        check('c-project-' not in text and '### Step' not in text, f'{path.name}: outdated ProjectShaper layout')
        goal = text.split('\n\n')[1]
        check(len(re.findall(r'[.!?](?=\s|$)', goal)) == 1, f'{path.name}: summary must be one sentence')
        if n == 1:
            check(headings == ['What you will make'], 'Introduction title mismatch')
            check('[!TASK]' not in text and '**Test' not in text and '```' not in text, 'Introduction must contain no tasks, tests, or code')
            check('starter' not in text.lower(), 'Starter belongs in step 2, not the introduction')
            check('[!NOPRINT]' in text and '[!PRINTONLY]' in text, 'Introduction needs separate screen/print previews')
        else:
            check('> [!TASK]' in text, f'{path.name}: missing task callouts')
            final_task = text.rsplit('> [!TASK]', 1)[-1]
            check('**Test your project.**' in final_task, f'{path.name}: missing final observable test task')
        unquoted = re.sub(r'^> ?', '', text, flags=re.M)
        blocks = re.findall(r'```blocks3\n(.*?)\n```', unquoted, re.S)
        quoted_blocks = list(re.finditer(r'^> ```blocks3\n((?:>.*\n)*?)> ```', text, re.M))
        check(len(blocks) == len(quoted_blocks), f'{path.name}: code must be quoted inside a task')
        for match in quoted_blocks:
            callouts = re.findall(r'^> \[!(\w+)\]', text[:match.start()], re.M)
            check(callouts and callouts[-1] == 'TASK', f'{path.name}: code outside a TASK callout')
        check(bool(blocks) == (n not in {1, 20, 21, 22}), f'{path.name}: expected coding/noncoding step')
        for block in blocks:
            check(any(line.startswith('+') for line in block.splitlines()), f'{path.name}: missing new-block highlights')
            check(block.count('(') == block.count(')'), f'{path.name}: unbalanced round inputs')
            check('[YYYY]' not in block, f'{path.name}: unescaped literal brackets')
        check(not re.search(r'TODO|REPLACE-WITH|Hello, world|language: python|main\.py', text), f'{path.name}: stale placeholder')
        for target in re.findall(r'\]\(([^)]+)\)|src="([^"]+)"', text):
            link = next(value for value in target if value)
            if not link.startswith(('https:', 'http:', '#')):
                check((content / link).is_file(), f'{path.name}: broken local link {link}')
    step_two = (content / 'step_2.md').read_text()
    check('.sb3)' not in step_two and 'Load from your computer' not in step_two, 'Step 2 must start from a Scratch URL, not a download workflow')
    starter_links = re.findall(r'https://scratch\.mit\.edu/projects/\d+(?:/editor)?/?', step_two)
    if not starter_links:
        warnings.append('Starter Scratch URL is awaiting the user; step 2 has the opening task but no invented link.')
    intro = (content / 'step_1.md').read_text()
    if '<iframe' not in intro:
        warnings.append('Completed Scratch URL is awaiting the user; the introduction uses the observed project screenshot as its preview.')
    meta = (content / 'meta.yml').read_text()
    meta_titles = re.findall(r'^  - title: [\'"]?(.*?)[\'"]?$', meta, re.M)
    check(meta_titles == titles, 'Metadata titles differ from lessons')
    check('landing:' not in meta, 'Dino Jump uses step 1 as the introduction; remove separate landing metadata')
    entries = re.split(r'^  - title:', meta, flags=re.M)[1:]
    for n, entry in enumerate(entries, 1):
        expected = {2: 'engaged', 16: 'internal', 20: 'external'}.get(n)
        completions = re.findall(r"^      - ['\"]?(\w+)", entry, re.M)
        check(completions == ([expected] if expected else []), f'step {n}: completion placement')
        check(('challenge: true' in entry) == (n == 22), f'step {n}: challenge placement')
    for kind in ('starter', 'complete'):
        folders = list((content / 'code').glob(f'*-{kind}'))
        check(len(folders) == 1, f'Expected one {kind} folder')
        config = (folders[0] / 'project_config.yml').read_text()
        check("type: 'scratch'" in config and 'build: true' in config, f'{kind}: wrong config')
        check(f'identifier: "{folders[0].name}"' in config, f'{kind}: wrong identifier')
    check(not (content / 'landing.md').exists(), 'Outdated separate landing page remains')
    check((content / 'images/banner.png').is_file(), 'Hero image missing')
    render_path = content / 'images/render_status.json'
    check(render_path.is_file(), 'Missing render status')
    if render_path.is_file():
        status = json.loads(render_path.read_text())
        check(set(status['steps']) == {str(n) for n in range(1, 23)}, 'Render coverage mismatch')
        for n, record in status['steps'].items():
            exists = (content / record['output']).is_file()
            check(exists == (record['status'] == 'generated'), f'step {n}: dishonest render status')
            if not exists:
                check(bool(record.get('reason')), f'step {n}: missing render reason')
        missing = [n for n, r in status['steps'].items() if r['status'] != 'generated']
        if missing: warnings.append('No screenshot for steps: ' + ', '.join(missing) + '; see render_status.json.')
    result = {'checks': checks, 'errors': errors, 'warnings': warnings,
              'calculation_years_checked': 9999, 'checkpoints_checked': 22,
              'complete_sha256': SOURCE_SHA256}
    (ROOT / 'render_targets/validation_report.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))
    raise SystemExit(bool(errors))


if __name__ == '__main__':
    main()
