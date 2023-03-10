{
  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";

  outputs = { self, nixpkgs }:
    let
      supportedSystems = [ "x86_64-linux" "x86_64-darwin" "aarch64-linux" "aarch64-darwin" ];
      forAllSystems = nixpkgs.lib.genAttrs supportedSystems;
      pkgs = forAllSystems (system: nixpkgs.legacyPackages.${system});
    in
    {
      packages = forAllSystems (system: {
        default = pkgs.${system}.poetry2nix.mkPoetryApplication {
          projectDir = self;
          overrides = pkgs.${system}.poetry2nix.defaultPoetryOverrides.extend
            (self: super: {
              discord-py = super.discord-py.overridePythonAttrs
                (
                  old: {
                    buildInputs = (old.buildInputs or [ ]) ++ [ super.setuptools ];
                  }
                );
              pytest = super.pytest.overridePythonAttrs
                (
                  old: {
                    buildInputs = (old.buildInputs or [ ]) ++ [ super.hatchling ];
                  }
                );
            });
        };
      });

      devShells = forAllSystems (system: {
        default = pkgs.${system}.mkShellNoCC {
          packages = with pkgs.${system}; [
            (poetry2nix.mkPoetryEnv { projectDir = self; })
            poetry
          ];
        };
      });
    };
}
