{
  buildPythonApplication,
  hatchling,
  prometheus-client,
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
    ];

  pythonImportsCheck = [ "prometheus_libmanager_exporter" ];

  nativeCheckInputs = [
    pytestCheckHook
  ];
}
