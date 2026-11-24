from script.mfs.core.me import ME
from script.mfs.core.me_types import Blends, Domains
from script.mfs.func.ui.mfs_ui_main import ui_main


def ui_master() -> None:
	"""マテリアル(UI)"""
	ME.schema_domain(Domains.UI.name)
	ME.schema_blend(Blends.Translucent.name)

	uv = ME.tex_coord(0)
	color, opacity = ui_main(uv)

	ME.output_emissive_color(color)
	ME.output_opacity(opacity)
