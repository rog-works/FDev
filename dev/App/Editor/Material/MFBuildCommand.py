from enum import Enum
from typing import Annotated

from tranp.app.compatible.cpp.cvar import CP
from tranp.app.compatible.cpp.function import c_func_ref
from tranp.app.compatible.python.embed import Embed
from UE5.Core.Math.MathFwd import PI
from UE5.Engine.Materials.MaterialExpressionTextureSample import MaterialSamplerType

from App.Editor.Material.MFBuilder import MFBuilder, MFExp
from App.Main.Core.Lang.Json.Json import Json
from App.Main.Core.Logs import Logs
from compatible.error import Errors


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

	def __init__(self, data: Json) -> None:
		"""インスタンスを生成

		Args:
			data: 定義データ
		"""
		self.data = data
		self.role = MFBuildCommand.analyze_role(data)

	@classmethod
	def analyze_role(cls, data: Json) -> Roles:
		"""Returns: コマンド種別"""
		if data.is_scalar:
			if data.is_bool:
				return cls.Roles.Bool
			elif data.is_int:
				return cls.Roles.Integer
			elif data.is_float:
				return cls.Roles.Number
			else:
				return cls.Roles.String
		elif data.has_key('statements'):
			return cls.Roles.Function
		else:
			return cls.Roles.Exp

	@property
	def hash(self) -> Annotated[str, Embed.immutable]:
		"""Returns: ハッシュ(関数) @immutable"""
		if self.role != MFBuildCommand.Roles.Function:
			raise Errors.NotAllowed(MFBuildCommand.hash, self.data, self.role)

		return self.data['hash'].as_string

	# region 関数

	@property
	def desc(self) -> Annotated[str, Embed.immutable]:
		"""Returns: コメント(関数) @immutable"""
		if self.role != MFBuildCommand.Roles.Function:
			raise Errors.NotAllowed(MFBuildCommand.desc, self.data, self.role)

		return self.data['desc'].as_string

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
	def output(self) -> Json:
		"""Returns: 出力(JSON)"""
		if self.role != MFBuildCommand.Roles.Function:
			raise Errors.NotAllowed(MFBuildCommand.desc, self.data, self.role)

		return self.data['output']

	# endregion
	# region 名前

	@property
	def name(self) -> str:
		"""Returns: 関数名/コマンド名"""
		if self.role == MFBuildCommand.Roles.Function:
			return self.data['name'].as_string
		elif self.role == MFBuildCommand.Roles.Exp:
			return self.data.key_at(0)
		else:
			raise Errors.Never(MFBuildCommand.name, self.data, self.role)

	# endregion
	# region 値

	@property
	def as_bool(self) -> bool:
		"""Returns: True = 有効"""
		if not self.data.is_bool:
			raise Errors.Never(MFBuildCommand.as_bool, self.data, self.role)

		return self.data.as_bool

	@property
	def as_string(self) -> Annotated[str, Embed.immutable]:
		"""Returns: シンボル名/コメント @immutable"""
		if not self.data.is_string:
			raise Errors.Never(MFBuildCommand.as_string, self.data, self.role)

		return self.data.as_string

	@property
	def as_float(self) -> float:
		"""Returns: 定数値"""
		if not self.data.is_float:
			raise Errors.Never(MFBuildCommand.as_float, self.data, self.role)

		return self.data.as_float

	@property
	def as_int(self) -> int:
		"""Returns: 関数の戻り値の使用インデックス"""
		if not self.data.is_int:
			raise Errors.Never(MFBuildCommand.as_int, self.data, self.role)

		return self.data.as_int

	# endregion
	# region 引数

	@property
	def arg_num(self) -> int:
		"""Returns: マテリアル関数式の実引数の数"""
		if self.role != MFBuildCommand.Roles.Exp:
			raise Errors.Never(MFBuildCommand.arg_num, self.data, self.role)

		return self.data.at(0).length

	def arg_at(self, index: int) -> 'MFBuildCommand':
		"""Returns: マテリアル関数式の実引数"""
		if self.role != MFBuildCommand.Roles.Exp:
			raise Errors.Never(MFBuildCommand.arg_at, self.data, self.role)

		return MFBuildCommand(self.data.at(0).at(index))

	# endregion


