#!/usr/bin/env python3
"""Build the complete Lunar Horoscope Scratch 3 project."""

from __future__ import annotations

import hashlib
import json
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
IMAGE_DIR = ROOT / "en" / "images" / "lunar-calendar"
OUTPUT = ROOT / "en" / "solutions" / "lunar-horoscope.sb3"

ANIMALS = [
    "rat",
    "ox",
    "tiger",
    "rabbit",
    "dragon",
    "snake",
    "horse",
    "sheep",
    "monkey",
    "rooster",
    "dog",
    "pig",
]

ANIMAL_NAMES = [name.title() for name in ANIMALS]
ELEMENTS = ["wood", "fire", "earth", "metal", "water"]
ELEMENT_NAMES = [name.title() for name in ELEMENTS]

# Three compact display rows preserve every supplied animal trait while keeping
# the native Scratch list readable without scrolling.
ANIMAL_TRAIT_LINES = [
    ("Intelligent • Adaptable", "Quick-witted • Charming", "Artistic • Sociable"),
    ("Loyal • Reliable • Thorough", "Strong • Reasonable", "Steady • Determined"),
    ("Enthusiastic • Courageous", "Ambitious • Leadership", "Confidence • Charismatic"),
    ("Trustworthy • Empathic • Modest", "Diplomatic • Sincere • Sociable", "Caretakers • Sensitive"),
    ("Lucky • Flexible • Eccentric", "Imaginative • Artistic", "Spiritual • Charismatic"),
    ("Philosophical • Organised", "Intelligent • Intuitive • Elegant", "Attentive • Decisive"),
    ("Adaptable • Loyal • Courageous", "Ambitious • Intelligent", "Adventurous • Strong"),
    ("Tasteful • Crafty • Warm", "Elegant • Charming • Intuitive", "Sensitive • Calm"),
    ("Quick-witted • Charming • Lucky", "Adaptable • Bright • Versatile", "Lively • Smart"),
    ("Honest • Energetic • Intelligent", "Flamboyant • Flexible", "Diverse • Confident"),
    ("Loyal • Sociable • Courageous", "Diligent • Steady • Lively", "Adaptable • Smart"),
    ("Honourable • Philanthropic", "Determined • Optimistic", "Sincere • Sociable"),
]

ELEMENT_TRAIT_LINES = [
    ("Exceptionally gifted • Idealists", "Planners"),
    ("Courageous • Passionate", "Good at research"),
    ("Kindness • Tolerant • Honest", "Leader"),
    ("Determined • Persistent", "Workaholic • Manager"),
    ("Sympathetic • Perfectionist", "Coordinator"),
]


SPINNER_BACKDROP = """<svg xmlns="http://www.w3.org/2000/svg" width="480" height="360" viewBox="0 0 480 360">
<defs>
  <radialGradient id="bg" cx="50%" cy="42%" r="75%"><stop offset="0" stop-color="#263257"/><stop offset="0.58" stop-color="#11182f"/><stop offset="1" stop-color="#090d1b"/></radialGradient>
  <linearGradient id="gold" x1="0" x2="1"><stop stop-color="#f7d77b"/><stop offset="0.5" stop-color="#b67a24"/><stop offset="1" stop-color="#f7d77b"/></linearGradient>
</defs>
<rect width="480" height="360" fill="url(#bg)"/>
<g fill="#f6d57b" opacity=".22">
  <circle cx="26" cy="34" r="2"/><circle cx="455" cy="45" r="1.8"/><circle cx="232" cy="53" r="1.2"/><circle cx="65" cy="262" r="1.3"/><circle cx="426" cy="248" r="1.4"/><circle cx="241" cy="271" r="1.2"/>
  <path d="M25 72h28M39 58v28M427 79h24M439 67v24M225 260h30M240 245v30" stroke="#f6d57b" stroke-width="1"/>
</g>
<rect x="8" y="7" width="464" height="346" rx="20" fill="none" stroke="url(#gold)" stroke-width="2" opacity=".8"/>
<text x="240" y="21" text-anchor="middle" fill="#fff6d8" font-family="Georgia,serif" font-size="13" font-weight="700" letter-spacing="2">LUNAR HOROSCOPE</text>
<rect x="34" y="270" width="412" height="72" rx="15" fill="#11182f" stroke="#a87a32" stroke-width="1.5" opacity=".96"/>
<text x="240" y="293" text-anchor="middle" fill="#fff7df" font-family="Arial,sans-serif" font-size="14" font-weight="700">Enter a birth year to spin both wheels</text>
<text x="240" y="316" text-anchor="middle" fill="#d8cba9" font-family="Arial,sans-serif" font-size="11">Born before Lunar New Year (usually Jan/Feb)?</text>
<text x="240" y="332" text-anchor="middle" fill="#d8cba9" font-family="Arial,sans-serif" font-size="11">Enter the previous year for the traditional sign.</text>
</svg>"""


