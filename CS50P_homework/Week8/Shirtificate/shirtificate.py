from pathlib import Path
from typing import Literal

from fpdf import FPDF
from fpdf.enums import DocumentCompliance, PageOrientation

# 可选的类实现
# class Shirt(FPDF):
#     def __init__(self, orientation: str | PageOrientation = PageOrientation.PORTRAIT, unit: str | float = "mm", format: str | tuple[float, float] = "A4", font_cache_dir: Literal['DEPRECATED'] = "DEPRECATED", *, enforce_compliance: str | DocumentCompliance | None = None) -> None:
#         super().__init__(orientation, unit, format, font_cache_dir, enforce_compliance=enforce_compliance)
#     def shirtificate(self, name):
#         self.image("shirtificate.png")


def main():
    # 提示用户输入名字。题目要求生成的文字格式是：
    # "{name} took CS50"
    name = input("Name: ")

    # 创建一个 PDF 对象。
    # orientation="P" 表示 Portrait，即纵向页面。
    # unit="mm" 表示后续所有坐标和尺寸都使用毫米。
    # format="A4" 表示页面大小是 A4，也就是 210mm x 297mm。
    pdf = FPDF(orientation="P", unit="mm", format="A4")

    # 添加一页空白页面。FPDF 必须先 add_page，之后才能写文字或放图片。
    pdf.add_page()

    # 设置标题字体。
    # helvetica 是 fpdf 内置字体之一，"B" 表示 bold 粗体，48 是字号。
    pdf.set_font("helvetica", "B", 48)

    # 在页面顶部写标题。
    # w=0 表示单元格宽度自动延伸到当前行的右边界。
    # h=30 表示这个单元格高度是 30mm。
    # align="C" 表示文字在单元格里水平居中。
    pdf.cell(0, 30, "CS50 Shirtificate", align="C")

    # 获取 shirtificate.png 的绝对位置。
    # Path(__file__) 是当前 Python 文件的位置。
    # with_name("shirtificate.png") 表示使用同一目录下的 shirtificate.png。
    # 这样无论从哪个工作目录运行脚本，都能找到图片。
    shirt_path = Path(__file__).with_name("shirtificate.png")

    # 设置衬衫图片宽度为 190mm。
    # A4 页面宽度是 210mm，所以左右各留大约 10mm 边距。
    shirt_width = 190

    # 计算图片左上角的 x 坐标，让图片水平居中。
    # pdf.w 是当前页面总宽度，A4 纵向时是 210mm。
    # 页面宽度减去图片宽度，再除以 2，就是左边距。
    shirt_x = (pdf.w - shirt_width) / 2

    # 把衬衫图片放到 PDF 中。
    # x 控制图片左边位置，y=60 表示图片从页面顶部 60mm 处开始。
    # w=shirt_width 表示按指定宽度缩放图片，高度会自动按比例缩放。
    pdf.image(str(shirt_path), x=shirt_x, y=60, w=shirt_width)

    # 设置名字文字的字体和颜色。
    # 题目要求名字文字显示在衬衫上，并且是白色。
    pdf.set_font("helvetica", "B", 24)
    pdf.set_text_color(255, 255, 255)

    # 把当前写入位置移动到 y=135mm。
    # 这个位置大约落在衬衫胸口区域，适合覆盖在图片上。
    pdf.set_y(135)

    # 写入用户名字。
    # w=0 让单元格占满当前行可用宽度，align="C" 让文字水平居中。
    pdf.cell(0, 10, f"{name} took CS50", align="C")

    # 将 PDF 保存到当前运行目录下，文件名必须是题目指定的 shirtificate.pdf。
    pdf.output("shirtificate.pdf")


# 只有当这个文件被直接运行时，才调用 main()。
# 如果这个文件被其他测试文件 import，main() 不会自动执行。
if __name__ == "__main__":
    main()
