
# parsetab.py
# This file is automatically generated. Do not edit.
_tabversion = '3.2'

_lr_method = 'LALR'

_lr_signature = '\xd6\x9f+As\xaa\xe7X\xcb\xeb\xf6\x14$6\x1ab'

_lr_action_items = {'STAR':([34,],[39,]),'REGIONCOLOR_ID':([15,22,23,27,31,33,36,37,45,46,47,48,67,74,],[-43,34,-16,-43,-17,-18,34,-21,-25,-22,-23,-24,-34,-26,]),'RPAREN':([80,89,],[84,90,]),'SEMICOLON':([42,50,55,58,59,60,61,62,65,66,79,84,],[53,56,-43,67,-37,-35,-36,-39,74,-27,-28,-38,]),'OFFSET_ID':([64,78,],[69,69,]),'MIN_DIAMETER_ID':([14,20,21,28,56,],[-43,30,-8,-9,-10,]),'FILENAME':([4,49,],[12,55,]),'COMMA':([39,40,41,54,57,64,68,70,72,73,82,83,85,87,90,],[-42,51,-40,63,-41,-43,75,-32,78,-31,-29,-33,86,88,-30,]),'COLON':([26,30,39,40,41,57,69,71,],[35,38,-42,52,-40,-41,76,77,]),'$end':([2,3,5,6,7,8,13,24,29,32,44,],[-6,-3,-2,-5,0,-4,-1,-11,-7,-15,-19,]),'RBRACE':([11,14,15,16,17,20,21,22,23,25,27,28,31,33,36,37,45,46,47,48,53,56,64,67,70,72,73,74,82,83,90,],[-43,-43,-43,24,-12,29,-8,32,-16,-13,-43,-9,-17,-18,44,-21,-25,-22,-23,-24,-14,-10,-43,-34,-32,79,-31,-26,-29,-33,-30,]),'LBRACE':([1,9,10,12,18,19,55,],[11,14,15,-43,27,-20,64,]),'LPAREN':([35,52,76,],[43,43,81,]),'ID':([11,16,17,25,52,53,],[-43,26,-12,-13,62,-14,]),'OPTION_DEFAULTS_ID':([0,2,3,5,6,7,8,13,24,29,32,44,],[9,-6,-3,-2,-5,9,-4,-1,-11,-7,-15,-19,]),'MAKEPLY_ID':([0,2,3,5,6,7,8,13,24,29,32,44,],[4,-6,-3,-2,-5,4,-4,-1,-11,-7,-15,-19,]),'COLOR_ALIASES_ID':([0,2,3,5,6,7,8,13,24,29,32,44,],[1,-6,-3,-2,-5,1,-4,-1,-11,-7,-15,-19,]),'FLOAT':([38,],[50,]),'INT':([34,43,51,63,75,77,81,86,88,],[41,54,57,68,80,82,85,87,89,]),'TRIM_ID':([64,78,],[71,71,]),'INCLUDE_ID':([27,36,37,45,46,47,48,67,74,],[-43,49,-21,-25,-22,-23,-24,-34,-26,]),'IGNORE_ID':([52,],[59,]),'COLOR_DEFAULTS_ID':([0,2,3,5,6,7,8,13,24,29,32,44,],[10,-6,-3,-2,-5,10,-4,-1,-11,-7,-15,-19,]),}

_lr_action = { }
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = { }
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'color':([52,],[58,]),'makeply_block_stmt':([36,],[46,]),'color_rgb':([35,52,],[42,60,]),'option_block_stmts':([14,],[20,]),'config_block':([0,7,],[5,13,]),'makeply_block_stmts':([27,],[36,]),'color_aliases_block_stmt':([16,],[25,]),'include_options':([64,],[72,]),'color_defaults_block_stmts':([15,],[22,]),'color_aliases_block_stmts':([11,],[16,]),'int_list':([34,],[40,]),'include_option':([64,78,],[70,83,]),'color_alias':([52,],[61,]),'config':([0,],[7,]),'empty':([11,12,14,15,27,55,64,],[17,19,21,23,37,66,73,]),'color_defaults_block_stmt':([22,],[31,]),'option_block_stmt':([20,],[28,]),'region_color_def':([22,36,],[33,45,]),'include_option_set':([55,],[65,]),'makeply_block':([0,7,],[2,2,]),'makeply_block_stmt_include':([36,],[48,]),'options_block':([0,7,],[6,6,]),'color_aliases_block':([0,7,],[8,8,]),'color_defaults_block':([0,7,],[3,3,]),'ply_block_open':([12,],[18,]),'makeply_block_stmt_color':([36,],[47,]),}