RESULT_BACKDROP = """<svg xmlns="http://www.w3.org/2000/svg" width="480" height="360" viewBox="0 0 480 360">
<defs>
  <radialGradient id="bg" cx="30%" cy="55%" r="85%"><stop offset="0" stop-color="#29385e"/><stop offset="0.58" stop-color="#11182f"/><stop offset="1" stop-color="#090d1b"/></radialGradient>
  <linearGradient id="gold" x1="0" x2="1"><stop stop-color="#f7d77b"/><stop offset="0.5" stop-color="#b67a24"/><stop offset="1" stop-color="#f7d77b"/></linearGradient>
</defs>
<rect width="480" height="360" fill="url(#bg)"/>
<rect x="8" y="7" width="464" height="346" rx="20" fill="none" stroke="url(#gold)" stroke-width="2" opacity=".8"/>
<text x="354" y="25" text-anchor="middle" fill="#fff6d8" font-family="Georgia,serif" font-size="15" font-weight="700" letter-spacing="1.5">YOUR LUNAR SIGN</text>
<text x="60" y="114" text-anchor="middle" fill="#d8cba9" font-family="Arial,sans-serif" font-size="9" font-weight="700" letter-spacing="1.2">ANIMAL</text>
<text x="180" y="114" text-anchor="middle" fill="#d8cba9" font-family="Arial,sans-serif" font-size="9" font-weight="700" letter-spacing="1.2">ELEMENT</text>
<circle cx="122" cy="220" r="108" fill="#192343" stroke="#b98a39" stroke-width="1.5" opacity=".7"/>
<path d="M28 220h188M122 126v188" stroke="#f6d57b" stroke-width="1" opacity=".08"/>
<rect x="238" y="42" width="232" height="288" rx="16" fill="#151d37" stroke="#a87a32" stroke-width="1.5" opacity=".8"/>
<text x="354" y="54" text-anchor="middle" fill="#d8cba9" font-family="Arial,sans-serif" font-size="9" letter-spacing="1">YEAR • ELEMENT • ANIMAL</text>
</svg>"""


POINTERS = """<svg xmlns="http://www.w3.org/2000/svg" width="480" height="360" viewBox="0 0 480 360">
<defs><linearGradient id="g" x1="0" x2="1"><stop stop-color="#fff2a6"/><stop offset=".5" stop-color="#d3952f"/><stop offset="1" stop-color="#fff2a6"/></linearGradient></defs>
<g font-family="Arial,sans-serif" font-size="10" font-weight="700" letter-spacing="1.4" text-anchor="middle" fill="#fff3c1">
  <text x="128" y="29">ANIMAL</text><text x="352" y="29">ELEMENT</text>
</g>
<g fill="url(#g)" stroke="#5f3a0a" stroke-width="2">
  <path d="M116 33h24l-12 20z"/><path d="M340 33h24l-12 20z"/>
</g>
<g fill="#fff8d5"><circle cx="128" cy="39" r="3"/><circle cx="352" cy="39" r="3"/></g>
</svg>"""


TRY_AGAIN = """<svg xmlns="http://www.w3.org/2000/svg" width="176" height="48" viewBox="0 0 176 48">
<defs><linearGradient id="b" x1="0" y1="0" x2="0" y2="1"><stop stop-color="#f3ce6d"/><stop offset="1" stop-color="#b77620"/></linearGradient></defs>
<rect x="2" y="2" width="172" height="44" rx="22" fill="#0d1429" stroke="url(#b)" stroke-width="3"/>
<text x="88" y="30" text-anchor="middle" fill="#fff5d1" font-family="Arial,sans-serif" font-size="14" font-weight="700">TRY ANOTHER YEAR</text>
</svg>"""


