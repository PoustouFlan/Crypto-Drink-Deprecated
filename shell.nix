with (import <nixpkgs> {});
let
  packages = p: with p; [
    discordpy
    pyyaml
    requests
  ];
  python-with-my-packages = python310.withPackages packages;
in
mkShell {
  buildInputs = [
    python-with-my-packages
  ];
}
