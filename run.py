#! /usr/bin/env python
from frontend import app
import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 33507))
    app.run(debug=True, port=port)