VARIABLES = {
    "var_birth_year": ["Birth Year", 0],
    "var_cycle": ["Cycle", 0],
    "var_animal_index": ["Animal Index", 0],
    "var_element_index": ["Element Index", 0],
    "var_animal_name": ["Animal Name", "Rat"],
    "var_element_name": ["Element Name", "Wood"],
    "var_costume_number": ["Costume Number", 1],
    "var_your_sign": ["Your Sign", ""],
}

LISTS = {
    "list_animal_names": ["Animal Names", ANIMAL_NAMES],
    "list_element_names": ["Element Names", ELEMENT_NAMES],
    "list_animal_headings": ["Animal Headings", [f"{name.upper()} TRAITS" for name in ANIMAL_NAMES]],
    "list_animal_trait_1": ["Animal Trait Line 1", [rows[0] for rows in ANIMAL_TRAIT_LINES]],
    "list_animal_trait_2": ["Animal Trait Line 2", [rows[1] for rows in ANIMAL_TRAIT_LINES]],
    "list_animal_trait_3": ["Animal Trait Line 3", [rows[2] for rows in ANIMAL_TRAIT_LINES]],
    "list_element_headings": ["Element Headings", [f"{name.upper()} ELEMENT" for name in ELEMENT_NAMES]],
    "list_element_trait_1": ["Element Trait Line 1", [rows[0] for rows in ELEMENT_TRAIT_LINES]],
    "list_element_trait_2": ["Element Trait Line 2", [rows[1] for rows in ELEMENT_TRAIT_LINES]],
    "list_your_traits": ["Your Traits", []],
}

BROADCASTS = {
    "broadcast_start": "START",
    "broadcast_spin": "SPIN",
    "broadcast_reveal": "REVEAL",
}


def literal(value, input_type=10):
    return {"node": "literal", "value": value, "input_type": input_type}


def expression(opcode, inputs=None, fields=None):
    return {"node": "expression", "opcode": opcode, "inputs": inputs or {}, "fields": fields or {}}


def variable(variable_id):
    return expression("data_variable", fields={"VARIABLE": [VARIABLES[variable_id][0], variable_id]})


def answer():
    return expression("sensing_answer")


def direction():
    return expression("motion_direction")


def number(value):
    return literal(value, 4)


def text(value):
    return literal(value, 10)


def binary(opcode, left, right, left_name="NUM1", right_name="NUM2", kind="number"):
    return expression(opcode, {left_name: (kind, left), right_name: (kind, right)})


def add(left, right):
    return binary("operator_add", left, right)


def subtract(left, right):
    return binary("operator_subtract", left, right)


def multiply(left, right):
    return binary("operator_multiply", left, right)


def divide(left, right):
    return binary("operator_divide", left, right)


def modulo(left, right):
    return binary("operator_mod", left, right)


def equals(left, right):
    return binary("operator_equals", left, right, "OPERAND1", "OPERAND2", "string")


def greater(left, right):
    return binary("operator_gt", left, right, "OPERAND1", "OPERAND2", "string")


def less(left, right):
    return binary("operator_lt", left, right, "OPERAND1", "OPERAND2", "string")


def boolean_and(left, right):
    return binary("operator_and", left, right, "OPERAND1", "OPERAND2", "boolean")


def join(left, right):
    return binary("operator_join", left, right, "STRING1", "STRING2", "string")


def random_number(low, high):
    return expression("operator_random", {"FROM": ("number", number(low)), "TO": ("number", number(high))})


def round_number(value):
    return expression("operator_round", {"NUM": ("number", value)})


def floor_number(value):
    return expression("operator_mathop", {"NUM": ("number", value)}, {"OPERATOR": ["floor", None]})


def list_item(list_id, index):
    return expression(
        "data_itemoflist",
        {"INDEX": ("number", index)},
        {"LIST": [LISTS[list_id][0], list_id]},
    )


def statement(opcode, inputs=None, fields=None, substacks=None):
    return {
        "opcode": opcode,
        "inputs": inputs or {},
        "fields": fields or {},
        "substacks": substacks or {},
    }


def set_variable(variable_id, value):
    return statement(
        "data_setvariableto",
        {"VALUE": ("string", value)},
        {"VARIABLE": [VARIABLES[variable_id][0], variable_id]},
    )