_lr_goto = { }
for _k, _v in _lr_goto_items.items():
   for _x,_y in zip(_v[0],_v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = { }
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> config","S'",1,None,None,None),
  ('config -> config config_block','config',2,'p_config_completeB','/home/michael/hw_to_come/morphforge/src/morphforgecontrib/indev/meshtools/mesh_config_parser.py',155),
  ('config -> config_block','config',1,'p_config_completeB','/home/michael/hw_to_come/morphforge/src/morphforgecontrib/indev/meshtools/mesh_config_parser.py',156),
  ('config_block -> color_defaults_block','config_block',1,'p_configblocksA','/home/michael/hw_to_come/morphforge/src/morphforgecontrib/indev/meshtools/mesh_config_parser.py',163),
  ('config_block -> color_aliases_block','config_block',1,'p_configblocksA','/home/michael/hw_to_come/morphforge/src/morphforgecontrib/indev/meshtools/mesh_config_parser.py',164),
  ('config_block -> options_block','config_block',1,'p_configblocksA','/home/michael/hw_to_come/morphforge/src/morphforgecontrib/indev/meshtools/mesh_config_parser.py',165),
  ('config_block -> makeply_block','config_block',1,'p_configblocksA','/home/michael/hw_to_come/morphforge/src/morphforgecontrib/indev/meshtools/mesh_config_parser.py',166),
  ('options_block -> OPTION_DEFAULTS_ID LBRACE option_block_stmts RBRACE','options_block',4,'p_option_defaults_block','/home/michael/hw_to_come/morphforge/src/morphforgecontrib/indev/meshtools/mesh_config_parser.py',174),
  ('option_block_stmts -> empty','option_block_stmts',1,'p_option_defaults_block_stmts','/home/michael/hw_to_come/morphforge/src/morphforgecontrib/indev/meshtools/mesh_config_parser.py',177),
  ('option_block_stmts -> option_block_stmts option_block_stmt','option_block_stmts',2,'p_option_defaults_block_stmts','/home/michael/hw_to_come/morphforge/src/morphforgecontrib/indev/meshtools/mesh_config_parser.py',178),
  ('option_block_stmt -> MIN_DIAMETER_ID COLON FLOAT SEMICOLON','option_block_stmt',4,'p_option_block_block_stmt','/home/michael/hw_to_come/morphforge/src/morphforgecontrib/indev/meshtools/mesh_config_parser.py',182),
  ('color_aliases_block -> COLOR_ALIASES_ID LBRACE color_aliases_block_stmts RBRACE','color_aliases_block',4,'p_color_aliases_block','/home/michael/hw_to_come/morphforge/src/morphforgecontrib/indev/meshtools/mesh_config_parser.py',196),
  ('color_aliases_block_stmts -> empty','color_aliases_block_stmts',1,'p_color_aliases_block_stmts','/home/michael/hw_to_come/morphforge/src/morphforgecontrib/indev/meshtools/mesh_config_parser.py',200),
  ('color_aliases_block_stmts -> color_aliases_block_stmts color_aliases_block_stmt','color_aliases_block_stmts',2,'p_color_aliases_block_stmts','/home/michael/hw_to_come/morphforge/src/morphforgecontrib/indev/meshtools/mesh_config_parser.py',201),
  ('color_aliases_block_stmt -> ID COLON color_rgb SEMICOLON','color_aliases_block_stmt',4,'p_color_aliases_block_stmt','/home/michael/hw_to_come/morphforge/src/morphforgecontrib/indev/meshtools/mesh_config_parser.py',205),
  ('color_defaults_block -> COLOR_DEFAULTS_ID LBRACE color_defaults_block_stmts RBRACE','color_defaults_block',4,'p_color_defaults_block','/home/michael/hw_to_come/morphforge/src/morphforgecontrib/indev/meshtools/mesh_config_parser.py',214),
  ('color_defaults_block_stmts -> empty','color_defaults_block_stmts',1,'p_color_defaults_block_stmts','/home/michael/hw_to_come/morphforge/src/morphforgecontrib/indev/meshtools/mesh_config_parser.py',218),
  ('color_defaults_block_stmts -> color_defaults_block_stmts color_defaults_block_stmt','color_defaults_block_stmts',2,'p_color_defaults_block_stmts','/home/michael/hw_to_come/morphforge/src/morphforgecontrib/indev/meshtools/mesh_config_parser.py',219),
  ('color_defaults_block_stmt -> region_color_def','color_defaults_block_stmt',1,'p_color_defaults_block_stmt','/home/michael/hw_to_come/morphforge/src/morphforgecontrib/indev/meshtools/mesh_config_parser.py',224),
  ('makeply_block -> MAKEPLY_ID FILENAME ply_block_open LBRACE makeply_block_stmts RBRACE','makeply_block',6,'p_ply_block','/home/michael/hw_to_come/morphforge/src/morphforgecontrib/indev/meshtools/mesh_config_parser.py',237),
  ('ply_block_open -> empty','ply_block_open',1,'p_ply_block_open','/home/michael/hw_to_come/morphforge/src/morphforgecontrib/indev/meshtools/mesh_config_parser.py',241),
  ('makeply_block_stmts -> empty','makeply_block_stmts',1,'p_ply_block_stmts','/home/michael/hw_to_come/morphforge/src/morphforgecontrib/indev/meshtools/mesh_config_parser.py',245),
  ('makeply_block_stmts -> makeply_block_stmts makeply_block_stmt','makeply_block_stmts',2,'p_ply_block_stmts','/home/michael/hw_to_come/morphforge/src/morphforgecontrib/indev/meshtools/mesh_config_parser.py',246),
  ('makeply_block_stmt -> makeply_block_stmt_color','makeply_block_stmt',1,'p_ply_block_stmt','/home/michael/hw_to_come/morphforge/src/morphforgecontrib/indev/meshtools/mesh_config_parser.py',251),
  ('makeply_block_stmt -> makeply_block_stmt_include','makeply_block_stmt',1,'p_ply_block_stmt','/home/michael/hw_to_come/morphforge/src/morphforgecontrib/indev/meshtools/mesh_config_parser.py',252),
  ('makeply_block_stmt_color -> region_color_def','makeply_block_stmt_color',1,'p_ply_block_stmt_color','/home/michael/hw_to_come/morphforge/src/morphforgecontrib/indev/meshtools/mesh_config_parser.py',257),
  ('makeply_block_stmt_include -> INCLUDE_ID FILENAME include_option_set SEMICOLON','makeply_block_stmt_include',4,'p_ply_block_stmt_include','/home/michael/hw_to_come/morphforge/src/morphforgecontrib/indev/meshtools/mesh_config_parser.py',264),
  ('include_option_set -> empty','include_option_set',1,'p_include_option_set','/home/michael/hw_to_come/morphforge/src/morphforgecontrib/indev/meshtools/mesh_config_parser.py',269),
  ('include_option_set -> LBRACE include_options RBRACE','include_option_set',3,'p_include_option_set','/home/michael/hw_to_come/morphforge/src/morphforgecontrib/indev/meshtools/mesh_config_parser.py',270),
  ('include_option -> TRIM_ID COLON INT','include_option',3,'p_include_option_trim','/home/michael/hw_to_come/morphforge/src/morphforgecontrib/indev/meshtools/mesh_config_parser.py',280),
  ('include_option -> OFFSET_ID COLON LPAREN INT COMMA INT COMMA INT RPAREN','include_option',9,'p_include_option_offset','/home/michael/hw_to_come/morphforge/src/morphforgecontrib/indev/meshtools/mesh_config_parser.py',284),
  ('include_options -> empty','include_options',1,'p_include_optionsA','/home/michael/hw_to_come/morphforge/src/morphforgecontrib/indev/meshtools/mesh_config_parser.py',289),
  ('include_options -> include_option','include_options',1,'p_include_optionsB','/home/michael/hw_to_come/morphforge/src/morphforgecontrib/indev/meshtools/mesh_config_parser.py',293),
  ('include_options -> include_options COMMA include_option','include_options',3,'p_include_optionsB','/home/michael/hw_to_come/morphforge/src/morphforgecontrib/indev/meshtools/mesh_config_parser.py',294),
  ('region_color_def -> REGIONCOLOR_ID int_list COLON color SEMICOLON','region_color_def',5,'p_region_color_def_stmt','/home/michael/hw_to_come/morphforge/src/morphforgecontrib/indev/meshtools/mesh_config_parser.py',305),
  ('color -> color_rgb','color',1,'p_color','/home/michael/hw_to_come/morphforge/src/morphforgecontrib/indev/meshtools/mesh_config_parser.py',310),
  ('color -> color_alias','color',1,'p_color','/home/michael/hw_to_come/morphforge/src/morphforgecontrib/indev/meshtools/mesh_config_parser.py',311),
  ('color -> IGNORE_ID','color',1,'p_color3','/home/michael/hw_to_come/morphforge/src/morphforgecontrib/indev/meshtools/mesh_config_parser.py',315),
  ('color_rgb -> LPAREN INT COMMA INT COMMA INT RPAREN','color_rgb',7,'p_color1','/home/michael/hw_to_come/morphforge/src/morphforgecontrib/indev/meshtools/mesh_config_parser.py',319),
  ('color_alias -> ID','color_alias',1,'p_color2','/home/michael/hw_to_come/morphforge/src/morphforgecontrib/indev/meshtools/mesh_config_parser.py',323),
  ('int_list -> INT','int_list',1,'p_int_list','/home/michael/hw_to_come/morphforge/src/morphforgecontrib/indev/meshtools/mesh_config_parser.py',329),
  ('int_list -> int_list COMMA INT','int_list',3,'p_int_list','/home/michael/hw_to_come/morphforge/src/morphforgecontrib/indev/meshtools/mesh_config_parser.py',330),
  ('int_list -> STAR','int_list',1,'p_int_list_star','/home/michael/hw_to_come/morphforge/src/morphforgecontrib/indev/meshtools/mesh_config_parser.py',337),
  ('empty -> <empty>','empty',0,'p_empty','/home/michael/hw_to_come/morphforge/src/morphforgecontrib/indev/meshtools/mesh_config_parser.py',342),
]
