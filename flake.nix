{
  description = "A very basic flake";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs?ref=nixos-unstable";
  };

  outputs =
    { self, nixpkgs }:
    let
      pkgs = nixpkgs.legacyPackages.x86_64-linux;
      dependencies = with pkgs; [
        figlet
      ];
    in
    {
      devShells.x86_64-linux.default = pkgs.mkShell {
        packages = with pkgs; [
          python314
        ] ++ dependencies;
      };
      packages.x86_64-linux.default = pkgs.writers.writePython3 "pymodoro" {
        libraries = dependencies;
        flakeIgnore = [ "F401" ];
      } (builtins.readFile ./main.py);
    };
}