def show_variable(variable_id):
    return statement("data_showvariable", fields={"VARIABLE": [VARIABLES[variable_id][0], variable_id]})


def hide_variable(variable_id):
    return statement("data_hidevariable", fields={"VARIABLE": [VARIABLES[variable_id][0], variable_id]})


def clear_list(list_id):
    return statement("data_deletealloflist", fields={"LIST": [LISTS[list_id][0], list_id]})


def add_to_list(list_id, value):
    return statement(
        "data_addtolist",
        {"ITEM": ("string", value)},
        {"LIST": [LISTS[list_id][0], list_id]},
    )


def show_list(list_id):
    return statement("data_showlist", fields={"LIST": [LISTS[list_id][0], list_id]})


def hide_list(list_id):
    return statement("data_hidelist", fields={"LIST": [LISTS[list_id][0], list_id]})


def broadcast(name, wait=False):
    broadcast_id = next(key for key, value in BROADCASTS.items() if value == name)
    return statement(
        "event_broadcastandwait" if wait else "event_broadcast",
        {"BROADCAST_INPUT": ("broadcast", (name, broadcast_id))},
    )


def switch_backdrop(name):
    return statement("looks_switchbackdropto", {"BACKDROP": ("menu", ("looks_backdrops", "BACKDROP", name))})


def costume_by_number(value):
    return statement(
        "looks_switchcostumeto",
        {"COSTUME": ("menu_expression", (value, "looks_costume", "COSTUME", "rat_wood"))},
    )


class BlockBuilder:
    def __init__(self, prefix):
        self.blocks = {}
        self.counter = 0
        self.prefix = prefix

    def new_id(self):
        self.counter += 1
        return f"{self.prefix}_block_{self.counter:04d}"

    def base_block(self, opcode, *, parent=None, shadow=False, top_level=False):
        block_id = self.new_id()
        self.blocks[block_id] = {
            "opcode": opcode,
            "next": None,
            "parent": parent,
            "inputs": {},
            "fields": {},
            "shadow": shadow,
            "topLevel": top_level,
        }
        return block_id

    def encode_input(self, spec, parent):
        kind, value = spec
        if kind == "broadcast":
            name, broadcast_id = value
            return [1, [11, name, broadcast_id]]
        if kind == "menu":
            opcode, field_name, field_value = value
            menu_id = self.base_block(opcode, parent=parent, shadow=True)
            self.blocks[menu_id]["fields"] = {field_name: [field_value, None]}
            return [1, menu_id]
        if kind == "menu_expression":
            expr, opcode, field_name, field_value = value
            reporter_id = self.emit_expression(expr, parent)
            menu_id = self.base_block(opcode, parent=parent, shadow=True)
            self.blocks[menu_id]["fields"] = {field_name: [field_value, None]}
            return [3, reporter_id, menu_id]
        if value["node"] == "literal":
            input_type = value["input_type"]
            raw = value["value"]
            if input_type in {4, 5, 6, 7, 8}:
                raw = str(raw)
            return [1, [input_type, raw]]
        reporter_id = self.emit_expression(value, parent)
        if kind == "boolean":
            return [2, reporter_id]
        input_type = {"number": 4, "positive": 5, "integer": 6, "angle": 8, "string": 10}[kind]
        return [3, reporter_id, [input_type, ""]]

    def emit_expression(self, spec, parent):
        block_id = self.base_block(spec["opcode"], parent=parent)
        block = self.blocks[block_id]
        block["fields"] = spec["fields"]
        block["inputs"] = {
            name: self.encode_input(input_spec, block_id)
            for name, input_spec in spec["inputs"].items()
        }
        return block_id

    def emit_statement(self, spec):
        block_id = self.base_block(spec["opcode"])
        block = self.blocks[block_id]
        block["fields"] = spec["fields"]
        block["inputs"] = {
            name: self.encode_input(input_spec, block_id)
            for name, input_spec in spec["inputs"].items()
        }
        for input_name, child_specs in spec["substacks"].items():
            first_child = self.emit_stack(child_specs, block_id)
            if first_child is not None:
                block["inputs"][input_name] = [2, first_child]
        return block_id

    def emit_stack(self, specs, parent):
        ids = [self.emit_statement(spec) for spec in specs]
        if not ids:
            return None
        for index, block_id in enumerate(ids):
            self.blocks[block_id]["parent"] = parent if index == 0 else ids[index - 1]
            if index:
                self.blocks[ids[index - 1]]["next"] = block_id
        return ids[0]

    def add_hat(self, opcode, body, *, fields=None, x=24, y=24):
        hat_id = self.base_block(opcode, top_level=True)
        hat = self.blocks[hat_id]
        hat["fields"] = fields or {}
        hat["x"] = x
        hat["y"] = y
        hat["next"] = self.emit_stack(body, hat_id)
        return hat_id


