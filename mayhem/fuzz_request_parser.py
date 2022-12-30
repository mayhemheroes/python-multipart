#! /usr/bin/env python3
import atheris
import logging
import sys

logging.disable(logging.CRITICAL)

import fuzz_helpers

with atheris.instrument_imports(include=["multipart"]):
    import multipart
    from multipart.exceptions import FormParserError, ParseError

def on_field(field):
    pass

def on_file(file):
    pass

@atheris.instrument_func
def TestOneInput(data):
    fdp = fuzz_helpers.EnhancedFuzzedDataProvider(data)
    try:
        headers = fuzz_helpers.build_fuzz_dict(fdp, [bytes, bytes])
        headers['Content-Type'] = fdp.ConsumeRandomBytes()  # Required

        with fdp.ConsumeMemoryFile(all_data=True, as_bytes=True) as inp_stream:
            multipart.parse_form(headers, inp_stream, on_field, on_file)
    except (FormParserError, ParseError):
        return -1


def main():
    atheris.Setup(sys.argv, TestOneInput)
    atheris.Fuzz()


if __name__ == "__main__":
    main()
