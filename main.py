import tkinter as tk
import os

# สร้างหน้าต่างหลัก
app = tk.Tk()
app.title("LayoutDesign Group")
app.geometry("1000x600")

# สร้างเฟรมสำหรับ layout
toolbar = tk.Frame(app, padx=8, pady=6)
toolbar.pack(side="top", fill="x")

main_area = tk.Frame(app)
main_area.pack(side="top", fill="both", expand=True)

palette = tk.Frame(main_area, bg="#eaeaea", width=200)
palette.pack(side="left", fill="y")

workspace = tk.Frame(main_area, bg="#f5f5f5")
workspace.pack(side="left", expand=True, fill="both")

#==================================================#

# ฟังก์ชันช่วยสร้างปุ่ม
def create_button(parent, text, row, col):
    btn = tk.Button(parent, text=text, width=15)
    btn.grid(row=row, column=col, padx=5, pady=5)
    return btn

# สร้างปุ่มใน toolbar
btn_1 = create_button(toolbar, "Save",   0, 0)
btn_2 = create_button(toolbar, "Load",   0, 1)
btn_3 = create_button(toolbar, "Export", 0, 2)

#==================================================#

current_drag_widget = None  # ใช้เก็บวิดเจ็ตที่กำลังลาก

# ฟังก์ชั่นจัด Drag & Drop
def drag_start(event):
    global current_drag_widget
    template = event.widget  # widget ต้นแบบใน palette
    
    # สร้างวิดเจ็ตใหม่ใน workspace
    current_drag_widget = tk.Label(
        workspace,
        text=template.cget("text"),
        bg=template.cget("bg"),
        width=template.cget("width"),
        height=template.cget("height")
    )
    current_drag_widget.drag_offset_x = event.x
    current_drag_widget.drag_offset_y = event.y

    current_drag_widget.widget_type = template.cget("text")  # เก็บประเภท widget

# ฟังก์ชันลาก widget
def do_drag(event):
    if current_drag_widget:
        x = event.x_root - workspace.winfo_rootx() - current_drag_widget.drag_offset_x
        y = event.y_root - workspace.winfo_rooty() - current_drag_widget.drag_offset_y
        current_drag_widget.place(x=x, y=y)

# ฟังก์ชันหยุดลากวิดเจ็ต
def drag_stop(event):
    global current_drag_widget
    current_drag_widget = None # เคลียร์สถานะการลาก

# สร้างวิดเจ็ตใน palette
drag_label = tk.Label(palette, text="Div", bg="#d1e7dd", width=15, height=2)
drag_label.place(x=20, y=40)

drag_label_2 = tk.Label(palette, text="Header", bg="#d1e7dd", width=15, height=2)
drag_label_2.place(x=20, y=80)

drag_label_3 = tk.Label(palette, text="Button", bg="#d1e7dd", width=15, height=2)
drag_label_3.place(x=20, y=120)

# เชื่อมฟังก์ชัน Drag & Drop กับวิดเจ็ตใน palette
for connect_widget in (drag_label, drag_label_2, drag_label_3):
    connect_widget.bind("<Button-1>", drag_start)
    connect_widget.bind("<B1-Motion>", do_drag)
    connect_widget.bind("<ButtonRelease-1>", drag_stop)

#==================================================#

# ฟังก์ชั่น Export layout
def export_layout():
    html_elements = []

    # วนลูปผ่าน widget ทั้งหมดใน workspace
    for child in workspace.winfo_children():
        # ข้ามถ้า widget ไม่มี attribute นี้ (กัน error)
        widget_type = getattr(child, "widget_type", None)
        if not widget_type:
            continue

        # ดึงข้อมูลตำแหน่งและขนาด
        x = child.winfo_x()
        y = child.winfo_y()
        w = child.winfo_width()
        h = child.winfo_height()
        text = child.cget("text")

        # สร้างโค้ด HTML ตามประเภท widget
        if widget_type == "Div":
            element = f'<div class="box" style="left:{x}px; top:{y}px; width:{w}px; height:{h}px;"></div>'
        elif widget_type == "Header":
            element = f'<div class="header" style="left:{x}px; top:{y}px;">{text}</div>'
        elif widget_type == "Button":
            element = f'<button class="btn" style="left:{x}px; top:{y}px;">{text}</button>'
        else:
            # เอาไว้เพิ่มนะน้อง Keyes(เอาไว้เพิ่ม element ใหม่ในอนาคต)
            continue
        html_elements.append("  " + element)

    # สร้างโฟลเดอร์
    output_dir = "src"
    os.makedirs(output_dir, exist_ok=True)

    # อ่าน template.html
    template_path = os.path.join(output_dir, "template.html")
    with open(template_path, "r", encoding="utf-8") as f:
        template_html = f.read()

    # แทนที่ {{ELEMENTS}} ด้วยโค้ด HTML ที่สร้างขึ้น
    elements_html = "\n".join(html_elements)
    export_html = template_html.replace("{{ELEMENTS}}", elements_html)

    # เขียนไฟล์ export.html
    with open(os.path.join(output_dir, "export.html"), "w", encoding="utf-8") as f:
        f.write(export_html)

    print("Export เสร็จแล้ว: src/export.html (ใช้ src/style.css)")

# เชื่อมปุ่ม Export กับฟังก์ชัน
btn_3.config(command=export_layout)

#==================================================#

# เปลี่ยนโลโก้
try:
    logo = tk.PhotoImage(file="assets/image/logo.png")
    app.iconphoto(True, logo)
except Exception as e:
    print("โหลดโลโก้ไม่สำเร็จ:", e)

# วนการทำงาน
app.mainloop()

#==================================================#