def compile_blocks(hats, prefix):
    builder = BlockBuilder(prefix)
    for hat in hats:
        builder.add_hat(**hat)
    return builder.blocks


def flag_hat(body, x=24, y=24):
    return {"opcode": "event_whenflagclicked", "body": body, "x": x, "y": y}


def receive_hat(name, body, x=24, y=120):
    broadcast_id = next(key for key, value in BROADCASTS.items() if value == name)
    return {
        "opcode": "event_whenbroadcastreceived",
        "fields": {"BROADCAST_OPTION": [name, broadcast_id]},
        "body": body,
        "x": x,
        "y": y,
    }


def clicked_hat(body, x=24, y=24):
    return {"opcode": "event_whenthisspriteclicked", "body": body, "x": x, "y": y}


def stage_blocks():
    valid_year = boolean_and(
        boolean_and(equals(answer(), variable("var_birth_year")), greater(variable("var_birth_year"), number(0))),
        less(variable("var_birth_year"), number(10000)),
    )

    animal_lookup_index = add(variable("var_animal_index"), number(1))
    element_lookup_index = add(variable("var_element_index"), number(1))

    main = [
        switch_backdrop("Spinner"),
        hide_variable("var_your_sign"),
        hide_list("list_your_traits"),
        clear_list("list_your_traits"),
        statement(
            "sensing_askandwait",
            {"QUESTION": ("string", text("Enter a whole birth year. Born before Lunar New Year? Enter the previous year."))},
        ),
        set_variable("var_birth_year", round_number(answer())),
        statement(
            "control_repeat_until",
            {"CONDITION": ("boolean", valid_year)},
            substacks={
                "SUBSTACK": [
                    statement(
                        "sensing_askandwait",
                        {"QUESTION": ("string", text("Please enter one whole numerical year, for example 2024."))},
                    ),
                    set_variable("var_birth_year", round_number(answer())),
                ]
            },
        ),
        set_variable(
            "var_cycle",
            modulo(
                add(modulo(subtract(variable("var_birth_year"), number(1984)), number(60)), number(60)),
                number(60),
            ),
        ),
        set_variable("var_animal_index", modulo(variable("var_cycle"), number(12))),
        set_variable(
            "var_element_index",
            floor_number(divide(modulo(variable("var_cycle"), number(10)), number(2))),
        ),
        set_variable("var_animal_name", list_item("list_animal_names", animal_lookup_index)),
        set_variable("var_element_name", list_item("list_element_names", element_lookup_index)),
        set_variable(
            "var_costume_number",
            add(add(multiply(variable("var_animal_index"), number(5)), variable("var_element_index")), number(1)),
        ),
        set_variable(
            "var_your_sign",
            join(
                variable("var_birth_year"),
                join(text(" • "), join(variable("var_element_name"), join(text(" "), variable("var_animal_name")))),
            ),
        ),
        broadcast("SPIN", wait=True),
        statement("control_wait", {"DURATION": ("positive", number(0.6))}),
        clear_list("list_your_traits"),
        add_to_list("list_your_traits", list_item("list_animal_headings", animal_lookup_index)),
        add_to_list("list_your_traits", list_item("list_animal_trait_1", animal_lookup_index)),
        add_to_list("list_your_traits", list_item("list_animal_trait_2", animal_lookup_index)),
        add_to_list("list_your_traits", list_item("list_animal_trait_3", animal_lookup_index)),
        add_to_list("list_your_traits", list_item("list_element_headings", element_lookup_index)),
        add_to_list("list_your_traits", list_item("list_element_trait_1", element_lookup_index)),
        add_to_list("list_your_traits", list_item("list_element_trait_2", element_lookup_index)),
        switch_backdrop("Result"),
        show_variable("var_your_sign"),
        show_list("list_your_traits"),
        broadcast("REVEAL", wait=True),
    ]

    return compile_blocks(
        [
            flag_hat([broadcast("START")], x=24, y=24),
            receive_hat("START", main, x=24, y=110),
        ],
        "stage",
    )


