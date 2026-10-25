# call-me-maybe



## Makefile
(maybe not a bad idea to add these to the makefile???)
To create the invalid utf-8 in invalid_encoding.json:
```
uv run python -c 'from pathlib import Path; Path("src/data/input/invalid_encoding.json").write_bytes(b"{\"prompt\": \"\xff\"}")'
```

also remember to get the reading permission from the inavlid_permission.json:
```chmod -r src/data/input/invalid_permission.json```


To run from the repo root:<br>
```uv run python -m unittest discover -s tests -v```


run only the loader tests:<br>
```uv run python -m unittest tests.test_inputs.TestJsonLoader -v```


## Notes for loading jsons:

| Exception | What went wrong |
|---|---|
| `json.JSONDecodeError` | The file contains invalid JSON |
| `UnicodeDecodeError` | The file’s bytes cannot be decoded as UTF-8 |
| `FileNotFoundError` | The requested file doesn’t exist |
| `OSError` | Another filesystem problem, such as permission denied |





## Resources
- https://docs.python.org/3/library/json.html#basic-usage
- https://docs.python.org/3/library/json.html
- https://www.geeksforgeeks.org/python/python-json/
- https://docs.python.org/3/library/unittest.html
- https://realpython.com/python-unittest/#creating-test-cases

