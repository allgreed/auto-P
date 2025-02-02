let
  pkgs = import (builtins.fetchGit {
    url = "https://github.com/nixos/nixpkgs/";
    ref = "refs/heads/nixos-unstable";
    rev = "76612b17c0ce71689921ca12d9ffdc9c23ce40b2"; # 13-11-2024
    # obtain via `git ls-remote https://github.com/nixos/nixpkgs nixos-unstable`
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
