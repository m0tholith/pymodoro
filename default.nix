{
  python3Packages,
  figlet,
}:
python3Packages.buildPythonApplication {
  pname = "pymodoro";
  version = "1.0";
  propagatedBuildInputs = [ figlet ];
  src = ./.;
}
