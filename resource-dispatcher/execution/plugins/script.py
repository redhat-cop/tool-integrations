import subprocess
import sys
from jinja2 import Template

code_template = Template("""
def fn(params):
    {{ code_inject|indent(width=4) }}
""")


def initialize(params):
    if "packages" in params:
        ls = subprocess.run([sys.executable, "-m", "pip", "list"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        for package in params["packages"]:
            if package.lower() not in str(ls.stdout).lower():
                print(f"Fetching required package {package}")
                pip_install = subprocess.run([sys.executable, "-m", "pip", "install", package], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                if pip_install.returncode == 0:
                    print(str(pip_install.stdout))
                else:
                    raise Exception(f"Error fetching required package: {str(pip_install.stderr)}")


def process(context, params):

    if "script" in params and "script_file" in params:
        print("Cannot process script and script_file in the same block - please separate them.")
        raise Exception

    if "script" in params:
        return execute(params["script"], context, params)
    elif "script_file" in params:
        return execute(open(params["script_file"]).read(), context, params)


def execute(script, context, params):
    code = code_template.render(code_inject=script)
    local_vars = dict(locals())
    exec(code, local_vars)
    result = local_vars["fn"](params)
    context.update(local_vars["context"])
    return result
