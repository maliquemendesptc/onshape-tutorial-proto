# Each step should be defined as a python dict below, following the structure of "step_X" where X is the step number.
step_1 = {
  "step": 1,
  "instruction_step": "Assembling the Peg",
  "instruction_title": "Part Design",
  "instructions": """
    Click the <em class=\"green-txt\">sketch</em> tool on the upper left side of your screen.
  """,
  "hint_txt": "You design is too large – is the dimension set to 3.5 in?",
  "imgorvid": "step1.png"
}
step_2 = {
  "step": 2,
  "instruction_step": "Second Instruction Step",
  "instruction_title": "Second Title",
  "instructions": """
    Click the <em class=\"green-txt\">sketch</em> tool on the upper left side of your screen.2
  """,
  "hint_txt": "You design is too large – is the dimension set to 3.5 in?2",
  "imgorvid": "step2.png"
}

# Each step should then be added to this python array below, in the order that they will appear.
instructions_list = [step_1, step_2]