def wheel_blocks(kind):
    is_animal = kind == "animal"
    index_var = "var_animal_index" if is_animal else "var_element_index"
    wheel_count = 12 if is_animal else 5
    landing_step_count = 5 if is_animal else 12
    degree_step = 30 if is_animal else 72
    start_x = -112 if is_animal else 112
    result_x = -180 if is_animal else -60

    repeat_count = add(
        multiply(random_number(2, 6), number(60)),
        multiply(modulo(subtract(number(wheel_count), variable(index_var)), number(wheel_count)), number(landing_step_count)),
    )

    reset = [
        statement("motion_setrotationstyle", fields={"STYLE": ["all around", None]}),
        statement("motion_gotoxy", {"X": ("number", number(start_x)), "Y": ("number", number(45))}),
        statement("looks_setsizeto", {"SIZE": ("number", number(31))}),
        statement("motion_pointindirection", {"DIRECTION": ("angle", number(90))}),
        statement("looks_show"),
    ]

    spin = [
        statement(
            "control_repeat",
            {"TIMES": ("integer", repeat_count)},
            substacks={
                "SUBSTACK": [
                    statement("motion_turnright", {"DEGREES": ("number", number(6))}),
                    statement("control_wait", {"DURATION": ("positive", number(0.01))}),
                ]
            },
        ),
        statement(
            "motion_pointindirection",
            {
                "DIRECTION": (
                    "angle",
                    subtract(number(90), multiply(variable(index_var), number(degree_step))),
                )
            },
        ),
    ]

    reveal = [
        statement("motion_gotoxy", {"X": ("number", number(result_x)), "Y": ("number", number(122))}),
        statement("looks_setsizeto", {"SIZE": ("number", number(17))}),
    ]

    return compile_blocks(
        [
            receive_hat("START", reset, x=24, y=24),
            receive_hat("SPIN", spin, x=250, y=24),
            receive_hat("REVEAL", reveal, x=24, y=250),
        ],
        "zodiac" if is_animal else "element",
    )


def pointer_blocks():
    reset = [
        statement("motion_gotoxy", {"X": ("number", number(0)), "Y": ("number", number(0))}),
        statement("looks_setsizeto", {"SIZE": ("number", number(100))}),
        statement("looks_show"),
        statement("looks_gotofrontback", fields={"FRONT_BACK": ["front", None]}),
    ]
    return compile_blocks(
        [
            receive_hat("START", reset, x=24, y=24),
            receive_hat("REVEAL", [statement("looks_hide")], x=24, y=180),
        ],
        "pointers",
    )


def animal_blocks():
    reset = [
        statement("looks_hide"),
        statement("looks_cleargraphiceffects"),
        statement("motion_setrotationstyle", fields={"STYLE": ["don't rotate", None]}),
    ]
    reveal = [
        costume_by_number(variable("var_costume_number")),
        statement("motion_gotoxy", {"X": ("number", number(-118)), "Y": ("number", number(-42))}),
        statement("looks_setsizeto", {"SIZE": ("number", number(68))}),
        statement("looks_seteffectto", {"VALUE": ("number", number(100))}, {"EFFECT": ["GHOST", None]}),
        statement("looks_show"),
        statement("looks_gotofrontback", fields={"FRONT_BACK": ["front", None]}),
        statement(
            "control_repeat",
            {"TIMES": ("integer", number(10))},
            substacks={
                "SUBSTACK": [
                    statement("looks_changeeffectby", {"CHANGE": ("number", number(-10))}, {"EFFECT": ["GHOST", None]}),
                    statement("control_wait", {"DURATION": ("positive", number(0.02))}),
                ]
            },
        ),
        statement("looks_cleargraphiceffects"),
    ]
    return compile_blocks(
        [
            receive_hat("START", reset, x=24, y=24),
            receive_hat("REVEAL", reveal, x=250, y=24),
        ],
        "animal",
    )


