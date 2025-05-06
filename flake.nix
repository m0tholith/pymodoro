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
    rec {
      devShells.x86_64-linux.default = pkgs.mkShell {
        packages =
          with pkgs;
          [
            python314
          ]
          ++ dependencies;
      };
      packages.x86_64-linux.pymodoro = self.packages.x86_64-linux.default;
      packages.x86_64-linux.default = pkgs.callPackage ./default.nix { };
    };
}
