let
  pkgs = import (builtins.fetchTree {
    type = "git";
    url = "https://github.com/nixos/nixpkgs/";
    rev = "d74a2335ac9c133d6bbec9fc98d91a77f1604c1f"; # 17-02-2025
    narHash = "sha256-zON2GNBkzsIyALlOCFiEBcIjI4w38GYOb+P+R4S8Jsw=";
    # obtain via `nix-prefetch-git https://github.com/nixos/nixpkgs/ --rev $(git ls-remote https://github.com/nixos/nixpkgs nixos-unstable)`
  }) { config = {}; };

  pythonCore = pkgs.python312;
  pythonPkgs = python-packages: with python-packages; [
      ptpython
      requests
    ]; 
  myPython = pythonCore.withPackages pythonPkgs;
in
pkgs.stdenv.mkDerivation rec {
  name = "gmail-notes-scrapper";
  src = ./.;

  installPhase = ''
    runHook preInstall
    
    mkdir -p $out/${myPython.sitePackages}
    cp -r . $out/${myPython.sitePackages}/${name}

    runHook postInstall
  '';

  propagatedbuildInputs =
    with pkgs;
    [
      git
      gnumake
      # this is only for the shell

      myPython
      # this is a requirement

      pyright
      ruff
      ruff-lsp
      # this is for dev lol
    ];
  buildInputs = propagatedbuildInputs;
}
