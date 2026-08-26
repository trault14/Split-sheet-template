import os
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle

# Dimensions matching the original template
PAGE_WIDTH = 2550
PAGE_HEIGHT = 3629

def draw_text(c, text, x, y, font_name, font_size, color='#000000', anchor='left'):
    c.setFont(font_name, font_size)
    c.setFillColor(HexColor(color))
    if anchor == 'left':
        c.drawString(x, y, text)
    elif anchor == 'center':
        c.drawCentredString(x, y, text)
    elif anchor == 'right':
        c.drawRightString(x, y, text)

def draw_paragraph_top_left(c, p, x, y_top, width):
    w, h = p.wrap(width, 1000)
    p.drawOn(c, x, y_top - h)
    return h

def main():
    pdf_filename = "Split Sheet Template FR.pdf"
    c = canvas.Canvas(pdf_filename, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    
    # 1. Page Background (White)
    c.setFillColor(HexColor('#FFFFFF'))
    c.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, fill=1, stroke=0)
    
    # 2. Title
    draw_text(c, "SPLIT SHEET, ACCORD DE", 157.65, 3300, "Helvetica-Bold", 96)
    draw_text(c, "RÉPARTITION DES DROITS", 157.65, 3180, "Helvetica-Bold", 96)
    
    # 3. Metadata (Titre de l'œuvre, Date de création, Genre)
    c.setLineWidth(3)
    c.setStrokeColor(HexColor('#000000'))
    
    # Titre de l'œuvre
    draw_text(c, "Titre de l'œuvre :", 157.65, 2950, "Helvetica-Bold", 45)
    c.line(550, 2950, 2342.30, 2950)
    
    # Date de création
    draw_text(c, "Date de création :", 157.65, 2800, "Helvetica-Bold", 45)
    c.line(570, 2800, 1250, 2800)
    
    # Genre
    draw_text(c, "Genre :", 1350, 2800, "Helvetica-Bold", 45)
    c.line(1530, 2800, 2342.30, 2800)
    
    # 4. Table Elements
    # Column Definitions: (Title, Width)
    cols = [
        ("Contributeur", 450),
        ("E-mail", 350),
        ("Rôle", 400),
        ("%", 150),
        ("OGC", 240),
        ("IPI", 250),
        ("Éditeur", 359.25)
    ]
    
    table_left = 176.38
    table_width = 2199.25
    table_top = 2530.15
    header_height = 119.32
    row_height = 119.08
    num_rows = 5
    
    # Table Header Background
    c.setFillColor(HexColor('#0c1b2b'))
    c.rect(table_left, table_top - header_height, table_width, header_height, fill=1, stroke=0)
    
    # Draw Header Text & Vertical Lines Coordinates
    current_x = table_left
    col_x_coords = [table_left]
    for title, width in cols:
        center_x = current_x + width / 2
        # Vertically center text in header cell
        draw_text(c, title, center_x, table_top - header_height + 40, "Helvetica-Bold", 36, color='#FFFFFF', anchor='center')
        current_x += width
        col_x_coords.append(current_x)
        
    # Draw Table Grid Lines
    c.setLineWidth(3)
    c.setStrokeColor(HexColor('#000000'))
    
    # Horizontal lines
    c.line(table_left, table_top, table_left + table_width, table_top) # Top border
    c.line(table_left, table_top - header_height, table_left + table_width, table_top - header_height) # Header separator
    for r in range(1, num_rows + 1):
        y = table_top - header_height - r * row_height
        c.line(table_left, y, table_left + table_width, y)
        
    # Vertical lines
    table_bottom = table_top - header_height - num_rows * row_height
    for x in col_x_coords:
        c.line(x, table_top, x, table_bottom)
        
    # 5. Terms Paragraphs
    # Total : 100 %
    draw_text(c, "Total : 100 %", 157.65, 1740, "Helvetica-Bold", 45)
    
    style_terms = ParagraphStyle(
        name='Terms',
        fontName='Helvetica',
        fontSize=42,
        leading=65,
        textColor=HexColor('#000000')
    )
    
    terms_text1 = (
        "Les soussignés déclarent être les seuls auteurs et compositeurs de l'œuvre mentionnée "
        "ci-dessus et acceptent la répartition des droits telle que définie dans le présent document."
    )
    terms_text2 = (
        "La déclaration de l'œuvre auprès de la SACEM sera effectuée par : "
        "____________________________________________________"
    )
    terms_text3 = (
        "Fait à ______________________________________, le ______________________________________"
    )
    
    terms_p1 = Paragraph(terms_text1, style_terms)
    h_terms1 = draw_paragraph_top_left(c, terms_p1, 157.65, 1630, 2184.96)
    
    terms_p2 = Paragraph(terms_text2, style_terms)
    h_terms2 = draw_paragraph_top_left(c, terms_p2, 157.65, 1630 - h_terms1 - 60, 2184.96)
    
    terms_p3 = Paragraph(terms_text3, style_terms)
    h_terms3 = draw_paragraph_top_left(c, terms_p3, 157.65, 1630 - h_terms1 - 60 - h_terms2 - 60, 2184.96)
    
    # 6. Signatures Section
    draw_text(c, "Signatures :", 157.65, 1100, "Helvetica-Bold", 45)
    
    y_sig = 980
    for i in range(1, 6):
        # Bullet point
        draw_text(c, "•", 157.65, y_sig, "Helvetica", 40)
        # Text
        draw_text(c, f"Contributeur {i} :", 220, y_sig, "Helvetica", 40)
        # Underline
        c.setLineWidth(3)
        c.setStrokeColor(HexColor('#000000'))
        c.line(550, y_sig, 2342.30, y_sig)
        y_sig -= 110
        
    c.save()
    print("PDF generated successfully.")

if __name__ == "__main__":
    main()
