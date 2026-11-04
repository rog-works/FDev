from enum import Enum

from tranp.app.compatible.cpp.cvar import CP
from tranp.app.compatible.python.embed import Embed
from UE5.Core.Math.MathFwd import PI
from UE5.Engine.Materials.MaterialExpressionTextureSample import MaterialSamplerType

from App.Editor.Material.MFBuilder import MFBuilder, MFExp
from App.Main.Const.ProjectConst import ClassPrefixs
from App.Main.Core.Lang.Json.Json import Json
from compatible.error import Errors


@Embed.alias(ClassPrefixs.General.value, prefix=True)
class MFBuildCommand:
	"""ビルドコマンド"""

	class Roles(Enum):
		"""コマンド種別"""
		Bool = 0
		Integer = 1
		Number = 2
		String = 3
		Exp = 4
		Function = 5

	data: Json
	role: Roles

	def __init__(self, data: Json, role_is_function: bool = False) -> None:
		"""インスタンスを生成

		Args:
			data: 定義データ
			role_is_function: True = 関数, False = 自動判別
		"""
		self.data = data
		self.role = MFBuildCommand.Roles.Function if role_is_function else MFBuildCommand.analyze_role(data)

	@classmethod
	def analyze_role(cls, data: Json) -> Roles:
		"""Returns: コマンド種別 Note: 関数以外の判別に利用"""
		if data.is_scalar:
			if data.is_bool:
				return cls.Roles.Bool
			elif data.is_int:
				return cls.Roles.Integer
			elif data.is_float:
				return cls.Roles.Number
			else:
				return cls.Roles.String
		else:
			return cls.Roles.Exp

	@property
	def is_scalar(self) -> bool:
		"""Returns: True = スカラー型"""
		return self.data.is_scalar

	@property
	def name(self) -> str:
		"""Returns: 関数名/コマンド名"""
		if self.role == MFBuildCommand.Roles.Function:
			return self.data['name'].as_string
		elif self.role == MFBuildCommand.Roles.Exp:
			return self.data.key_at(0)
		else:
			raise Errors.Never(MFBuildCommand.name, self.data, self.role)

	@property
	def desc(self) -> str:
		"""Returns: コメント(関数)"""
		if self.role != MFBuildCommand.Roles.Function:
			raise Errors.NotAllowed(MFBuildCommand.desc, self.data, self.role)

		return self.data['desc'].as_string

	@property
	def hash(self) -> str:
		"""Returns: ハッシュ(関数)"""
		if self.role != MFBuildCommand.Roles.Function:
			raise Errors.NotAllowed(MFBuildCommand.hash, self.data, self.role)

		return self.data['hash'].as_string

	@property
	def params(self) -> 'list[MFBuildCommand]':
		"""Returns: 仮引数リスト(関数)"""
		if self.role != MFBuildCommand.Roles.Function:
			raise Errors.NotAllowed(MFBuildCommand.params, self.data, self.role)

		return [MFBuildCommand(under) for under in self.data['params'].entries]

	@property
	def statements(self) -> 'list[MFBuildCommand]':
		"""Returns: ステートメントリスト(関数)"""
		if self.role != MFBuildCommand.Roles.Function:
			raise Errors.NotAllowed(MFBuildCommand.statements, self.data, self.role)

		return [MFBuildCommand(under) for under in self.data['statements'].entries]

	@property
	def as_bool(self) -> bool:
		"""Returns: True = 有効"""
		if not self.is_scalar:
			raise Errors.Never(MFBuildCommand.as_bool, self.data, self.role)

		return self.data.as_bool

	@property
	def as_string(self) -> str:
		"""Returns: シンボル名/コメント"""
		if not self.is_scalar:
			raise Errors.Never(MFBuildCommand.as_string, self.data, self.role)

		return self.data.as_string

	@property
	def as_float(self) -> float:
		"""Returns: 定数値"""
		if not self.is_scalar:
			raise Errors.Never(MFBuildCommand.as_float, self.data, self.role)

		if self.role == MFBuildCommand.Roles.String and self.as_string == 'PI':
			return PI
		else:
			return self.data.as_float

	@property
	def as_int(self) -> int:
		"""Returns: 関数の戻り値の使用インデックス"""
		if not self.is_scalar:
			raise Errors.Never(MFBuildCommand.as_int, self.data, self.role)

		return self.data.as_int

	@property
	def args(self) -> 'list[MFBuildCommand]':
		"""Returns: マテリアル関数式の実引数リスト"""
		if self.role != MFBuildCommand.Roles.Exp:
			raise Errors.Never(MFBuildCommand.args, self.data, self.role)

		return [MFBuildCommand(under) for under in self.data.at(0).entries]


