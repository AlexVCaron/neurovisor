from functools import reduce

from .rules import (
    BLOCK_STATEMENT_ID_RULES,
    STATEMENT_ID_RULES,
    MODULE_STATEMENT_RULES,
    COMPONENT_NAME_RULES,
    COMPONENT_CONTENT_RULES,
    WORKFLOW_CONTENT_RULES
)


def _extract_strings(node):
    leaf_type = node.get("leaf")
    if leaf_type == "DEF":
        yield "def "
    elif leaf_type == "AS":
        yield " as "
    elif leaf_type == "IDENTIFIER" and node["value"] in ("tuple",):
        # line start identifier
        yield f"{node['value']} "
    elif leaf_type == "IDENTIFIER" and node["value"] in ("from",):
        # middle line identifier
        yield f" {node['value']} "
    elif leaf_type is not None:
        # if leaf_type in (
        #     "GSTRING_PART",
        #     "IDENTIFIER",
        #     "STRING_LITERAL",
        #     "STRING_LITERAL_PART",
        #     "DOT"
        # ):
        yield node["value"]
    else:
        children = node.get("children")
        if isinstance(children, list):
            for child in children:
                yield from _extract_strings(child)


def _recurse_component(json_tree, rules, cmp=lambda _: True):

    def _recurse(_trees, _rule):
        for _tree in _trees:
            if _tree is not None and "rule" in _tree and _tree["rule"] == _rule:
                return _tree["children"]

    _res = reduce(
        lambda t, r: _recurse(t, r) if t is not None else None,
        rules, [json_tree]
    )

    if _res is None:
        if "children" in json_tree:
            for child in json_tree["children"]:
                _res = _recurse_component(child, rules, cmp)

                if _res is not None:
                    break

    if _res is not None and cmp(_res):
        return _res


def _value(_leaf):
    return _leaf[0]["value"]


def unpack_nf_module(json_tree):
    sections = ["tag", "label", "container", "input", "output", "script", "stub", "when"]
    current_section = None
    module = {}
    name = _value(_recurse_component(json_tree, COMPONENT_NAME_RULES))
    content = _recurse_component(json_tree, COMPONENT_CONTENT_RULES)
    # Unpack each section of the content
    for section in content:
        _id = _recurse_component(section, STATEMENT_ID_RULES)
        if _id is not None:
            _id = _value(_id)

        if _id in sections:
            if not _id in module:
                module[_id] = []
            current_section = _id
            module[_id].append(''.join(map(str, _extract_strings({
                "rule": ["content"],
                "children": list(filter(
                    lambda c: "rule" in c and not c["rule"] in
                        STATEMENT_ID_RULES + BLOCK_STATEMENT_ID_RULES,
                    section["children"]))
            }))))
        else:
            # We may have a block statement, try to extract it
            _id = _recurse_component(section, BLOCK_STATEMENT_ID_RULES)
            if _id is not None:
                _id = _value(_id)
                if _id in sections:
                    if not _id in module:
                        module[_id] = []
                    current_section = _id
                    module[_id].append(''.join(map(str, _extract_strings({
                        "rule": ["content"],
                        "children": list(filter(
                            lambda c: "rule" in c and not c["rule"] in
                                STATEMENT_ID_RULES + BLOCK_STATEMENT_ID_RULES,
                            section["children"]))
                    }))))
            else:
                # We don't know what to do, so we just continue filling previous section
                module[current_section].append(
                    ''.join(map(str, _extract_strings(section))))

    # Split args from script
    script, args = [], []
    for it in module["script"]:
        if it[:3] == "\"\"\"":
            # Script content always starts with triple quotes
            script.append(it)
        else:
            args.append(it)

    module["script"] = script
    module["args"] = args
    module["stub"] = list(filter(lambda a: a[:3] == "\"\"\"", module["stub"]))
    module["name"] = name

    return module


def unpack_nf_workflow(json_tree):
    sections = ["take", "main", "emit"]
    current_section = None
    module = {}
    name = _value(_recurse_component(json_tree, COMPONENT_NAME_RULES))
    content = _recurse_component(json_tree, COMPONENT_CONTENT_RULES)
    # Unpack each section of the content
    for section in content:
        _id = _recurse_component(section, STATEMENT_ID_RULES)
        if _id is not None:
            _id = _value(_id)

        if _id in sections:
            if not _id in module:
                module[_id] = []
            current_section = _id
            module[_id].append(''.join(map(str, _extract_strings({
                "rule": ["content"],
                "children": list(filter(
                    lambda c: "rule" in c and not c["rule"] in
                        STATEMENT_ID_RULES + BLOCK_STATEMENT_ID_RULES,
                    section["children"]))
            }))))
        else:
            # We may have a block statement, try to extract it
            _id = _recurse_component(section, BLOCK_STATEMENT_ID_RULES)
            if _id is not None:
                _id = _value(_id)
                if _id in sections:
                    if not _id in module:
                        module[_id] = []
                    current_section = _id
                    module[_id].append(''.join(map(str, _extract_strings({
                        "rule": ["content"],
                        "children": list(filter(
                            lambda c: "rule" in c and not c["rule"] in
                                STATEMENT_ID_RULES + BLOCK_STATEMENT_ID_RULES,
                            section["children"]))
                    }))))
            else:
                # We don't know what to do, so we just continue filling previous section
                module[current_section].append(
                    ''.join(map(str, _extract_strings(section))))

    module["name"] = name

    return module


def unpack_nf_include(json_tree):
    return ''.join(map(str, _extract_strings({
        "rule": ["include"],
        "children": list(filter(lambda c: "rule" in c and not c["rule"] in
                                STATEMENT_ID_RULES,
                                json_tree["children"]))
    })))


def unpack_nf_parameter(json_tree):
    pass


def unpack_nf_component(json_tree):
    # Unpack first layer of children (includes, params, component)
    workflow, includes = None, []
    for statement in json_tree["children"]:
        # Find statement type
        _statement = _recurse_component(statement, STATEMENT_ID_RULES)
        _type = _value(_statement)

        if _type == "process":
            # Unpack whole process statement. For now, we don't support anything else than it
            return unpack_nf_module({
                "rule": ["process"],
                "children": _recurse_component(statement, MODULE_STATEMENT_RULES)
            })
        elif _type == "workflow":
            # Unpack workflow statement without params and includes
            workflow = unpack_nf_workflow({
                "rule": ["workflow"],
                "children": _recurse_component(statement, WORKFLOW_CONTENT_RULES)
            })
        elif _type == "include":
            # Unpack include statement and add to list
            includes.append(unpack_nf_include(statement))
        else:
            # Unknown type, or parameter which we don't know how to unpack yet
            NotImplementedError()

    workflow["includes"] = includes
    return workflow
