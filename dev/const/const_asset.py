from enum import Enum


class AssetDomains(Enum):
	"""アセットドメイン"""
	Easing = 'easing'
	# 画像
	Image = 'image'
	Texture = Image + '/texture'
	# マテリアル
	Material = 'material'
	MaterialConst = Material + '/const'
	MaterialFunc = Material + '/func'
	# マスター
	Master = 'master'
	MasterApp = 'master/app'
	Const = MasterApp + '/const'


class AssetNames(Enum):
	"""アセットの名前"""
	# マスター
	MFs = 'mfs'
	# マテリアル
	Parameters = 'parameters'
	UIMaster = 'ui_master'


class AssetFormats(Enum):
	"""アセットの書式関連"""
	MasterFilepath = 'Content/{path}.json.data'
	AssetPath = '{domain}/{src}'
	InternalPath = '{domain}#{src}'
	InternalDelimiter = '#'
