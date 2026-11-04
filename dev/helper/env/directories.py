from os import path as os_path


def project_dir() -> str:
	"""Returns: ディレクトリー(ルート)"""
	return os_path.abspath(os_path.join(os_path.dirname(__file__), '../../../'))


def dev_dir() -> str:
	"""Returns: ディレクトリー(dev)"""
	return os_path.join(project_dir(), 'dev')


def cache_dir() -> str:
	"""Returns: ディレクトリー(dev/.cache)"""
	return os_path.join(dev_dir(), '.cache')


def data_dir() -> str:
	"""Returns: ディレクトリー(dev/data)"""
	return os_path.join(dev_dir(), 'data')


def master_dir() -> str:
	"""Returns: ディレクトリー(dev/data/master)"""
	return os_path.join(dev_dir(), 'data', 'master')


def script_dir() -> str:
	"""Returns: ディレクトリー(dev/script)"""
	return os_path.join(dev_dir(), 'script')


def test_dir() -> str:
	"""Returns: ディレクトリー(dev/tests)"""
	return os_path.join(dev_dir(), 'tests')