def try_again_blocks():
    reveal = [
        statement("control_wait", {"DURATION": ("positive", number(0.2))}),
        statement("looks_show"),
        statement("looks_gotofrontback", fields={"FRONT_BACK": ["front", None]}),
    ]
    return compile_blocks(
        [
            receive_hat("START", [statement("looks_hide")], x=24, y=24),
            receive_hat("REVEAL", reveal, x=24, y=140),
            clicked_hat([statement("looks_hide"), broadcast("START")], x=250, y=24),
        ],
        "button",
    )


class AssetStore:
    def __init__(self):
        self.files = {}

    def add_bytes(self, data, extension):
        digest = hashlib.md5(data).hexdigest()
        filename = f"{digest}.{extension}"
        self.files[filename] = data
        return digest, filename

    def add_file(self, path):
        return self.add_bytes(path.read_bytes(), path.suffix.lstrip(".").lower())


def costume(asset_store, source, name, center_x, center_y, bitmap_resolution=1):
    if isinstance(source, str):
        asset_id, md5ext = asset_store.add_bytes(source.encode("utf-8"), "svg")
        data_format = "svg"
    else:
        asset_id, md5ext = asset_store.add_file(source)
        data_format = source.suffix.lstrip(".").lower()
    return {
        "assetId": asset_id,
        "name": name,
        "bitmapResolution": bitmap_resolution,
        "md5ext": md5ext,
        "dataFormat": data_format,
        "rotationCenterX": center_x,
        "rotationCenterY": center_y,
    }


def sprite_target(name, costumes, blocks, *, layer_order, visible, x, y, size, direction=90, rotation_style="all around"):
    return {
        "isStage": False,
        "name": name,
        "variables": {},
        "lists": {},
        "broadcasts": {},
        "blocks": blocks,
        "comments": {},
        "currentCostume": 0,
        "costumes": costumes,
        "sounds": [],
        "volume": 100,
        "layerOrder": layer_order,
        "visible": visible,
        "x": x,
        "y": y,
        "size": size,
        "direction": direction,
        "draggable": False,
        "rotationStyle": rotation_style,
    }


def build_project():
    assert len(ANIMAL_TRAIT_LINES) == len(ANIMALS)
    assert len(ELEMENT_TRAIT_LINES) == len(ELEMENTS)

    expected_costume_names = [f"{animal}_{element}" for animal in ANIMALS for element in ELEMENTS]
    missing = [name for name in expected_costume_names if not (IMAGE_DIR / f"{name}.png").is_file()]
    if missing:
        raise FileNotFoundError(f"Missing animal costumes: {', '.join(missing)}")

    asset_store = AssetStore()
    spinner_backdrop = costume(asset_store, SPINNER_BACKDROP, "Spinner", 240, 180)
    result_backdrop = costume(asset_store, RESULT_BACKDROP, "Result", 240, 180)
    pointer_costume = costume(asset_store, POINTERS, "Pointers", 240, 180)
    button_costume = costume(asset_store, TRY_AGAIN, "Try another year", 88, 24)

    zodiac_wheel = costume(
        asset_store,
        IMAGE_DIR / "chinese_zodiac_wheel.png",
        "Chinese zodiac wheel",
        627,
        627,
        bitmap_resolution=2,
    )
    element_wheel = costume(
        asset_store,
        IMAGE_DIR / "five_elements_wheel.png",
        "Five elements wheel",
        627,
        627,
        bitmap_resolution=2,
    )
    animal_costumes = [
        costume(asset_store, IMAGE_DIR / f"{name}.png", name, 300, 200, bitmap_resolution=2)
        for name in expected_costume_names
    ]

    stage = {
        "isStage": True,
        "name": "Stage",
        "variables": VARIABLES,
        "lists": LISTS,
        "broadcasts": BROADCASTS,
        "blocks": stage_blocks(),
        "comments": {},
        "currentCostume": 0,
        "costumes": [spinner_backdrop, result_backdrop],
        "sounds": [],
        "volume": 100,
        "layerOrder": 0,
        "tempo": 60,
        "videoTransparency": 50,
        "videoState": "off",
        "textToSpeechLanguage": None,
    }

    targets = [
        stage,
        sprite_target(
            "Zodiac Wheel",
            [zodiac_wheel],
            wheel_blocks("animal"),
            layer_order=1,
            visible=True,
            x=-112,
            y=45,
            size=31,
        ),
        sprite_target(
            "Element Wheel",
            [element_wheel],
            wheel_blocks("element"),
            layer_order=2,
            visible=True,
            x=112,
            y=45,
            size=31,
        ),
        sprite_target(
            "Pointers",
            [pointer_costume],
            pointer_blocks(),
            layer_order=3,
            visible=True,
            x=0,
            y=0,
            size=100,
            rotation_style="don't rotate",
        ),
        sprite_target(
            "Animal",
            animal_costumes,
            animal_blocks(),
            layer_order=4,
            visible=False,
            x=-118,
            y=-42,
            size=68,
            rotation_style="don't rotate",
        ),
        sprite_target(
            "Try Another Year",
            [button_costume],
            try_again_blocks(),
            layer_order=5,
            visible=False,
            x=-118,
            y=-148,
            size=100,
            rotation_style="don't rotate",
        ),
    ]

    project = {
        "targets": targets,
        "monitors": [
            {
                "id": "var_your_sign",
                "mode": "large",
                "opcode": "data_variable",
                "params": {"VARIABLE": "Your Sign"},
                "spriteName": None,
                "value": "",
                "width": 220,
                "height": 34,
                "x": 244,
                "y": 59,
                "visible": False,
                "sliderMin": 0,
                "sliderMax": 100,
                "isDiscrete": True,
            },
            {
                "id": "list_your_traits",
                "mode": "list",
                "opcode": "data_listcontents",
                "params": {"LIST": "Your Traits"},
                "spriteName": None,
                "value": [],
                "width": 220,
                "height": 222,
                "x": 244,
                "y": 98,
                "visible": False,
            },
        ],
        "extensions": [],
        "meta": {"semver": "3.0.0", "vm": "11.3.0", "agent": "Codex"},
    }

    return project, asset_store.files, expected_costume_names


