# Prompt attempts
- `simple_parsing`: parse a section of a form NPX, where metadata has been removed and the fund name is directly specified in the prompt. User prompt is a section of `../sample_data/normal_doc/raw.txt`.
- `direct_parsing`: parse a full form NPX (using one short enough to fit in context window). User prompt contains the contents of `../sample_data/normal_doc/raw.txt`.
- `parser_generation`: generate a parser, given a sample document. User prompt contains the contents of `../sample_data/normal_doc/raw.txt`.