@Embed.alias(ClassPrefixs.General.value, prefix=True)
class MFBuildCommandRunner:
	"""ビルドコマンドランナー"""

	@classmethod
	def parse(cls, data: Json) -> dict[str, MFBuildCommand]:
		"""ビルドコマンドをパース

		Returns:
			ビルドコマンド(関数)リスト
		"""
		return {src: MFBuildCommand(data[src], role_is_function=True) for src in data.keys}

	@classmethod
	def run(cls, builder: CP[MFBuilder], func: MFBuildCommand) -> None:
		"""ビルダーに対してコマンドを実行(関数)

		Args:
			builder: マテリアル関数ビルダー
			func: ビルドコマンド(関数)
		"""
		builder.on.clear()
		builder.on.description(func.desc)

		for param in func.params:
			cls.run_command(builder, param)

		for statement in func.statements:
			cls.run_command(builder, statement)

	@classmethod
	def run_command(cls, builder: CP[MFBuilder], command: MFBuildCommand) -> MFExp:
		"""ビルダーに対してコマンドを実行

		Args:
			builder: マテリアル関数ビルダー
			command: ビルドコマンド
		"""
		if command.role == MFBuildCommand.Roles.Bool:
			return builder.on.literal_b(command.as_bool)
		elif command.role == MFBuildCommand.Roles.Number:
			return builder.on.literal_f(command.as_float)
		elif command.role == MFBuildCommand.Roles.String:
			return builder.on.var_ref(command.as_string)

		name = command.name
		args = command.args

		if name == 'get':
			...
		elif name == MFBuilder.var.__name__:
			...
		else:
			...

		if name == MFBuilder.param.__name__:
			return builder.on.param(args[0].as_string, args[1].as_string, cls.run_command(builder, args[2]), args[3].as_string)
		elif name == MFBuilder.returns.__name__:
			return builder.on.returns(args[0].as_string, cls.run_command(builder, args[1]), args[2].as_string)
		elif name == MFBuilder.var.__name__:
			return builder.on.var(args[0].as_string, cls.run_command(builder, args[1]))
		elif name == MFBuilder.vars.__name__:
			return builder.on.vars([args[index].as_string for index in range(len(args) - 1)], cls.run_command(builder, args[len(args) - 1]))
		elif name == 'get':
			return cls.run_command(builder, args[0]).new_index(args[1].as_int)
		elif name == builder.on.ex_bool.__name__:
			return builder.on.ex_bool(symbol=args[0].as_string, group=args[1].as_string, uid=args[2].as_string, value=args[3].as_bool, desc=args[4].as_string)
		elif name == builder.on.ex_float.__name__:
			return builder.on.ex_float(symbol=args[0].as_string, group=args[1].as_string, uid=args[2].as_string, value=args[3].as_float, desc=args[4].as_string, minimum=args[5].as_float, maximum=args[6].as_float)
		elif name == builder.on.ex_float3.__name__:
			return builder.on.ex_float3(symbol=args[0].as_string, group=args[1].as_string, uid=args[2].as_string, x=args[3].as_float, y=args[4].as_float, z=args[5].as_float, desc=args[6].as_string)
		elif name == builder.on.ex_texture.__name__:
			return builder.on.ex_texture(symbol=args[0].as_string, group=args[1].as_string, uid=args[2].as_string, src=args[3].as_string, desc=args[4].as_string, sampler=args[5].as_string if len(args) == 6 else MaterialSamplerType.SAMPLERTYPE_Color.value)
		elif name == 'pi':
			return builder.on.literal_f(PI)
		elif name == 'float2':
			return builder.on.literal_f2(args[0].as_float, args[1].as_float)
		elif name == 'float3':
			return builder.on.literal_f3(args[0].as_float, args[1].as_float, args[2].as_float)
		elif name == 'float4':
			return builder.on.literal_f4(args[0].as_float, args[1].as_float, args[2].as_float, args[3].as_float)
		elif name == MFBuilder.add.__name__:
			values = cls.run_command(builder, args[0]), cls.run_command(builder, args[1])
			return builder.on.add(values[0], values[1])
		elif name == MFBuilder.sub.__name__:
			values = cls.run_command(builder, args[0]), cls.run_command(builder, args[1])
			return builder.on.sub(values[0], values[1])
		elif name == MFBuilder.mul.__name__:
			values = cls.run_command(builder, args[0]), cls.run_command(builder, args[1])
			return builder.on.mul(values[0], values[1])
		elif name == MFBuilder.div.__name__:
			values = cls.run_command(builder, args[0]), cls.run_command(builder, args[1])
			return builder.on.div(values[0], values[1])
		elif name == MFBuilder.mod.__name__:
			values = cls.run_command(builder, args[0]), cls.run_command(builder, args[1])
			return builder.on.mod(values[0], values[1])
		elif name == MFBuilder.one_minus.__name__:
			return builder.on.one_minus(cls.run_command(builder, args[0]))
		elif name == MFBuilder.abs.__name__:
			return builder.on.abs(cls.run_command(builder, args[0]))
		elif name == MFBuilder.clamp.__name__:
			values = cls.run_command(builder, args[0]), cls.run_command(builder, args[1]), cls.run_command(builder, args[2])
			return builder.on.clamp(values[0], values[1], values[2])
		elif name == MFBuilder.cos.__name__:
			return builder.on.cos(cls.run_command(builder, args[0]), args[1].as_float if len(args) == 2 else 1.0)
		elif name == MFBuilder.floor.__name__:
			return builder.on.floor(cls.run_command(builder, args[0]))
		elif name == MFBuilder.length.__name__:
			return builder.on.length(cls.run_command(builder, args[0]))
		elif name == MFBuilder.lerp.__name__:
			values = cls.run_command(builder, args[0]), cls.run_command(builder, args[1]), cls.run_command(builder, args[2])
			return builder.on.lerp(values[0], values[1], values[2])
		elif name == MFBuilder.max.__name__:
			values = cls.run_command(builder, args[0]), cls.run_command(builder, args[1])
			return builder.on.max(values[0], values[1])
		elif name == MFBuilder.min.__name__:
			values = cls.run_command(builder, args[0]), cls.run_command(builder, args[1])
			return builder.on.min(values[0], values[1])
		elif name == MFBuilder.power.__name__:
			values = cls.run_command(builder, args[0]), cls.run_command(builder, args[1])
			return builder.on.power(values[0], values[1])
		elif name == MFBuilder.sin.__name__:
			return builder.on.sin(cls.run_command(builder, args[0]), args[1].as_float if len(args) == 2 else 1.0)
		elif name == MFBuilder.smoothstep.__name__:
			values = cls.run_command(builder, args[0]), cls.run_command(builder, args[1]), cls.run_command(builder, args[2])
			return builder.on.smoothstep(values[0], values[1], values[2])
		elif name == MFBuilder.step.__name__:
			values = cls.run_command(builder, args[0]), cls.run_command(builder, args[1])
			return builder.on.step(values[0], values[1])
		elif name == MFBuilder.tan.__name__:
			return builder.on.tan(cls.run_command(builder, args[0]), args[1].as_float if len(args) == 2 else 1.0)
		elif name == MFBuilder.saturate.__name__:
			return builder.on.saturate(cls.run_command(builder, args[0]))
		elif name == MFBuilder.append.__name__:
			values = cls.run_command(builder, args[0]), cls.run_command(builder, args[1])
			return builder.on.append(values[0], values[1])
		elif name == MFBuilder.cross.__name__:
			values = cls.run_command(builder, args[0]), cls.run_command(builder, args[1])
			return builder.on.cross(values[0], values[1])
		elif name == MFBuilder.dot.__name__:
			values = cls.run_command(builder, args[0]), cls.run_command(builder, args[1])
			return builder.on.dot(values[0], values[1])
		elif name == MFBuilder.make_float2.__name__:
			values = cls.run_command(builder, args[0]), cls.run_command(builder, args[1])
			return builder.on.make_float2(values[0], values[1])
		elif name == MFBuilder.make_float3.__name__:
			values = cls.run_command(builder, args[0]), cls.run_command(builder, args[1]), cls.run_command(builder, args[2])
			return builder.on.make_float3(values[0], values[1], values[2])
		elif name == MFBuilder.make_float4.__name__:
			values = cls.run_command(builder, args[0]), cls.run_command(builder, args[1]), cls.run_command(builder, args[2]), cls.run_command(builder, args[3])
			return builder.on.make_float4(values[0], values[1], values[2], values[3])
		elif name == MFBuilder.mask.__name__:
			return builder.on.mask(cls.run_command(builder, args[0]), args[1].as_string)
		elif name == MFBuilder.normalize.__name__:
			return builder.on.normalize(cls.run_command(builder, args[0]))
		elif name == MFBuilder.rgb_to_hsv.__name__:
			return builder.on.rgb_to_hsv(cls.run_command(builder, args[0]))
		elif name == MFBuilder.hsv_to_rgb.__name__:
			return builder.on.hsv_to_rgb(cls.run_command(builder, args[0]))
		elif name == MFBuilder.panner.__name__:
			values = cls.run_command(builder, args[0]), cls.run_command(builder, args[1])
			return builder.on.panner(values[0], values[1])
		elif name == MFBuilder.tex_coord.__name__:
			return builder.on.tex_coord(args[0].as_int)
		elif name == MFBuilder.texture.__name__:
			return builder.on.texture(args[0].as_string, args[1].as_string if len(args) == 2 else MaterialSamplerType.SAMPLERTYPE_Color.value)
		elif name == MFBuilder.time.__name__:
			return builder.on.time()
		elif name == MFBuilder.sample.__name__:
			values = cls.run_command(builder, args[0]), cls.run_command(builder, args[1])
			return builder.on.sample(values[0], values[1], args[2].as_string if len(args) == 3 else MaterialSamplerType.SAMPLERTYPE_Color.value)
		elif name == MFBuilder.ddx.__name__:
			return builder.on.ddx(cls.run_command(builder, args[0]))
		elif name == MFBuilder.ddy.__name__:
			return builder.on.ddy(cls.run_command(builder, args[0]))
		elif name == MFBuilder.const_by.__name__:
			return builder.on.const_by(args[0].as_string)
		elif name == MFBuilder.ternary.__name__:
			values = cls.run_command(builder, args[0]), cls.run_command(builder, args[1]), cls.run_command(builder, args[2])
			return builder.on.ternary(values[0], values[1], values[2])
		else:
			return builder.on.call(name, [cls.run_command(builder, args[index]) for index in range(len(args))])
