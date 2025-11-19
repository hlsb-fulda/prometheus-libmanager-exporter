{
  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs =
    {
      self,
      nixpkgs,
      flake-utils,
      ...
    }:
    flake-utils.lib.eachDefaultSystem (
      system:
      let
        pkgs = nixpkgs.legacyPackages.${system};

      in
      {
        packages = {
          prometheus-libmanager-exporter = pkgs.python3.pkgs.callPackage ./package.nix { };
          default = self.packages.${system}.prometheus-libmanager-exporter;
        };

        devShells.default = pkgs.mkShell {
          inputsFrom = [ self.packages.${system}.prometheus-libmanager-exporter ];
          packages = [
            self.packages.${system}.prometheus-libmanager-exporter.build-system
            pkgs.uv
            pkgs.python3.pkgs.ruff
            pkgs.python3.pkgs.pytest
          ];
        };

        formatter = pkgs.nixfmt-tree;
      }
    );
}
