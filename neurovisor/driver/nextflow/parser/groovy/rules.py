
# GLOBAL RULES


STATEMENT_ID_RULES = [[
    "expression",
    "postfix_expression",
    "path_expression",
    "primary",
    "identifier"
]]

BLOCK_STATEMENT_ID_RULES = [
    [
        "block_statement",
        "statement"
    ],
    [
        "identifier"
    ]
]

MODULE_STATEMENT_RULES = [[
    "argument_list",
    "first_argument_list_element",
    "expression_list_element",
    "expression",
    "postfix_expression",
    "path_expression"
]]

COMPONENT_NAME_RULES = [[
    "primary",
    "identifier"
]]

COMPONENT_CONTENT_RULES = [
    [ 
        "path_element",
        "closure_or_lambda_expression",
        "closure",
        "block"
    ],
    [
        "block_statements_opt",
        "block_statements"
    ]
]

WORKFLOW_CONTENT_RULES = [[
    "argument_list",
    "first_argument_list_element",
    "expression_list_element",
    "expression",
    "postfix_expression",
    "path_expression"
]]
