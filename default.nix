let
  nixpkgs = builtins.fetchGit {
    url = "https://github.com/nixos/nixpkgs-channels/";
    ref = "refs/heads/nixos-unstable";
    rev = "4762fba469e2baa82f983b262e2c06ac2fdaae67"; # 7-03-2022
    # obtain via `git ls-remote https://github.com/nixos/nixpkgs-channels nixos-unstable`
  };
  pkgs = import nixpkgs { config = {}; };
  pythonCore = pkgs.python38;
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
    ];
  buildInputs = propagatedbuildInputs;
}
