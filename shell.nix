{ pkgs ? import <nixpkgs> { } }:

let
  packages = p: with p; (
    let
      pypika-tortoise = buildPythonPackage rec {
        pname = "pypika-tortoise";
        version = "0.1.6";
        format = "pyproject";

        src = fetchPypi {
          inherit pname version;
          sha256 = "sha256-2AKGj0eacI4yY3JMe1cZomrXk5mypwzqBl9KTK2+vzY";
        };

        doCheck = false;

        nativeBuildInputs = [ poetry-core ];

        postFixup = ''
          rm $out/lib/${python.libPrefix}/site-packages/{README.md,CHANGELOG.md}
        '';
      };
      aiosqlite-17 = buildPythonPackage rec {
        pname = "aiosqlite";
        version = "0.17.0";

        src = fetchPypi {
          inherit pname version;
          sha256 = "sha256-8OaswkvEhkFJJnrIL7Rt+zvkRV+Z/iHfgmCcxua67lE=";
        };

        doCheck = false;

        propagatedBuildInputs = [ typing-extensions ];
      };
    in
    [
      discordpy
      pyyaml
      requests
      babel
      matplotlib
      (
        buildPythonPackage rec {
          pname = "tortoise-orm";
          version = "0.19.3";
          format = "wheel";

          src = pkgs.fetchurl {
            url = "https://files.pythonhosted.org/packages/58/cf/286eb8997113dd04a61c430b5a0d3b2aef9ee51031440d18357bf21740a9/tortoise_orm-0.19.3-py3-none-any.whl";
            sha256 = "9e368820c70a0866ef9c521d43aa5503485bd7a20a561edc0933b7b0f7036fbc";
          };

          doCheck = false;

          propagatedBuildInputs = [ poetry-core iso8601 pytz aiosqlite-17 asyncpg aiomysql asyncmy pypika-tortoise ];
        }
      )
    ]
  );
  python-with-my-packages = pkgs.python310.withPackages packages;
in
pkgs.mkShell {
  buildInputs = with pkgs; [
    python-with-my-packages
  ];
}