class MFBuildCommandRunner:
	"""ビルドコマンドランナー"""

	@classmethod
	def parse(cls, data: Json) -> dict[str, MFBuildCommand]:
		"""ビルドコマンドをパース

		Returns:
			ビルドコマンドリスト(関数/マテリアル)
		"""
		return {src: MFBuildCommand(data[src]) for src in data.keys}

	@classmethod
	def build_mf(cls, builder: CP[MFBuilder], entry: MFBuildCommand) -> None:
		"""アセットを構築(マテリアル関数)

		Args:
			builder: マテリアル関数ビルダー
			entry: ビルドコマンド(関数)
		"""
		builder.on.clear()
		builder.on.description(entry.desc)

		for param in entry.params:
			cls.__emit_command(builder, param)

		for statement in entry.statements:
			cls.__emit_command(builder, statement)

	@classmethod
	def build_material(cls, builder: CP[MFBuilder], entry: MFBuildCommand) -> None:
		"""アセットを構築(マテリアル)

		Args:
			builder: マテリアル関数ビルダー
			entry: ビルドコマンド(マテリアル)
		"""
		builder.on.clear()
		for statement in entry.statements:
			cls.__emit_command(builder, statement)

		builder.on.rebuild_material()

	@classmethod
	def __emit_command(cls, builder: CP[MFBuilder], command: MFBuildCommand) -> MFExp:
		"""ビルダーに対してコマンドを実行

		Args:
			builder: マテリアル関数ビルダー
			command: ビルドコマンド
		Returns:
			式
		"""
		cls.__debug_log(command)
		if command.role == MFBuildCommand.Roles.Bool:
			return cls.on_bool(builder, command)
		elif command.role == MFBuildCommand.Roles.Number:
			return cls.on_float(builder, command)
		elif command.role == MFBuildCommand.Roles.String:
			return cls.on_var_ref(builder, command)
		elif command.name == 'get':
			return cls.on_get(builder, command)
		else:
			return cls.__emit_exp(builder, command)

	@classmethod
	def __emit_exp(cls, builder: CP[MFBuilder], command: MFBuildCommand) -> MFExp:
		"""式コマンドを実行

		Args:
			builder: マテリアル関数ビルダー
			command: ビルドコマンド
		Returns:
			式
		Note:
			XXX on_bool/on_float/on_get/on_callは特殊化によりhandlersに含まれない
		"""
		handlers = Embed.static(cls.__emit_exp).decl(lambda: {
			str(cls.on_param.__name__)[3:]: c_func_ref(cls.on_param),
			str(cls.on_returns.__name__)[3:]: c_func_ref(cls.on_returns),
			str(cls.on_schema_domain.__name__)[3:]: c_func_ref(cls.on_schema_domain),
			str(cls.on_schema_blend.__name__)[3:]: c_func_ref(cls.on_schema_blend),
			str(cls.on_schema_shading.__name__)[3:]: c_func_ref(cls.on_schema_shading),
			str(cls.on_schema_option.__name__)[3:]: c_func_ref(cls.on_schema_option),
			str(cls.on_output_emissive_color.__name__)[3:]: c_func_ref(cls.on_output_emissive_color),
			str(cls.on_output_opacity.__name__)[3:]: c_func_ref(cls.on_output_opacity),
			str(cls.on_var.__name__)[3:]: c_func_ref(cls.on_var),
			str(cls.on_vars.__name__)[3:]: c_func_ref(cls.on_vars),
			str(cls.on_ex_bool.__name__)[3:]: c_func_ref(cls.on_ex_bool),
			str(cls.on_ex_float.__name__)[3:]: c_func_ref(cls.on_ex_float),
			str(cls.on_ex_float3.__name__)[3:]: c_func_ref(cls.on_ex_float3),
			str(cls.on_ex_texture.__name__)[3:]: c_func_ref(cls.on_ex_texture),
			str(cls.on_pi.__name__)[3:]: c_func_ref(cls.on_pi),
			str(cls.on_float2.__name__)[3:]: c_func_ref(cls.on_float2),
			str(cls.on_float3.__name__)[3:]: c_func_ref(cls.on_float3),
			str(cls.on_float4.__name__)[3:]: c_func_ref(cls.on_float4),
			str(cls.on_add.__name__)[3:]: c_func_ref(cls.on_add),
			str(cls.on_sub.__name__)[3:]: c_func_ref(cls.on_sub),
			str(cls.on_mul.__name__)[3:]: c_func_ref(cls.on_mul),
			str(cls.on_div.__name__)[3:]: c_func_ref(cls.on_div),
			str(cls.on_mod.__name__)[3:]: c_func_ref(cls.on_mod),
			str(cls.on_one_minus.__name__)[3:]: c_func_ref(cls.on_one_minus),
			str(cls.on_abs.__name__)[3:]: c_func_ref(cls.on_abs),
			str(cls.on_power.__name__)[3:]: c_func_ref(cls.on_power),
			str(cls.on_step.__name__)[3:]: c_func_ref(cls.on_step),
			str(cls.on_lerp.__name__)[3:]: c_func_ref(cls.on_lerp),
			str(cls.on_smoothstep.__name__)[3:]: c_func_ref(cls.on_smoothstep),
			str(cls.on_clamp.__name__)[3:]: c_func_ref(cls.on_clamp),
			str(cls.on_floor.__name__)[3:]: c_func_ref(cls.on_floor),
			str(cls.on_max.__name__)[3:]: c_func_ref(cls.on_max),
			str(cls.on_min.__name__)[3:]: c_func_ref(cls.on_min),
			str(cls.on_saturate.__name__)[3:]: c_func_ref(cls.on_saturate),
			str(cls.on_cos.__name__)[3:]: c_func_ref(cls.on_cos),
			str(cls.on_sin.__name__)[3:]: c_func_ref(cls.on_sin),
			str(cls.on_tan.__name__)[3:]: c_func_ref(cls.on_tan),
			str(cls.on_cross.__name__)[3:]: c_func_ref(cls.on_cross),
			str(cls.on_dot.__name__)[3:]: c_func_ref(cls.on_dot),
			str(cls.on_length.__name__)[3:]: c_func_ref(cls.on_length),
			str(cls.on_normalize.__name__)[3:]: c_func_ref(cls.on_normalize),
			str(cls.on_append.__name__)[3:]: c_func_ref(cls.on_append),
			str(cls.on_make_float2.__name__)[3:]: c_func_ref(cls.on_make_float2),
			str(cls.on_make_float3.__name__)[3:]: c_func_ref(cls.on_make_float3),
			str(cls.on_make_float4.__name__)[3:]: c_func_ref(cls.on_make_float4),
			str(cls.on_mask.__name__)[3:]: c_func_ref(cls.on_mask),
			str(cls.on_rgb_to_hsv.__name__)[3:]: c_func_ref(cls.on_rgb_to_hsv),
			str(cls.on_hsv_to_rgb.__name__)[3:]: c_func_ref(cls.on_hsv_to_rgb),
			str(cls.on_panner.__name__)[3:]: c_func_ref(cls.on_panner),
			str(cls.on_tex_coord.__name__)[3:]: c_func_ref(cls.on_tex_coord),
			str(cls.on_texture.__name__)[3:]: c_func_ref(cls.on_texture),
			str(cls.on_sample.__name__)[3:]: c_func_ref(cls.on_sample),
			str(cls.on_ddx.__name__)[3:]: c_func_ref(cls.on_ddx),
			str(cls.on_ddy.__name__)[3:]: c_func_ref(cls.on_ddy),
			str(cls.on_const_by.__name__)[3:]: c_func_ref(cls.on_const_by),
			str(cls.on_time.__name__)[3:]: c_func_ref(cls.on_time),
			str(cls.on_ternary.__name__)[3:]: c_func_ref(cls.on_ternary),
		})
		if command.name in handlers:
			return handlers[command.name](builder, command)
		else:
			return cls.on_call(builder, command)

	@classmethod
	def __debug_log(cls, command: MFBuildCommand) -> None:
		"""デバッグログを出力

		Args:
			command: ビルドコマンド
		"""
		if command.role == MFBuildCommand.Roles.Bool:
			...
		elif command.role == MFBuildCommand.Roles.Number:
			...
		elif command.role == MFBuildCommand.Roles.String:
			Logs.asset(MFBuildCommandRunner.__emit_command, 'command: var_ref, name: {name}'.format(name=command.as_string))
		elif command.name == 'get':
			Logs.asset(MFBuildCommandRunner.__emit_command, 'command: {name}, args: {num}, output: {output}'.format(name=command.name, num=command.arg_num, output=command.arg_at(1).as_int))
		elif command.name == MFBuilder.var.__name__:
			Logs.asset(MFBuildCommandRunner.__emit_command, 'command: {name}, args: {num}, var: {var}'.format(name=command.name, num=command.arg_num, var=command.arg_at(0).as_string))
		else:
			Logs.asset(MFBuildCommandRunner.__emit_command, 'command: {name}, args: {num}'.format(name=command.name, num=command.arg_num))

	# region インデクサー

	@classmethod
	def on_get(cls, builder: CP[MFBuilder], command: MFBuildCommand) -> MFExp:
		return cls.__emit_command(builder, command.arg_at(0)).new_index(command.arg_at(1).as_int)

	# endregion
	# region 関数シグネチャー

	@classmethod
	def on_param(cls, builder: CP[MFBuilder], command: MFBuildCommand) -> MFExp:
		return builder.on.param(command.arg_at(0).as_string, command.arg_at(1).as_string, cls.__emit_command(builder, command.arg_at(2)), command.arg_at(3).as_string)

	@classmethod
	def on_returns(cls, builder: CP[MFBuilder], command: MFBuildCommand) -> MFExp:
		return builder.on.returns(command.arg_at(0).as_string, cls.__emit_command(builder, command.arg_at(1)), command.arg_at(2).as_string)

	# endregion
	# region マテリアル/スキーマ

	@classmethod
	def on_schema_domain(cls, builder: CP[MFBuilder], command: MFBuildCommand) -> MFExp:
		builder.on.schema_domain(command.arg_at(0).as_string)
		return MFExp.empty()

	@classmethod
	def on_schema_blend(cls, builder: CP[MFBuilder], command: MFBuildCommand) -> MFExp:
		builder.on.schema_blend(command.arg_at(0).as_string)
		return MFExp.empty()

	@classmethod
	def on_schema_shading(cls, builder: CP[MFBuilder], command: MFBuildCommand) -> MFExp:
		builder.on.schema_shading(command.arg_at(0).as_string)
		return MFExp.empty()

	@classmethod
	def on_schema_option(cls, builder: CP[MFBuilder], command: MFBuildCommand) -> MFExp:
		builder.on.schema_option(command.arg_at(0).as_string)
		return MFExp.empty()

	# endregion
	# region マテリアル/出力

	@classmethod
	def on_output_emissive_color(cls, builder: CP[MFBuilder], command: MFBuildCommand) -> MFExp:
		builder.on.output_emissive_color(cls.__emit_command(builder, command.arg_at(0)))
		return MFExp.empty()

	@classmethod
	def on_output_opacity(cls, builder: CP[MFBuilder], command: MFBuildCommand) -> MFExp:
		builder.on.output_opacity(cls.__emit_command(builder, command.arg_at(0)))
		return MFExp.empty()

	# endregion
	# region 変数

	@classmethod
	def on_var(cls, builder: CP[MFBuilder], command: MFBuildCommand) -> MFExp:
		return builder.on.var(command.arg_at(0).as_string, cls.__emit_command(builder, command.arg_at(1)))

	@classmethod
	def on_vars(cls, builder: CP[MFBuilder], command: MFBuildCommand) -> MFExp:
		return builder.on.vars([command.arg_at(index).as_string for index in range(command.arg_num - 1)], cls.__emit_command(builder, command.arg_at(command.arg_num - 1)))

	@classmethod
	def on_var_ref(cls, builder: CP[MFBuilder], command: MFBuildCommand) -> MFExp:
		return builder.on.var_ref(command.as_string)

	# endregion
	# region 公開パラメーター

	@classmethod
	def on_ex_bool(cls, builder: CP[MFBuilder], command: MFBuildCommand) -> MFExp:
		return builder.on.ex_bool(symbol=command.arg_at(0).as_string, group=command.arg_at(1).as_string, uid=command.arg_at(2).as_string, value=command.arg_at(3).as_bool, desc=command.arg_at(4).as_string)

	@classmethod
	def on_ex_float(cls, builder: CP[MFBuilder], command: MFBuildCommand) -> MFExp:
		return builder.on.ex_float(symbol=command.arg_at(0).as_string, group=command.arg_at(1).as_string, uid=command.arg_at(2).as_string, value=command.arg_at(3).as_float, desc=command.arg_at(4).as_string, minimum=command.arg_at(5).as_float, maximum=command.arg_at(6).as_float)

	@classmethod
	def on_ex_float3(cls, builder: CP[MFBuilder], command: MFBuildCommand) -> MFExp:
		return builder.on.ex_float3(symbol=command.arg_at(0).as_string, group=command.arg_at(1).as_string, uid=command.arg_at(2).as_string, x=command.arg_at(3).as_float, y=command.arg_at(4).as_float, z=command.arg_at(5).as_float, desc=command.arg_at(6).as_string)

	@classmethod
	def on_ex_texture(cls, builder: CP[MFBuilder], command: MFBuildCommand) -> MFExp:
		return builder.on.ex_texture(symbol=command.arg_at(0).as_string, group=command.arg_at(1).as_string, uid=command.arg_at(2).as_string, src=command.arg_at(3).as_string, desc=command.arg_at(4).as_string, sampler=command.arg_at(5).as_string if command.arg_num == 6 else MaterialSamplerType.SAMPLERTYPE_Color.value)

	# endregion
	# region リテラル

	@classmethod
	def on_pi(cls, builder: CP[MFBuilder], command: MFBuildCommand) -> MFExp:
		return builder.on.literal_f(PI)

	@classmethod
	def on_bool(cls, builder: CP[MFBuilder], command: MFBuildCommand) -> MFExp:
		return builder.on.literal_b(command.as_bool)

	@classmethod
	def on_float(cls, builder: CP[MFBuilder], command: MFBuildCommand) -> MFExp:
		return builder.on.literal_f(command.as_float)

	@classmethod
	def on_float2(cls, builder: CP[MFBuilder], command: MFBuildCommand) -> MFExp:
		return builder.on.literal_f2(command.arg_at(0).as_float, command.arg_at(1).as_float)

	@classmethod
	def on_float3(cls, builder: CP[MFBuilder], command: MFBuildCommand) -> MFExp:
		return builder.on.literal_f3(command.arg_at(0).as_float, command.arg_at(1).as_float, command.arg_at(2).as_float)

	@classmethod
	def on_float4(cls, builder: CP[MFBuilder], command: MFBuildCommand) -> MFExp:
		return builder.on.literal_f4(command.arg_at(0).as_float, command.arg_at(1).as_float, command.arg_at(2).as_float, command.arg_at(3).as_float)

	# endregion
	# region 四則演算

	@classmethod
	def on_add(cls, builder: CP[MFBuilder], command: MFBuildCommand) -> MFExp:
		values = cls.__emit_command(builder, command.arg_at(0)), cls.__emit_command(builder, command.arg_at(1))
		return builder.on.add(values[0], values[1])

	@classmethod
	def on_sub(cls, builder: CP[MFBuilder], command: MFBuildCommand) -> MFExp:
		values = cls.__emit_command(builder, command.arg_at(0)), cls.__emit_command(builder, command.arg_at(1))
		return builder.on.sub(values[0], values[1])

	@classmethod
	def on_mul(cls, builder: CP[MFBuilder], command: MFBuildCommand) -> MFExp:
		values = cls.__emit_command(builder, command.arg_at(0)), cls.__emit_command(builder, command.arg_at(1))
		return builder.on.mul(values[0], values[1])

	@classmethod
	def on_div(cls, builder: CP[MFBuilder], command: MFBuildCommand) -> MFExp:
		values = cls.__emit_command(builder, command.arg_at(0)), cls.__emit_command(builder, command.arg_at(1))
		return builder.on.div(values[0], values[1])

	@classmethod
	def on_mod(cls, builder: CP[MFBuilder], command: MFBuildCommand) -> MFExp:
		values = cls.__emit_command(builder, command.arg_at(0)), cls.__emit_command(builder, command.arg_at(1))
		return builder.on.mod(values[0], values[1])

	@classmethod
	def on_one_minus(cls, builder: CP[MFBuilder], command: MFBuildCommand) -> MFExp:
		return builder.on.one_minus(cls.__emit_command(builder, command.arg_at(0)))

	# endregion
	# region 算術演算

	@classmethod
	def on_abs(cls, builder: CP[MFBuilder], command: MFBuildCommand) -> MFExp:
		return builder.on.abs(cls.__emit_command(builder, command.arg_at(0)))

	@classmethod
	def on_power(cls, builder: CP[MFBuilder], command: MFBuildCommand) -> MFExp:
		values = cls.__emit_command(builder, command.arg_at(0)), cls.__emit_command(builder, command.arg_at(1))
		return builder.on.power(values[0], values[1])

	@classmethod
	def on_step(cls, builder: CP[MFBuilder], command: MFBuildCommand) -> MFExp:
		values = cls.__emit_command(builder, command.arg_at(0)), cls.__emit_command(builder, command.arg_at(1))
		return builder.on.step(values[0], values[1])

	# endregion
	# region 線形補完

	@classmethod
	def on_lerp(cls, builder: CP[MFBuilder], command: MFBuildCommand) -> MFExp:
		values = cls.__emit_command(builder, command.arg_at(0)), cls.__emit_command(builder, command.arg_at(1)), cls.__emit_command(builder, command.arg_at(2))
		return builder.on.lerp(values[0], values[1], values[2])

	@classmethod
	def on_smoothstep(cls, builder: CP[MFBuilder], command: MFBuildCommand) -> MFExp:
		values = cls.__emit_command(builder, command.arg_at(0)), cls.__emit_command(builder, command.arg_at(1)), cls.__emit_command(builder, command.arg_at(2))
		return builder.on.smoothstep(values[0], values[1], values[2])

	# endregion
	# region 丸め込み

	@classmethod
	def on_clamp(cls, builder: CP[MFBuilder], command: MFBuildCommand) -> MFExp:
		values = cls.__emit_command(builder, command.arg_at(0)), cls.__emit_command(builder, command.arg_at(1)), cls.__emit_command(builder, command.arg_at(2))
		return builder.on.clamp(values[0], values[1], values[2])

	@classmethod
	def on_floor(cls, builder: CP[MFBuilder], command: MFBuildCommand) -> MFExp:
		return builder.on.floor(cls.__emit_command(builder, command.arg_at(0)))

	@classmethod
	def on_max(cls, builder: CP[MFBuilder], command: MFBuildCommand) -> MFExp:
		values = cls.__emit_command(builder, command.arg_at(0)), cls.__emit_command(builder, command.arg_at(1))
		return builder.on.max(values[0], values[1])

	@classmethod
	def on_min(cls, builder: CP[MFBuilder], command: MFBuildCommand) -> MFExp:
		values = cls.__emit_command(builder, command.arg_at(0)), cls.__emit_command(builder, command.arg_at(1))
		return builder.on.min(values[0], values[1])

	@classmethod
	def on_saturate(cls, builder: CP[MFBuilder], command: MFBuildCommand) -> MFExp:
		return builder.on.saturate(cls.__emit_command(builder, command.arg_at(0)))

	# endregion
	# region 三角関数

	@classmethod
	def on_cos(cls, builder: CP[MFBuilder], command: MFBuildCommand) -> MFExp:
		return builder.on.cos(cls.__emit_command(builder, command.arg_at(0)), command.arg_at(1).as_float if command.arg_num == 2 else 1.0)

	@classmethod
	def on_sin(cls, builder: CP[MFBuilder], command: MFBuildCommand) -> MFExp:
		return builder.on.sin(cls.__emit_command(builder, command.arg_at(0)), command.arg_at(1).as_float if command.arg_num == 2 else 1.0)

	@classmethod
	def on_tan(cls, builder: CP[MFBuilder], command: MFBuildCommand) -> MFExp:
		return builder.on.tan(cls.__emit_command(builder, command.arg_at(0)), command.arg_at(1).as_float if command.arg_num == 2 else 1.0)

	# endregion
	# region ベクトル演算

	@classmethod
	def on_cross(cls, builder: CP[MFBuilder], command: MFBuildCommand) -> MFExp:
		values = cls.__emit_command(builder, command.arg_at(0)), cls.__emit_command(builder, command.arg_at(1))
		return builder.on.cross(values[0], values[1])

	@classmethod
	def on_dot(cls, builder: CP[MFBuilder], command: MFBuildCommand) -> MFExp:
		values = cls.__emit_command(builder, command.arg_at(0)), cls.__emit_command(builder, command.arg_at(1))
		return builder.on.dot(values[0], values[1])

	@classmethod
	def on_length(cls, builder: CP[MFBuilder], command: MFBuildCommand) -> MFExp:
		return builder.on.length(cls.__emit_command(builder, command.arg_at(0)))

	@classmethod
	def on_normalize(cls, builder: CP[MFBuilder], command: MFBuildCommand) -> MFExp:
		return builder.on.normalize(cls.__emit_command(builder, command.arg_at(0)))

	# endregion
	# region ベクトル操作

	@classmethod
	def on_append(cls, builder: CP[MFBuilder], command: MFBuildCommand) -> MFExp:
		values = cls.__emit_command(builder, command.arg_at(0)), cls.__emit_command(builder, command.arg_at(1))
		return builder.on.append(values[0], values[1])

	@classmethod
	def on_make_float2(cls, builder: CP[MFBuilder], command: MFBuildCommand) -> MFExp:
		values = cls.__emit_command(builder, command.arg_at(0)), cls.__emit_command(builder, command.arg_at(1))
		return builder.on.make_float2(values[0], values[1])

	@classmethod
	def on_make_float3(cls, builder: CP[MFBuilder], command: MFBuildCommand) -> MFExp:
		values = cls.__emit_command(builder, command.arg_at(0)), cls.__emit_command(builder, command.arg_at(1)), cls.__emit_command(builder, command.arg_at(2))
		return builder.on.make_float3(values[0], values[1], values[2])

	@classmethod
	def on_make_float4(cls, builder: CP[MFBuilder], command: MFBuildCommand) -> MFExp:
		values = cls.__emit_command(builder, command.arg_at(0)), cls.__emit_command(builder, command.arg_at(1)), cls.__emit_command(builder, command.arg_at(2)), cls.__emit_command(builder, command.arg_at(3))
		return builder.on.make_float4(values[0], values[1], values[2], values[3])

	@classmethod
	def on_mask(cls, builder: CP[MFBuilder], command: MFBuildCommand) -> MFExp:
		return builder.on.mask(cls.__emit_command(builder, command.arg_at(0)), command.arg_at(1).as_string)

	# endregion
	# region カラー操作

	@classmethod
	def on_rgb_to_hsv(cls, builder: CP[MFBuilder], command: MFBuildCommand) -> MFExp:
		return builder.on.rgb_to_hsv(cls.__emit_command(builder, command.arg_at(0)))

	@classmethod
	def on_hsv_to_rgb(cls, builder: CP[MFBuilder], command: MFBuildCommand) -> MFExp:
		return builder.on.hsv_to_rgb(cls.__emit_command(builder, command.arg_at(0)))

	# endregion
	# region テクスチャー操作

	@classmethod
	def on_panner(cls, builder: CP[MFBuilder], command: MFBuildCommand) -> MFExp:
		values = cls.__emit_command(builder, command.arg_at(0)), cls.__emit_command(builder, command.arg_at(1))
		return builder.on.panner(values[0], values[1])

	@classmethod
	def on_tex_coord(cls, builder: CP[MFBuilder], command: MFBuildCommand) -> MFExp:
		return builder.on.tex_coord(command.arg_at(0).as_int)

	@classmethod
	def on_texture(cls, builder: CP[MFBuilder], command: MFBuildCommand) -> MFExp:
		return builder.on.texture(command.arg_at(0).as_string, command.arg_at(1).as_string if command.arg_num == 2 else MaterialSamplerType.SAMPLERTYPE_Color.value)

	@classmethod
	def on_sample(cls, builder: CP[MFBuilder], command: MFBuildCommand) -> MFExp:
		values = cls.__emit_command(builder, command.arg_at(0)), cls.__emit_command(builder, command.arg_at(1))
		return builder.on.sample(values[0], values[1], command.arg_at(2).as_string if command.arg_num == 3 else MaterialSamplerType.SAMPLERTYPE_Color.value)

	# endregion
	# region ピクセルシェーダー

	@classmethod
	def on_ddx(cls, builder: CP[MFBuilder], command: MFBuildCommand) -> MFExp:
		return builder.on.ddx(cls.__emit_command(builder, command.arg_at(0)))

	@classmethod
	def on_ddy(cls, builder: CP[MFBuilder], command: MFBuildCommand) -> MFExp:
		return builder.on.ddy(cls.__emit_command(builder, command.arg_at(0)))

	# endregion
	# region パラメーターコレクション

	@classmethod
	def on_const_by(cls, builder: CP[MFBuilder], command: MFBuildCommand) -> MFExp:
		return builder.on.const_by(command.arg_at(0).as_string)

	# endregion
	# region 時間

	@classmethod
	def on_time(cls, builder: CP[MFBuilder], command: MFBuildCommand) -> MFExp:
		return builder.on.time()

	# endregion
	# region フロー制御

	@classmethod
	def on_ternary(cls, builder: CP[MFBuilder], command: MFBuildCommand) -> MFExp:
		values = cls.__emit_command(builder, command.arg_at(0)), cls.__emit_command(builder, command.arg_at(1)), cls.__emit_command(builder, command.arg_at(2))
		return builder.on.ternary(values[0], values[1], values[2])

	# endregion
	# region 関数コール

	@classmethod
	def on_call(cls, builder: CP[MFBuilder], command: MFBuildCommand) -> MFExp:
		return builder.on.call(command.name, [cls.__emit_command(builder, command.arg_at(index)) for index in range(command.arg_num)])

	# endregion
