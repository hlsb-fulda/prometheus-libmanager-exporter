{
  buildPythonApplication,
  hatchling,
  prometheus-client,
  click,
  beautifulsoup4,
  requests,
  structlog,
  pytestCheckHook,
  ...
}:

buildPythonApplication {
  pname = "prometheus-libmanager-exporter";
  version = "0.1.0";

  src = ./.;

  pyproject = true;
  build-system = [ hatchling ];

  dependencies =
    [
      prometheus-client
      click
      beautifulsoup4
      requests
      structlog
    ];

  pythonImportsCheck = [ "prometheus_libmanager_exporter" ];

  doCheck = false;

  nativeCheckInputs = [
    pytestCheckHook
  ];
}
