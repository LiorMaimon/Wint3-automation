import cx_Freeze

executables = [cx_Freeze.Executable("inject_simulated_water.py")]

cx_Freeze.setup(
    name="inject_simulated_water",
    options={"build_exe": {"packages": ["click"], "include_files": []}},
    executables=executables
)