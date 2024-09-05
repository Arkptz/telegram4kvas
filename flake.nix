{
  description = "Application packaged using poetry2nix";

  inputs = {
    flake-utils.url = "github:numtide/flake-utils";
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
    poetry2nix = {
      url = "github:arkptz/poetry2nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs = {
    self,
    flake-utils,
    poetry2nix,
    nixpkgs,
  }:
    flake-utils.lib.eachDefaultSystem (system: let
      pkgs = import nixpkgs {
        inherit system;
        overlays = [
          (self: super: {
          })
          poetry2nix.overlays.default
        ];
      };

      inherit (poetry2nix.lib.mkPoetry2Nix {inherit pkgs;}) mkPoetryApplication mkPoetryEnv overrides cleanPythonSources;

      cleanSources = cleanPythonSources {src = ./.;};
      defaultPython = pkgs.python311;
      pythonPackages = defaultPython.pkgs;
      defaultOverrides =
        overrides.withDefaults
        (
          self: super: {
            uuid6 = super.uuid6.overridePythonAttrs (old: {
              nativeBuildInputs = old.nativeBuildInputs or [] ++ [self.setuptools];
            });

            pendulum = pythonPackages.pendulum;
          }
        );

      defaultAttrs = {
        projectDir = cleanSources;
        python = defaultPython;
        overrides = defaultOverrides;
      };
    in {
      devShells.default = let
        poetryEnv = (mkPoetryEnv defaultAttrs).override {ignoreCollisions = true;};
        makeLibraryPath = packages: pkgs.lib.concatStringsSep ":" (map (package: "${pkgs.lib.getLib package}/lib") packages);
        mpv_fixed =
          pkgs.mpv-unwrapped.overrideAttrs
          (oldAttrs: {
            postInstall =
              oldAttrs.postInstall
              or ""
              + ''
                ln -s $out/lib/libmpv.so $out/lib/libmpv.so.1
              '';
          });
        libs = with pkgs; [
          openssl
          stdenv.cc.cc.lib
          libz
          glib
          defaultPython
        ];
      in
        pkgs.mkShell {
          buildInputs = libs;
          nativeBuildInputs = with pkgs; [
            poetry
            pre-commit
          ];
          packages = with pkgs; [
            poetryEnv
            poetry
          ];

          NIX_LD_LIBRARY_PATH = makeLibraryPath libs;
          shellHook = ''
            unset SOURCE_DATE_EPOCH
            export LD_LIBRARY_PATH=$NIX_LD_LIBRARY_PATH:$LD_LIBRARY_PATH
            export PYTHONPATH=$PYTHONPATH:${poetryEnv}/lib/python:${poetryEnv}/lib/python3.11/site-packages
            ln -sfT ${poetryEnv.out} ./.venv
          '';
        };
    });
}