def zodiac_for_year(year):
    cycle = ((year - 1984) % 60 + 60) % 60
    return ANIMAL_NAMES[cycle % 12], ELEMENT_NAMES[(cycle % 10) // 2]


def validate_project(project, asset_files, expected_costume_names):
    expected_cases = {
        1960: ("Rat", "Metal"),
        1984: ("Rat", "Wood"),
        1985: ("Ox", "Wood"),
        1986: ("Tiger", "Fire"),
        1991: ("Sheep", "Metal"),
        2000: ("Dragon", "Metal"),
        2024: ("Dragon", "Wood"),
        2025: ("Snake", "Wood"),
        2026: ("Horse", "Fire"),
    }
    for year, expected in expected_cases.items():
        assert zodiac_for_year(year) == expected, (year, zodiac_for_year(year), expected)

    assert len(project["targets"]) == 6
    animal = next(target for target in project["targets"] if target["name"] == "Animal")
    assert [item["name"] for item in animal["costumes"]] == expected_costume_names
    assert len(animal["costumes"]) == 60

    referenced = []
    for target in project["targets"]:
        for item in target["costumes"] + target["sounds"]:
            referenced.append(item["md5ext"])
            assert item["md5ext"] in asset_files
            digest = hashlib.md5(asset_files[item["md5ext"]]).hexdigest()
            assert digest == item["assetId"]
            assert item["md5ext"] == f"{digest}.{item['dataFormat']}"
    assert len(referenced) == 66
    assert len(set(referenced)) == 66


def main():
    project, asset_files, expected_costume_names = build_project()
    validate_project(project, asset_files, expected_costume_names)

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    project_json = json.dumps(project, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    with zipfile.ZipFile(OUTPUT, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        archive.writestr("project.json", project_json)
        for filename, data in sorted(asset_files.items()):
            archive.writestr(filename, data)

    with zipfile.ZipFile(OUTPUT) as archive:
        assert archive.testzip() is None
        loaded = json.loads(archive.read("project.json"))
        assert len(loaded["targets"]) == 6
        assert len(archive.namelist()) == 67

    print(f"Built {OUTPUT}")
    print(f"Size: {OUTPUT.stat().st_size / (1024 * 1024):.2f} MiB")
    print("Targets: Stage, Zodiac Wheel, Element Wheel, Pointers, Animal, Try Another Year")
    print("Animal costumes: 60")
    print("Assets: 66")


if __name__ == "__main__":
    main()
