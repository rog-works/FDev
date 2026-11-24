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
	MaterialMaterial = Material + '/material'
	# マスター
	Master = 'master'
	MasterApp = 'master/app'
	Const = MasterApp + '/const'


class AssetNames(Enum):
	"""アセットの名前"""
	# マスター
	MFs = 'mfs'
	MIs = 'mis'
	# マテリアル
	Parameters = 'parameters'


class AssetSrcs(Enum):
	"""アセットソースパス"""
	# マテリアル
	UIMaster = 'material/ui/ui_master'
	UIMasterAdd = 'material/ui/ui_master_add'


class AssetFormats(Enum):
	"""アセットの書式関連"""
	MasterFilepath = 'Content/{path}.json.data'
	AssetPath = '{domain}/{src}'
	InternalPath = '{domain}#{src}'
	InternalDelimiter = '#'
